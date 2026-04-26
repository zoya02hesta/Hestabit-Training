import time
import os
from PIL import Image


from sentence_transformers import SentenceTransformer
from src.retriever.text_retriever import TextRetriever
from src.retriever.image_search import ImageSearch


from src.generator.sql_generator import SQLGenerator
from src.pipelines.sql_pipeline import SQLPipeline
from src.utils.schema_loader import load_schema




from src.evaluation.rag_eval import RAGEvaluator


class App:
    def __init__(self):
        
        self.model = SentenceTransformer("clip-ViT-B-32")
        self.text_retriever = TextRetriever()
        self.memory = []
        
        self.image_data = self.load_images("src/data/images")
        self.image_searcher = ImageSearch(self.image_data)

        
        
        print("⚡ Using Groq for SQL...")

        self.sql_generator = SQLGenerator()

        schema = load_schema("test.db")

        self.sql_pipeline = SQLPipeline(
            db_path="test.db",
            generator=self.sql_generator,
            schema=schema
        )

        # ✅ EVALUATOR
        self.evaluator = RAGEvaluator()

        print("✅ App Ready!")

    # ---------------- TEXT ----------------
    def ask_text(self, query):
        context = self.text_retriever.retrieve(query)

        answer = f"""
    Based on retrieved knowledge:

    {context}

    Conclusion:
    This answer is generated using RAG.
    """

        # ✅ USE evaluator properly
        eval_result = self.evaluator.evaluate(query, answer, context)

        return {
            "type": "text",
            "data": answer,
            "confidence": eval_result["confidence"],
            "hallucination": eval_result["hallucination"]
        }

    # ---------------- IMAGE ----------------

   

    def load_images(self, image_folder):
        import os
        from src.pipelines.image_ingest import ImageIngestor
        
        ingestor = ImageIngestor()
        image_data = []

        for file in os.listdir(image_folder):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(image_folder, file)
                
                try:
                    result = ingestor.process_image(path)
                    
                    # Convert embedding to numpy if needed
                    emb = result["embedding"]
                    if hasattr(emb, "cpu"):
                        emb = emb.cpu().numpy()
                        
                    image_data.append({
                        "image_path": result["image_path"],
                        "caption": result["caption"],
                        "ocr": result.get("ocr_text", ""),
                        "embedding": emb
                    })
                except Exception as e:
                    print(f"Error processing {path}: {e}")

        return image_data

    def ask_image(self, query=None, image_input=None):
        if image_input:
            results = self.image_searcher.search(query=None, image_input=image_input)
            self.update_memory("Uploaded Image", results)
        else:
            context = " ".join([m["query"] for m in self.memory if isinstance(m["query"], str)])
            refined_query = f"{context} {query}".strip()
            results = self.image_searcher.search(query=refined_query)
            self.update_memory(query, results)

        return {
            "type": "image",
            "data": results,
            "confidence": max([r.get("score", 0) for r in results], default=0),
            "hallucination": False
        }

    # ---------------- SQL ----------------
    def ask_sql(self, query):
        start_time = time.time()

        result_dict = self.sql_pipeline.run(query)

        print(f"⏱ Time taken: {time.time() - start_time:.2f}s")

        summary = result_dict.get("summary", "")

        if "Returned" in str(summary) or len(result_dict.get("raw", [])) > 0:
            confidence = 0.9
            hallucination = False
        else:
            confidence = 0.4
            hallucination = True

        return {
            "type": "sql",
            "data": summary,
            "sql": result_dict.get("sql", ""),
            "raw": result_dict.get("raw", []),
            "confidence": confidence,
            "hallucination": hallucination
        }

    def feedback(self, query, feedback_text):
        import json
        from datetime import datetime

        entry = {
            "timestamp": str(datetime.now()),
            "query": query,
            "feedback": feedback_text
        }

        try:
            with open("CHAT-LOGS.json", "r") as f:
                logs = json.load(f)
        except:
            logs = []

        logs.append(entry)

        with open("CHAT-LOGS.json", "w") as f:
            json.dump(logs, f, indent=2)

        return {"status": "feedback recorded"}



    def ask(self, query):
        result = self.text_retriever.retrieve(query)

        confidence = max(result["scores"]) if result["scores"] else 0.0
        context = result["data"]
        
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            
            # Initial generation
            prompt = f"Given the following context from our documents, answer the question naturally. Context:\n{context}\n\nQuestion: {query}"
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            answer = response.choices[0].message.content.strip()
            
            # Reflection step
            eval_result = self.evaluator.evaluate(query, answer, context)
            
            if eval_result.get("hallucination", False) or eval_result.get("context_score", 1.0) < 0.6:
                refine_prompt = f"""
                You previously answered the question: "{query}"
                Using the context: "{context}"
                
                Your previous answer was: "{answer}"
                
                Critique: Your answer was detected as either containing hallucinations or lacking faithfulness to the context. 
                Please refine your answer to strictly rely ONLY on the provided context. Do not invent information.
                """
                refine_response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": refine_prompt}],
                    temperature=0
                )
                answer = refine_response.choices[0].message.content.strip()
                # Re-evaluate post-refinement
                eval_result = self.evaluator.evaluate(query, answer, context)
                
            confidence = eval_result.get("confidence", confidence)
            hallucination = eval_result.get("hallucination", False)
                
        except Exception as e:
            print("Error in ask:", e)
            answer = f"Based on retrieved knowledge:\n{context}"
            hallucination = confidence < 0.2

        self.update_memory(query, answer)

        return {
            "type": "text",
            "data": answer,
            "confidence": confidence,
            "hallucination": hallucination
        }

    def update_memory(self, query, response):
        self.memory.append({
            "query": query,
            "response": response
        })

        # keep only last 5
        self.memory = self.memory[-5:]
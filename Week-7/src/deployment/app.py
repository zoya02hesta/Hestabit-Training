import time
import os
from PIL import Image

# TEXT + IMAGE
from sentence_transformers import SentenceTransformer
from src.retriever.text_retriever import TextRetriever
from src.retriever.image_search import ImageSearch

# SQL
from src.generator.sql_generator import SQLGenerator
from src.pipelines.sql_pipeline import SQLPipeline
from src.utils.schema_loader import load_schema



# ✅ EVALUATION
from src.evaluation.rag_eval import RAGEvaluator


class App:
    def __init__(self):
        # ---------------- TEXT ----------------
        self.model = SentenceTransformer("clip-ViT-B-32")
        self.text_data = [
            "Credit underwriting evaluates risk before lending.",
            "Banks analyze income, credit score, and repayment history.",
            "Underwriting helps prevent loan defaults."
        ]
        self.text_retriever = TextRetriever(self.text_data)
        self.memory = []
        # ---------------- IMAGE ----------------
        self.image_data = self.load_images("src/data/images")
        self.image_searcher = ImageSearch(self.image_data)

        # ---------------- SQL ----------------
        
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

        image_data = []

        for file in os.listdir(image_folder):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join(image_folder, file)

                image = Image.open(path).convert("RGB")

                embedding = self.model.encode(image, convert_to_tensor=True)

                caption = file.replace("_", " ").split(".")[0]

                image_data.append({
                    "image_path": path,
                    "caption": caption,
                    "ocr": "",
                    "embedding": embedding.cpu().numpy()  # convert to numpy for storage
                })

        return image_data

    def ask_image(self, query):
        context = " ".join([m["query"] for m in self.memory])
        refined_query = f"{context} {query}"

        results = self.image_searcher.search(refined_query)

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

        result = self.sql_pipeline.run(query)

        print(f"⏱ Time taken: {time.time() - start_time:.2f}s")

        if "Returned" in str(result):
            confidence = 0.9
            hallucination = False
        else:
            confidence = 0.4
            hallucination = True

        return {
            "type": "sql",
            "data": result,
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

    # ---------------- ROUTER ----------------
    # def ask(self, query):
    #     query_lower = query.lower()

    #     if any(word in query_lower for word in ["image", "photo", "picture", "show"]):
    #         return self.ask_image(query)

    #     elif any(word in query_lower for word in ["count", "list", "show users", "how many", "total"]):
    #         return self.ask_sql(query)

    #     else:
    #         return self.ask_text(query)

    def ask(self, query):
        result = self.text_retriever.retrieve(query)

        confidence = max(result["scores"])

        hallucination = confidence < 0.5

        if hallucination:
            refined_query = f"Give a more detailed answer for: {query}"
            result = self.text_retriever.retrieve(refined_query)

        self.update_memory(query, result["data"])

        return {
            "type": "text",
            "data": result["data"],
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
import os
import sys
from groq import Groq
from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

class NexusMemoryManager:
    """
    Unified manager for Day 4 memory systems.
    Integrates Session (Short-term), SQLite (Long-term), and FAISS (Vector).
    """

    def __init__(self, session_window=6, top_k_recall=5):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
        self.session = SessionMemory(window_size=session_window, client=self.client, model=self.model)
        self.vectors = VectorStore(persist=True)
        self.ltm = LongTermMemory()
        self.top_k = top_k_recall
        
        self.session_id = self.session.session_id
        
        print(f"[INFO] MemoryManager initialized (Session: {self.session_id})")

    def recall(self, query: str) -> str:
        """
        Retrieves context from all 3 memory layers with higher sensitivity.
        """
        context_parts = []
        clean_query = query.lower().strip("?!.")

        # 1. Semantic Recall (Vector) - Increased top_k
        vector_context = self.vectors.search_as_context(clean_query, top_k=self.top_k)
        if vector_context:
            context_parts.append(vector_context)

        # 2. Fact Recall (SQLite) - Smarter keyword matching
        # Include 3-letter words like 'who', 'age' but filter common stops later
        keywords = [k for k in clean_query.split() if len(k) >= 3][:5]
        
        found_facts = []
        if keywords:
            for kw in keywords:
                facts = self.ltm.search_facts(keyword=kw, limit=3)
                for f in facts:
                    if f['fact'] not in found_facts:
                        found_facts.append(f['fact'])

        if found_facts:
            lines = ["=== Deep Memory Facts ==="]
            lines.extend([f"- {fact}" for fact in found_facts])
            context_parts.append("\n".join(lines))

        # 3. Session Context (Short-term window)
        session_context = self.session.get_context_string()
        if session_context:
            context_parts.append(session_context)

        return "\n\n".join(context_parts)

    def store(self, user_query: str, agent_response: str):
        """
        Persists a conversation turn across all memory layers.
        """
        # Store in Session (and extract facts)
        self.session.add_turn("user", user_query)
        new_facts = self.session.add_turn("assistant", agent_response, extract_facts=True)

        # Store in Long-Term Memory (SQLite)
        self.ltm.save_turn(self.session_id, "user", user_query)
        self.ltm.save_turn(self.session_id, "assistant", agent_response)
        
        if new_facts:
            self.ltm.save_facts(self.session_id, new_facts, source="conversation")

        # Store in Vector Memory (FAISS)
        self.vectors.add(f"Q: {user_query} | A: {agent_response[:300]}", {"session": self.session_id})
        for fact in new_facts:
            self.vectors.add(fact, {"type": "fact", "session": self.session_id})

    def stats(self):
        return {
            "vectors": self.vectors.stats()["total_vectors"],
            "facts": self.ltm.stats()["total_facts"],
            "turns": self.ltm.stats()["total_turns"]
        }

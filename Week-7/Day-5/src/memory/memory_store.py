import json
from collections import deque


class MemoryStore:
    def __init__(self, max_size=5):
        self.memory = deque(maxlen=max_size)

    def add(self, query, answer):
        self.memory.append({
            "query": query,
            "answer": answer
        })

    def get_context(self):
        if not self.memory:
            return ""

        context = "Conversation History:\n"
        for item in self.memory:
            context += f"User: {item['query']}\nAssistant: {item['answer']}\n"

        return context
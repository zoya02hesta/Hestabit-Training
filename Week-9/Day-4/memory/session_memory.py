"""
memory/session_memory.py

Short-Term Session Memory
- Stores the current conversation in-memory.
- Maintains a rolling window of recent turns.
- Extracts key facts from each turn.
"""

import os
import json
from datetime import datetime

FACT_EXTRACTION_PROMPT = """You are a memory extraction agent.
Given a conversation turn (user query + agent response), extract
1-3 important facts worth remembering for future reference.

Output ONLY a JSON array of short fact strings. Example:
["User is analyzing sales data", "Top product is Laptop Pro with $18000 revenue"]

If nothing important, return: []
"""

class SessionMemory:
    """
    In-memory short-term store for one agent session.
    """

    def __init__(self, window_size: int = 6, client=None, model: str = "llama-3.3-70b-versatile"):
        self.window_size = window_size
        self.client = client
        self.model = model
        self.history: list[dict] = []
        self.window: list[dict] = []
        self.facts: list[str] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"[INFO] SessionMemory initialized (Session ID: {self.session_id})")

    def add_turn(self, role: str, content: str, extract_facts: bool = False) -> list[str]:
        """Add a user or assistant turn to memory."""
        turn = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        self.history.append(turn)

        self.window.append({"role": role, "content": content})
        if len(self.window) > self.window_size:
            self.window.pop(0)

        new_facts = []
        if extract_facts and role == "assistant" and len(self.history) >= 2:
            new_facts = self._extract_facts(
                self.history[-2]["content"],
                content
            )
            self.facts.extend(new_facts)

        return new_facts

    def _extract_facts(self, user_msg: str, agent_response: str) -> list[str]:
        """Extract memorable facts from a turn."""
        if not self.client:
            return []
        try:
            prompt = (
                f"User said: {user_msg}\n"
                f"Agent responded: {agent_response[:800]}"
            )
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": FACT_EXTRACTION_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                max_tokens=256,
            )
            raw = response.choices[0].message.content.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            facts = json.loads(raw)
            if isinstance(facts, list):
                print(f"[INFO] Extracted {len(facts)} facts from turn")
                return facts
        except Exception as e:
            print(f"[ERROR] Fact extraction failed: {e}")
        return []

    def get_context_string(self) -> str:
        """Build a context block for prompt injection."""
        parts = []

        if self.facts:
            parts.append("=== Recent Key Facts ===")
            for f in self.facts[-10:]:
                parts.append(f"- {f}")

        if self.window:
            parts.append("\n=== Recent Conversation ===")
            for turn in self.window:
                role = "User" if turn["role"] == "user" else "Agent"
                parts.append(f"{role}: {turn['content'][:300]}")

        return "\n".join(parts) if parts else ""

    def summary(self) -> dict:
        return {
            "session_id": self.session_id,
            "total_turns": len(self.history),
            "window_size": len(self.window),
            "facts_count": len(self.facts),
        }

    def clear(self):
        """Reset working memory window."""
        self.window = []
        print("[INFO] SessionMemory window cleared.")

    def reset(self):
        """Full reset for a new session."""
        self.__init__(self.window_size, self.client, self.model)

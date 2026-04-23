"""
memory_agent.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 4 — Memory Systems | Week 9 Agentic AI

MEMORY-AWARE AGENT — Fully Dynamic
  • No hardcoded data anywhere
  • Memory builds purely from your conversations
  • Each chat turn is stored across all 3 layers automatically
  • Recall grows richer the more you chat

Flow:
  New Query → Recall (FAISS + SQLite + Session)
            → Inject context → Generate (Groq)
            → Extract facts → Store in all 3 layers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os, sys, json
from groq import Groq

sys.path.insert(0, os.path.dirname(__file__))
from memory.session_memory   import SessionMemory
from memory.vector_store     import VectorStore
from memory.long_term_memory import LongTermMemory

# ── Config ────────────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a helpful AI assistant with memory.
You will be given recalled context from past conversations and vector memory.
Use this context to give more accurate, personalised responses.
If recalled context is relevant, reference it naturally.
If no context is relevant, answer from your own knowledge.
"""


class MemoryAgent:
    """
    A conversational agent with 3-layer memory.

    Parameters
    ----------
    session_window : int — how many turns to keep in short-term memory
    top_k_recall   : int — how many vector memories to recall per query
    """

    def __init__(self, session_window: int = 6, top_k_recall: int = 3):
        self.session = SessionMemory(window_size=session_window)
        self.vectors = VectorStore(persist=True)
        self.ltm     = LongTermMemory()
        self.top_k   = top_k_recall

        print(f"\n🤖 [MemoryAgent] Initialised")
        print(f"   Session  : {self.session.session_id}")
        print(f"   Vectors  : {self.vectors.stats()['total_vectors']} stored")
        print(f"   LTM      : {self.ltm.stats()['total_facts']} facts stored\n")

    # ── Memory recall ─────────────────────────────────────
    def _recall(self, query: str) -> str:
        """Search all memory layers and build a context block."""
        context_parts = []

        # 1. Vector memory — semantic similarity
        vector_context = self.vectors.search_as_context(query, top_k=self.top_k)
        if vector_context:
            context_parts.append(vector_context)

        # 2. Long-term memory — keyword search
        for kw in query.split()[:3]:
            facts = self.ltm.search_facts(keyword=kw, limit=3)
            if facts:
                lines = [f"=== Long-Term Memory (keyword: '{kw}') ==="]
                for f in facts:
                    lines.append(f"• {f['fact']} [from {f.get('source', '?')}]")
                context_parts.append("\n".join(lines))
                break

        # 3. Short-term — recent conversation window
        session_context = self.session.get_context_string()
        if session_context:
            context_parts.append(session_context)

        return "\n\n".join(context_parts)

    # ── Generate ──────────────────────────────────────────
    def chat(self, user_query: str) -> str:
        """
        Full memory flow:
        Recall → Inject → Generate → Extract facts → Store
        """
        print(f"\n👤 User: {user_query}")
        print("🔍 [MemoryAgent] Recalling from memory...")

        # Step 1: Recall
        recalled_context = self._recall(user_query)
        if recalled_context:
            print(f"📚 [MemoryAgent] Context recalled ({len(recalled_context)} chars)")
        else:
            print("📭 [MemoryAgent] No relevant memory found — this will be stored for future recall")

        # Step 2: Build messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if recalled_context:
            messages.append({
                "role":    "system",
                "content": f"Recalled Memory Context:\n{recalled_context}"
            })
        messages.extend(self.session.get_window_messages())
        messages.append({"role": "user", "content": user_query})

        # Step 3: Generate
        response = client.chat.completions.create(
            model=MODEL, messages=messages,
            temperature=0.3, max_tokens=1024,
        )
        answer = response.choices[0].message.content.strip()
        print(f"\n🤖 Agent: {answer}\n")

        # Step 4: Store in all 3 memory layers
        self.session.add_turn("user", user_query)
        new_facts = self.session.add_turn("assistant", answer, extract_facts=True)

        self.ltm.save_turn(self.session.session_id, "user",      user_query)
        self.ltm.save_turn(self.session.session_id, "assistant", answer)
        if new_facts:
            self.ltm.save_facts(
                self.session.session_id, new_facts,
                source="conversation", tag="auto-extracted"
            )

        self.vectors.add(
            f"Q: {user_query} | A: {answer[:200]}",
            {"type": "conversation", "session": self.session.session_id}
        )
        for fact in new_facts:
            self.vectors.add(
                fact,
                {"type": "fact", "session": self.session.session_id}
            )

        return answer

    def memory_stats(self) -> dict:
        return {
            "session":      self.session.summary(),
            "vector_store": self.vectors.stats(),
            "long_term":    self.ltm.stats(),
        }


# ── Interactive CLI ───────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  MEMORY-AWARE AGENT — Day 4, Week 9")
    print("  Memory builds dynamically from your conversation.")
    print("  The more you chat, the richer the memory gets.")
    print("─"*60)
    print("  Commands:")
    print("    stats  → show memory state across all 3 layers")
    print("    clear  → reset session (short-term) memory")
    print("    reset  → wipe ALL memory (FAISS + SQLite + session)")
    print("    quit   → exit")
    print("═"*60)

    agent = MemoryAgent(session_window=6, top_k_recall=3)

    # Show what's already in memory from previous sessions
    total_vectors = agent.vectors.stats()["total_vectors"]
    total_facts   = agent.ltm.stats()["total_facts"]

    if total_vectors > 0 or total_facts > 0:
        print(f"\n📂 Memory from previous sessions loaded:")
        print(f"   {total_vectors} vectors in FAISS")
        print(f"   {total_facts} facts in SQLite")
    else:
        print("\n📭 No previous memory found — starting fresh.")
        print("   Ask anything and I'll remember it for next time!\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        elif user_input.lower() == "quit":
            print("Goodbye!")
            break
        elif user_input.lower() == "stats":
            print(json.dumps(agent.memory_stats(), indent=2))
        elif user_input.lower() == "clear":
            agent.session.clear()
            print("🔄 Short-term session memory cleared.")
        elif user_input.lower() == "reset":
            agent.vectors.clear()
            agent.ltm.clear_all()
            agent.session.reset()
            print("🗑️  All memory wiped — starting completely fresh.")
        else:
            agent.chat(user_input)
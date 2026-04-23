# 🧠 MEMORY-SYSTEM.md — Day 4: Memory Systems

> **Week 9 — Agentic AI & Multi-Agent System Design**
> Stack: FAISS | SQLite | sentence-transformers | Groq

---

## Architecture Overview

```
New Query
    │
    ▼
┌─────────────────────────────────────┐
│           MEMORY RECALL             │
│                                     │
│  ┌─────────────┐  ┌──────────────┐  │
│  │ VectorStore │  │  LongTerm    │  │
│  │   (FAISS)   │  │   (SQLite)   │  │
│  │  semantic   │  │   keyword    │  │
│  │   search    │  │   search     │  │
│  └─────────────┘  └──────────────┘  │
│         │                │          │
│         └──────┬─────────┘          │
│                │                    │
│  ┌─────────────▼──────────────┐     │
│  │     SessionMemory          │     │
│  │   (recent window)          │     │
│  └────────────────────────────┘     │
└──────────────┬──────────────────────┘
               │ recalled context
               ▼
    ┌──────────────────────┐
    │   PROMPT INJECTION   │
    │  system + context    │
    │  + conversation      │
    │  + user query        │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │    Groq LLM          │
    │  (llama-3.3-70b)     │
    └──────────┬───────────┘
               │ response
               ▼
    ┌──────────────────────┐
    │    MEMORY STORAGE    │
    │                      │
    │  SessionMemory       │  ← in-memory window
    │  VectorStore (FAISS) │  ← embed + store
    │  LongTerm (SQLite)   │  ← persist to disk
    │  Fact Extraction     │  ← Groq extracts facts
    └──────────────────────┘
```

---

## Memory Layers

### 1. 🟡 Short-Term Memory (`memory/session_memory.py`)

| Property | Value |
|---|---|
| Storage | In-memory (Python list) |
| Scope | Current session only |
| Concept | Episodic + Working memory |
| Window | Last 6 turns (configurable) |
| Fact extraction | Groq extracts 1-3 facts per turn |

```python
from memory.session_memory import SessionMemory

mem = SessionMemory(window_size=6)
mem.add_turn("user", "What is the top product?")
facts = mem.add_turn("assistant", "Laptop Pro with $18,000", extract_facts=True)

print(mem.get_context_string())   # inject into prompt
print(mem.summary())              # stats
```

---

### 2. 🔵 Vector Memory (`memory/vector_store.py`)

| Property | Value |
|---|---|
| Storage | FAISS index on disk |
| Scope | Persists across sessions |
| Concept | Semantic memory |
| Model | all-MiniLM-L6-v2 (384-dim) |
| Search | Cosine similarity (L2) |

```python
from memory.vector_store import VectorStore

vs = VectorStore(persist=True)

# Store a fact
vs.add("West region leads with $19,105 in sales", {"source": "sales.csv"})

# Semantic search
results = vs.search("Which region has the most revenue?", top_k=3)
for r in results:
    print(f"[{r['rank']}] score={r['score']:.3f} | {r['text']}")

# As prompt context
context = vs.search_as_context("best performing region", top_k=3)
```

---

### 3. 🟢 Long-Term Memory (`memory/long_term_memory.py` → `long_term.db`)

| Property | Value |
|---|---|
| Storage | SQLite database |
| Scope | Permanent, survives restarts |
| Concept | Episodic + Semantic storage |
| Tables | conversations, facts, agent_outputs |

```python
from memory.long_term_memory import LongTermMemory

ltm = LongTermMemory()

# Save conversation
ltm.save_turn(session_id, "user", "Tell me about sales")
ltm.save_turn(session_id, "assistant", "Top product is Laptop Pro...")

# Save facts
ltm.save_facts(session_id, ["Laptop Pro earns $18,000"], source="sales.csv")

# Search by keyword
facts = ltm.search_facts(keyword="region")
sessions = ltm.get_all_sessions()
```

---

### 4. 🤖 Memory Agent (`memory_agent.py`)

Full memory-aware conversational agent tying all 3 layers together.

```python
from memory_agent import MemoryAgent

agent = MemoryAgent(session_window=6, top_k_recall=3)
answer = agent.chat("Who is the best salesperson?")
print(agent.memory_stats())
```

---

## Setup & Run

### 1. Install Dependencies
```bash
pip install groq faiss-cpu sentence-transformers
```

### 2. Set Groq API Key
```bash
export GROQ_API_KEY="gsk_your_key_here"
```

### 3. Run Individual Components
```bash
# Test short-term memory
python memory/session_memory.py

# Test vector store (FAISS)
python memory/vector_store.py

# Test long-term memory (SQLite)
python memory/long_term_memory.py
```

### 4. Run the Full Memory Agent
```bash
python memory_agent.py
```

---

## File Structure

```
Day-4/
├── memory/
│   ├── session_memory.py     ← Short-term (in-memory window)
│   ├── vector_store.py       ← Vector memory (FAISS)
│   ├── long_term_memory.py   ← Long-term (SQLite)
│   ├── long_term.db          ← SQLite DB (auto-created)
│   ├── faiss.index           ← FAISS index (auto-created)
│   └── faiss_meta.pkl        ← FAISS metadata (auto-created)
├── memory_agent.py           ← Full memory-aware agent
├── requirements.txt
└── MEMORY-SYSTEM.md          ← This file
```

---

## Key Concepts

| Concept | Implementation |
|---|---|
| **Episodic memory** | Full conversation log in SQLite + session history |
| **Semantic memory** | Distilled facts in FAISS + SQLite facts table |
| **Working memory** | Sliding window in SessionMemory (last N turns) |
| **Recall** | FAISS semantic search + SQLite keyword search |
| **Consolidation** | Groq extracts facts from each turn automatically |
| **Persistence** | FAISS index + SQLite survive process restarts |

---

## Memory Flow Example

```
User: "Who was the top salesperson?"

1. RECALL
   VectorStore → finds: "Dave is the top salesperson with $20,305"  (score=0.12)
   LongTerm    → finds: fact "Dave leads all salespeople"
   Session     → recent 4 turns injected

2. PROMPT INJECTION
   system: You are a helpful AI with memory...
   system: Recalled Memory: Dave is top salesperson...
   user:   [last 4 turns]
   user:   Who was the top salesperson?

3. GENERATE
   Agent: Based on our previous analysis, Dave is the top
          salesperson with $20,305 in total revenue...

4. STORE
   SessionMemory ← add turn (user + assistant)
   VectorStore   ← embed Q+A pair
   LongTerm      ← save turn + extracted facts
   Facts         ← ["Dave is top salesperson with $20,305"]
```

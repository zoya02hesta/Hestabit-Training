# 1. Activate virtual environment
source venv/bin/activate

# 2. Set Groq API key
export GROQ_API_KEY="gsk_your_key_here"

# 3. Seed the database (only needed once)
python seed_db.py

# 4. Run with default sales.csv
python orchestrator.py

# 5. Run with custom file
python orchestrator.py --file "organizations-100.csv"

# 6. Run with custom file + custom task
python orchestrator.py --file "organizations-100.csv" "List names of all organizations"

# 7. Run individual agents
python tools/file_agent.py
python tools/db_agent.py
python tools/code_executor.py
# action + file + question
python tools/file_agent.py "data/organizations-100.csv" "What countries are represented?"
python tools/file_agent.py "data/customers-100.csv" "List all unique cities"
python tools/file_agent.py "data/sales.csv" "Which product has highest sales?"

python tools/db_agent.py "Which organization was founded earliest?"
python tools/db_agent.py "How many customers are from each country?"
python tools/db_agent.py "What is the total revenue per region?"

python tools/code_executor.py "Load DATA_PATH and print top 5 rows"
python tools/code_executor.py "Compute average number of employees per industry"



Great question. Here's everything you're using, where, and what it actually does:

---

## Day 3 — Tool-Calling Agents

### 1. **Groq**
- **What**: Cloud API that gives you access to LLMs (like Llama 3.3)
- **Where**: Every agent — Planner, CodeAgent, FileAgent, DBAgent, Validator
- **Why**: Faster and free compared to OpenAI. Used as the "brain" for all reasoning
- **What it does here**: Generates Python code, SQL queries, analyses file content, plans which agents to call, synthesises final answers

### 2. **Llama 3.3 70B** (`llama-3.3-70b-versatile`)
- **What**: The actual LLM model running on Groq's servers
- **Where**: All Groq API calls
- **Why**: 70 billion parameter model — powerful enough for code gen, SQL gen, analysis
- **What it does here**: The actual intelligence behind every agent decision

### 3. **SQLite**
- **What**: A lightweight file-based relational database, no server needed
- **Where**: `tools/db_agent.py`
- **Why**: Built into Python (`import sqlite3`), zero setup, perfect for local agents
- **What it does here**: Stores CSV data in-memory, runs SQL queries against it dynamically

### 4. **Pandas**
- **What**: Python data analysis library
- **Where**: Inside CodeAgent's generated Python scripts
- **Why**: Best tool for CSV manipulation — groupby, sort, filter, aggregate
- **What it does here**: CodeAgent generates pandas code to compute insights from any CSV

### 5. **Subprocess** (Python stdlib)
- **What**: Runs shell commands / Python scripts from within Python
- **Where**: `tools/code_executor.py`
- **Why**: Isolates generated code execution — if it crashes, your main program is safe
- **What it does here**: Runs LLM-generated Python in a separate process with a 30s timeout

### 6. **CSV / DictReader** (Python stdlib)
- **What**: Built-in CSV reader
- **Where**: `orchestrator.py`, `tools/db_agent.py`
- **Why**: No extra install needed, reads column names dynamically
- **What it does here**: Sniffs column names from any CSV at runtime, feeds them to agents

---

## Day 4 — Memory Systems

### 7. **FAISS** (`faiss-cpu`)
- **What**: Facebook AI Similarity Search — a vector database library
- **Where**: `memory/vector_store.py`
- **Why**: Extremely fast similarity search even with millions of vectors, runs fully locally
- **What it does here**:
  - Takes text → converts to a 384-dimension number array (vector)
  - Stores all vectors in an index
  - When you ask a question, converts it to a vector and finds the closest stored vectors
  - Returns the most semantically similar past memories

```
"Who is the best salesperson?"
    ↓ embed
[0.23, -0.11, 0.87, ...] (384 numbers)
    ↓ search FAISS index
closest match → "Dave is top salesperson with $20,305"
```

### 8. **Sentence Transformers** (`sentence-transformers`)
- **What**: Library that converts text into dense vector embeddings
- **Where**: `memory/vector_store.py` — `SentenceTransformer("all-MiniLM-L6-v2")`
- **Why**: Turns words into numbers that capture *meaning*, not just keywords
- **Model used**: `all-MiniLM-L6-v2` — small (80MB), fast, 384 dimensions
- **What it does here**: Every fact/conversation is converted to a 384-dim vector before storing in FAISS

```
"best salesperson"  →  [0.23, -0.11, 0.87 ...]
"top sales person"  →  [0.24, -0.10, 0.85 ...]  ← very close! same meaning
"laptop computer"   →  [0.91,  0.54, -0.3 ...]  ← far away, different meaning
```

### 9. **SQLite (Long-Term Memory)**
- **What**: Same SQLite, different purpose from Day 3
- **Where**: `memory/long_term_memory.py` → creates `memory/long_term.db`
- **Why**: Structured, queryable, survives restarts
- **What it does here**: Stores 3 tables:
  - `conversations` — every turn ever spoken
  - `facts` — distilled key facts extracted by Groq
  - `agent_outputs` — raw agent results for audit

### 10. **Pickle** (Python stdlib)
- **What**: Python's built-in object serialization
- **Where**: `memory/vector_store.py`
- **Why**: FAISS saves the index but not the metadata (original text). Pickle saves the metadata
- **What it does here**: Saves the list of stored texts to disk so you can read them back after restart

---

## Architecture Patterns Used

| Pattern | Where | What it means |
|---|---|---|
| **Planner–Executor–Validator** | Day 3 orchestrator | Separate planning from doing from checking |
| **Tool wrapping** | All 3 agents | Each tool exposed as a clean `agent(task) → dict` API |
| **Subprocess sandboxing** | CodeAgent | Generated code runs in isolation |
| **Sliding window** | SessionMemory | Keep only last N turns to avoid prompt overflow |
| **RAG** (Retrieval Augmented Generation) | Day 4 full flow | Retrieve relevant memory → inject into prompt → generate |
| **3-layer memory** | Day 4 | Short-term + Long-term + Vector, each serving a different recall need |

---

## 🔑 The Big Picture

```
You type a question
        ↓
Groq (Llama 3.3) decides what to do     ← the brain
        ↓
Agents use tools to get real data        ← the hands
  • Python (pandas) for computation
  • SQLite for structured queries
  • File I/O for reading/writing
        ↓
Results stored in memory                 ← the memory
  • FAISS for "what's similar to this?"
  • SQLite for "what did I learn before?"
  • Session for "what did we just say?"
        ↓
Next question uses all that memory       ← gets smarter over time
```

This is the foundation of every production agentic AI system — tools + memory + LLM reasoning.
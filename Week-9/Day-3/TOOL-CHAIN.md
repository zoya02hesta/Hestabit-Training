# TOOL-CHAIN.md — Day 3: Tool-Calling Agents

> **Week 9 — Agentic AI & Multi-Agent System Design**
> Stack: AutoGen pattern | Groq (Llama-3 70B) | SQLite | Python

---

## Architecture Overview

```
User Request
     │
     ▼
┌─────────────┐
│   PLANNER   │  ← Groq decides which agents to invoke & in what order
│  (Groq LLM) │
└──────┬──────┘
       │  JSON plan: [{agent, instruction}, ...]
       ▼
┌─────────────┐
│  EXECUTOR   │  ← Dispatches tasks to specialist tool-agents
└──┬──┬──┬───┘
   │  │  │
   ▼  ▼  ▼
┌────┐ ┌────┐ ┌────┐
│FILE│ │CODE│ │ DB │   ← Three specialist agents (run in planned order)
│AGNT│ │AGNT│ │AGNT│
└────┘ └────┘ └────┘
   │     │      │
   └──┬──┘──────┘
      │  Agent outputs
      ▼
┌─────────────┐
│  VALIDATOR  │  ← Groq synthesises all outputs into final answer
│  (Groq LLM) │
└─────────────┘
      │
      ▼
 Final Answer  →  Console + data/final_report.txt
```

---

## Agents

### 1. File Agent (`tools/file_agent.py`)

| Capability | Details |
|---|---|
| **Read CSV** | Loads up to 50 rows, extracts column metadata |
| **Read TXT** | Full text read |
| **Analyse** | Sends content to Groq with a custom instruction |
| **Write / Append** | Saves text to .txt files |

**Actions:** `read` | `analyse` | `write` | `append`

```python
from tools.file_agent import file_agent

# Analyse a CSV
result = file_agent("analyse", "data/sales.csv",
                    instruction="What are the top 3 products by revenue?")
print(result["analysis"])

# Write a report
file_agent("write", "data/report.txt", write_content="# My Report\n...")
```

---

### 2. Code Agent (`tools/code_executor.py`)

| Capability | Details |
|---|---|
| **Code Gen** | Groq generates Python from plain English |
| **Safe Exec** | Runs in a temp file subprocess (30 s timeout) |
| **Data Path** | Injects `DATA_PATH` variable into every script |
| **Output** | Returns `stdout` + `stderr` + generated code |

```python
from tools.code_executor import code_agent

result = code_agent(
    task="Compute monthly revenue totals from the CSV and print them.",
    data_path="data/sales.csv"
)
print(result["stdout"])   # actual computation output
print(result["code"])     # see the generated code
```

---

### 3. DB Agent (`tools/db_agent.py`)

| Capability | Details |
|---|---|
| **NL → SQL** | Groq generates SELECT queries from English |
| **Safety** | Blocks INSERT / UPDATE / DELETE / DROP |
| **Summary** | Second Groq call turns rows into human insight |
| **DB** | SQLite at `data/sales.db` |

```python
from tools.db_agent import db_agent

result = db_agent("Which salesperson generated the most revenue?")
print(result["sql"])      # the generated SQL
print(result["rows"])     # raw query results
print(result["summary"])  # plain-English summary
```

---

### 4. Orchestrator (`orchestrator.py`)

The **Planner → Executor → Validator** pipeline.

```python
from orchestrator import orchestrate

answer = orchestrate(
    "Analyze sales.csv and generate top 5 insights about "
    "revenue, products, regions, and salesperson performance."
)
print(answer)
```

---

## Setup & Run

### 1. Install Dependencies
```bash
pip install groq pandas numpy
```

### 2. Set your Groq API Key
```bash
export GROQ_API_KEY="gsk_your_key_here"
```

### 3. Seed the Database
```bash
cd day3_tool_agents
python seed_db.py
```

### 4. Run Individual Agents
```bash
# File Agent
python tools/file_agent.py "What are the top products by revenue?"

# Code Agent
python tools/code_executor.py "Compute average order value per region"

# DB Agent
python tools/db_agent.py "Which region had the highest sales in January?"
```

### 5. Run the Full Orchestrator
```bash
# Default demo task
python orchestrator.py

# Custom task
python orchestrator.py "Find which salesperson underperformed in Q1 and suggest improvements"
```

---

## File Structure

```
day3_tool_agents/
├── data/
│   ├── sales.csv          ← Sample dataset (20 orders)
│   ├── sales.db           ← SQLite database (seeded from CSV)
│   ├── report.txt         ← Written by FileAgent demos
│   └── final_report.txt   ← Written by Orchestrator
├── tools/
│   ├── code_executor.py   ← Code Agent
│   ├── db_agent.py        ← DB Agent
│   └── file_agent.py      ← File Agent
├── orchestrator.py        ← Planner + Executor + Validator
├── seed_db.py             ← One-time DB setup
├── requirements.txt
└── TOOL-CHAIN.md          ← This file
```

---

## Key Design Patterns

| Pattern | Where Used |
|---|---|
| **Planner–Executor–Validator** | `orchestrator.py` — three-phase pipeline |
| **Tool Wrapping** | Each agent exposes a clean `agent(task) → dict` API |
| **Chain-of-Thought Isolation** | Each agent has its own system prompt & model call |
| **Safety Guards** | DB agent rejects non-SELECT SQL |
| **Subprocess Sandboxing** | Code agent runs generated code in isolated process |
| **Structured Output** | All agents return typed dicts for easy composition |

---

## Concepts Practised

- Python tool calling (Code Agent)
- Shell/subprocess execution (sandboxed)
- SQLite + NL→SQL querying (DB Agent)
- File read / write / analyse (File Agent)
- Planner → Executor → Validator orchestration
- Role-based system prompts
- Groq (Llama-3 70B) as the reasoning backbone

---

## Extension Ideas

| Idea | Hint |
|---|---|
| Add a **Search Agent** | Use DuckDuckGo API for local search |
| Add **FAISS memory** | Store agent results as embeddings for retrieval |
| Parallel execution | Run independent agents concurrently with `asyncio` |
| FastAPI wrapper | Expose `orchestrate()` as a REST endpoint |
| AutoGen integration | Replace manual orchestrator with `GroupChat` |

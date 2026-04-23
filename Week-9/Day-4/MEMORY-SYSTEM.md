# Memory Systems (Session + SQLite + Vector)

This document describes the three-layer memory architecture built for Day 4 of the Agentic AI curriculum. The system gives an agent the ability to remember context, persist facts across sessions, and recall semantically similar information on demand using the AutoGen framework.

## Architecture

1. **Short-Term Memory (Session)**: Managed via `SessionMemory`. It maintains a rolling window of recent turns and performs live fact extraction from each assistant response.
2. **Long-Term Memory (SQLite)**: Managed via `LongTermMemory`. It provides persistent storage for every conversation turn and distilled facts in a relational database (`long_term.db`).
3. **Vector Memory (FAISS)**: Managed via `VectorStore`. It handles semantic indexing and retrieval using vector embeddings (`faiss.index`).

## Unified Integration (NexusMemoryManager)

The `NexusMemoryManager` unifies these three layers into a single interface. It provides two primary methods:
- `recall(query)`: Searches semantic, factual, and session memory to build a context block.
- `store(query, response)`: Automatically persists the interaction and extracted facts across all layers.

## AutoGen Implementation

The system is implemented as an AutoGen `AssistantAgent` with custom hooks for RAG (Retrieval-Augmented Generation).

### Flow:
1. **User Input**: User sends a query via `UserProxyAgent`.
2. **Context Injection**: Before the assistant generates a reply, the system performs a semantic recall and injects the context into the agent's system message.
3. **Generation**: The agent generates a response using the LLM, enriched by past memories.
4. **Auto-Persistence**: The interaction is immediately stored in the SQLite database and FAISS index for future recall.

### Running the System
```bash
./venv/bin/python3 main_autogen.py
```

## Key Components

| Component | File | Purpose |
|---|---|---|
| **Session Memory** | `memory/session_memory.py` | Rolling window + Live fact extraction |
| **Vector Store** | `memory/vector_store.py` | FAISS-based semantic search |
| **Long-Term Memory** | `memory/long_term_memory.py` | SQLite-based persistent storage |
| **Memory Manager** | `nexus_memory_manager.py` | Unified management of all 3 layers |
| **AutoGen Entry** | `main_autogen.py` | Multi-agent RAG workflow |

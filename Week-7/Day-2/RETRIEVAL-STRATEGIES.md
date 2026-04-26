# Retrieval Strategy

## 1. Hybrid Search
We combine:
- BM25 (keyword matching)
- Embeddings (semantic search)

## 2. Reranking
We use Cross-Encoder to rank documents based on query relevance.

## 3. Deduplication
Duplicate chunks are removed to avoid redundant context.

## 4. Context Optimization
We limit context size to fit LLM input window.

## 5. Filters
We support filtering by metadata (year, type, etc.)
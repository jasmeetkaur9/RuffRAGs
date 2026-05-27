# RuffRAGs

A hybrid RAG agent built with LangGraph, FAISS, and BM25. Answers user queries from a local document store using a two-stage retrieval pipeline (keyword + semantic) and a stateful conversation agent.

## Architecture

- **Retrieval** — BM25 keyword search narrows a candidate set, then vector similarity re-ranks it (`HybridRet`)
- **Vector store** — FAISS with `BAAI/bge-large-en-v1.5` embeddings
- **LLM** — Ollama (`llama3.1`) via `ChatOllama`
- **Agent** — LangGraph agent with `InMemorySaver` checkpointing and per-session thread history
- **Docs** — plain text files in `docs/` with a `key: value` metadata header separated by `---`

## Setup

**1. Install uv**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Create environment and install dependencies**
```bash
uv sync
```

**3. Configure environment variables**
```bash
cp .env.example .env
# edit .env and add your OPENAI_API_KEY
```

**4. Pull the Ollama model**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3.1:8b
```

**5. Add documents to `docs/`**

Each file must follow this format:
```
title: My Document
author: Jane Doe
link: https://example.com/doc
---
Document content goes here...
```

**6. Run**
```bash
uv run python script.py
```

## Project Structure

```
RuffRAGs/
├── docs/            # Document knowledge base
├── threads/         # Persisted conversation histories (auto-created)
├── rag.py           # Agent, vectorstore, and chat logic
├── hybrid_ret.py    # BM25 + semantic hybrid retriever
├── script.py        # CLI entrypoint
└── pyproject.toml   # Dependencies
```

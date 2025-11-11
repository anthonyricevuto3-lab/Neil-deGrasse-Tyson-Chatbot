# Architecture

## Overview

NDT Bot is a RAG-powered chatbot that answers questions in the style of Neil deGrasse Tyson, grounded in his writings, interviews, and public statements.

## System Design

```
User Question
    ↓
[FastAPI Backend]
    ↓
[Guardrails] → Identity/Scope Check
    ↓
[RAG Pipeline]
    ├─ Embed Query
    ├─ FAISS Retrieval (top-k=10)
    ├─ Cross-Encoder Rerank (top-k=5)
    └─ Context Formatting
    ↓
[LLM Generation] → OpenAI GPT-4 + System Prompt
    ↓
[Response Validation] → Citations, Word Limit
    ↓
[Frontend Display] → React UI with Sources
```

## Components

### Backend (FastAPI)
- **Routers**: Chat, health, search endpoints
- **RAG Pipeline**: Ingest, retrieve, rerank, format
- **Services**: LLM wrapper, guardrails, telemetry
- **Models**: Pydantic schemas for type safety

### Vector Store (FAISS)
- Dense embeddings via `text-embedding-3-small`
- Attribution metadata per chunk
- Persistent disk storage

### Frontend (React + Vite)
- Real-time chat with SSE streaming
- Citation badges per message
- Source document links

## Data Flow

1. **Ingestion**: PDFs + HTML → Chunks → Embeddings → FAISS
2. **Query**: User input → Embed → Retrieve → Rerank → Format
3. **Generation**: Context + Prompt → LLM → Response
4. **Display**: Markdown + Citations → UI

## Security & Compliance

- No PII stored
- Rate limiting on API
- Content filtering via guardrails
- Source licensing tracked in `data/LICENSES/`

## Threat Model

- **Prompt injection**: Mitigated via system prompts and input validation
- **Data poisoning**: Curated, vetted sources only
- **Output hallucination**: Citations required per response

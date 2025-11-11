# High-Accuracy RAG Upgrade

This upgrade implements a citation-first, low-hallucination RAG pipeline for the NDT chatbot.

## What Changed

### 1. **Enhanced HTML Ingestion** (`backend/rag/ingest_html.py`)
- **Curated seed sources**: 13+ public interviews, essays, and transcripts
- **Attribution-first chunking**: Every chunk preserves URL, title, and domain
- **Boilerplate removal**: Uses `trafilatura` for clean text extraction
- **Quality filtering**: Skips pages with <400 characters

### 2. **BGE Reranker** (`backend/rag/rerank.py`)
- Upgraded from `ms-marco-MiniLM-L-6-v2` to **BAAI/bge-reranker-large**
- Retrieves 20 documents → reranks → keeps top 5
- Significant accuracy improvement for complex science questions

### 3. **Strict Citation Template** (`backend/prompts.py`)
- **Forces inline quotes**: ≤20 words in "quotes"
- **Mandates [source: ...] citations**: Every paragraph must cite
- **180-word limit**: Down from 300 for conciseness
- **Identity disclaimer**: "AI inspired by NDT" (not impersonation)

### 4. **Enhanced Safety Rails** (`backend/services/guardrails.py`)
- **Fast keyword check**: Science topics get instant approval
- **LLM fallback**: For ambiguous questions
- **Validation**: Checks for [source: ...] format and quoted snippets

### 5. **Better Context Formatting** (`backend/rag/context.py`)
- Includes **titles** alongside URLs for cleaner citations
- Format: `[Title] content [Source: URL]`
- Helps LLM generate readable citations like `[source: PBS NOVA]`

### 6. **Quality Evaluation** (`eval/check_quality.py`)
- Validates:
  - ✅ Proper `[source: ...]` citations
  - ✅ Citations from allowed domains (PBS, Natural History, etc.)
  - ✅ Quoted snippets present
  - ✅ Word count ≤180
- Pass rate threshold: 80%

## Quick Start

### Option 1: Automated Setup

**Windows (PowerShell):**
```powershell
.\scripts\setup_rag.ps1
```

**Linux/Mac (Bash):**
```bash
bash scripts/setup_rag.sh
```

### Option 2: Manual Steps

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ingest HTML sources (uses built-in seed URLs)
python backend/rag/ingest_html.py

# 3. (Optional) Ingest PDFs if you have documents
python backend/rag/ingest_pdf.py --input-dir data/docs --output-dir storage/vector_store

# 4. Start backend
uvicorn backend.app:app --reload --port 8000

# 5. Test
curl -X POST localhost:8000/api/chat -H "content-type: application/json" \
  -d "{\"message\":\"Why do we say we are made of stardust?\"}"

# 6. Run evaluation
python eval/check_quality.py
```

## Seed Sources

The HTML ingestion uses these curated public sources:

1. **PBS NOVA**: Interviews and transcripts (Origins series)
2. **Natural History Magazine**: Universe column essays
3. **Neil deGrasse Tyson site**: Personal essays
4. **StarTalk**: Episode pages and transcripts
5. **Podcast transcripts**: Tim Ferriss, SmartLess, Joe Rogan
6. **AMNH**: Events, courses, and debates

All sources are public and scraping respects `robots.txt`.

## Expected Output Format

Example response:
```
The phrase "we are made of stardust" refers to the fact that 
heavy elements in our bodies were forged in stellar cores. 
As NDT often explains, "the atoms of our bodies are traceable 
to stars that manufactured them in their cores and exploded 
these enriched ingredients across our galaxy" [source: PBS NOVA].

Key quotes:
• "We are not figuratively, but literally stardust" [source: Natural History Magazine]
• "Every atom in your body came from a star that exploded" [source: StarTalk]

Bottom line: Stellar nucleosynthesis is the cosmic origin of the 
elements that comprise all life [source: AMNH].
```

## Validation Checks

Run `python eval/check_quality.py` to check:
- ✅ Citations in `[source: ...]` format
- ✅ Citations from allowed domains
- ✅ Quoted snippets (≤20 words)
- ✅ Response ≤180 words
- ✅ Pass rate ≥80%

## Configuration

Key settings in `.env`:
```bash
# Retrieval
TOP_K=10              # Dense retrieval (actually uses 20 internally)
RERANK_TOP_K=5        # Final documents after reranking

# Response
MAX_RESPONSE_WORDS=180

# Models
EMBED_MODEL=text-embedding-3-large  # For better embeddings
LLM_MODEL=gpt-4                     # For accurate generation
```

## Troubleshooting

**Q: Getting "Import FlagEmbedding could not be resolved"**  
A: Run `pip install FlagEmbedding`

**Q: HTML ingestion returns no content**  
A: Some URLs may have changed. Check `data/cache/` for cached HTML or update seed URLs.

**Q: Citations missing from responses**  
A: Verify vector store has data (`storage/vector_store/`) and run ingestion again.

**Q: Pass rate <80%**  
A: Check if ingestion succeeded and vector store is populated. Also verify `.env` has valid `OPENAI_API_KEY`.

## Next Steps

1. **Add more sources**: Update `SEED_URLS` in `backend/rag/ingest_html.py`
2. **Tune retrieval**: Adjust `TOP_K` and `RERANK_TOP_K` in settings
3. **Custom evaluation**: Add questions to `eval/seed.jsonl`
4. **Monitor quality**: Run `check_quality.py` after each deployment

## Architecture

```
Query → Dense Retrieval (20 docs) 
      → BGE Reranking (top 5)
      → Context Formatting (with titles)
      → LLM Generation (strict template)
      → Citation Validation
      → Response
```

## Dependencies Added

- `FlagEmbedding==1.2.10` - BGE reranker
- `trafilatura==1.6.2` - HTML extraction (already in requirements)
- `beautifulsoup4==4.12.2` - HTML parsing (already in requirements)
- `sentence-transformers==2.2.2` - CrossEncoder base (already in requirements)

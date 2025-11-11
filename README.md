# Neil deGrasse Tyson ChatBot

An AI-powered chatbot that answers questions in the style of Neil deGrasse Tyson, backed by his writings, interviews, and public statements.

## Features

- **RAG-based responses**: Retrieves relevant context from curated sources
- **Citation-backed answers**: All responses include source citations
- **Guardrails**: Stays in character and scope
- **Modern stack**: FastAPI backend, React frontend, FAISS vector store

## Quick Start

```bash
# Bootstrap environment
make dev

# Ingest data sources
make ingest

# Run locally
make run

# Run tests
make test
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Data Sources](docs/DATA_SOURCES.md)
- [Evaluation Guide](docs/EVAL_GUIDE.md)
- [Prompt Guide](docs/PROMPT_GUIDE.md)

## License

See [LICENSE](LICENSE) for details.

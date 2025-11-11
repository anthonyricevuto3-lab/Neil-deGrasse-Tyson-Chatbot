#!/bin/bash
set -e

echo "📚 Starting data ingestion..."

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Ingest PDFs
echo "Ingesting PDF documents..."
python -m backend.rag.ingest_pdf \
    --input-dir data/docs \
    --output-dir storage/vector_store

# Ingest HTML from URLs
echo "Ingesting web content..."
python -m backend.rag.ingest_html \
    --urls-file data/urls/seed_urls.txt \
    --cache-dir data/cache \
    --output-dir storage/vector_store

# Export index for artifact storage
echo "Exporting index..."
python scripts/export_index.py --action pack

echo "✅ Ingestion complete!"

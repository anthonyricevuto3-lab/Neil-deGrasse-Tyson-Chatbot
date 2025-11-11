#!/usr/bin/env bash
# Quick setup script for high-accuracy RAG upgrade

set -e

echo "=================================================="
echo "NDT Bot - High-Accuracy RAG Setup"
echo "=================================================="

# 1. Install dependencies
echo ""
echo "[1/5] Installing dependencies..."
pip install -r requirements.txt

# 2. Ingest HTML sources
echo ""
echo "[2/5] Ingesting HTML sources (seed URLs)..."
python backend/rag/ingest_html.py

# 3. Optional: Re-ingest PDFs if you have new docs
if [ -d "data/docs" ] && [ "$(ls -A data/docs)" ]; then
    echo ""
    echo "[3/5] Ingesting PDF documents..."
    python backend/rag/ingest_pdf.py --input-dir data/docs --output-dir storage/vector_store
else
    echo ""
    echo "[3/5] Skipping PDF ingestion (no docs found in data/docs)"
fi

# 4. Start backend
echo ""
echo "[4/5] Starting backend server..."
echo "Backend will be available at http://localhost:8000"
echo ""
echo "To test, run:"
echo "  curl -X POST localhost:8000/api/chat -H 'content-type: application/json' \\"
echo "    -d '{\"message\":\"Why do we say we are made of stardust?\"}'"
echo ""

# Don't start automatically - let user do it
echo "[5/5] Ready to start!"
echo ""
echo "Next steps:"
echo "  1. Start backend:  uvicorn backend.app:app --reload --port 8000"
echo "  2. Test endpoint:  curl -X POST localhost:8000/api/chat -H 'content-type: application/json' -d '{\"message\":\"Why are we made of stardust?\"}'"
echo "  3. Run evaluation: python eval/check_quality.py"
echo ""
echo "✅ Setup complete!"

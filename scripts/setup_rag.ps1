# Quick setup script for high-accuracy RAG upgrade
# PowerShell version

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "NDT Bot - High-Accuracy RAG Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Install dependencies
Write-Host ""
Write-Host "[1/5] Installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# 2. Ingest HTML sources
Write-Host ""
Write-Host "[2/5] Ingesting HTML sources (seed URLs)..." -ForegroundColor Green
python backend/rag/ingest_html.py

# 3. Optional: Re-ingest PDFs if you have new docs
if (Test-Path "data/docs" -PathType Container) {
    $files = Get-ChildItem "data/docs" -File
    if ($files.Count -gt 0) {
        Write-Host ""
        Write-Host "[3/5] Ingesting PDF documents..." -ForegroundColor Green
        python backend/rag/ingest_pdf.py --input-dir data/docs --output-dir storage/vector_store
    } else {
        Write-Host ""
        Write-Host "[3/5] Skipping PDF ingestion (no docs found in data/docs)" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "[3/5] Skipping PDF ingestion (data/docs not found)" -ForegroundColor Yellow
}

# 4. Instructions
Write-Host ""
Write-Host "[4/5] Backend ready to start..." -ForegroundColor Green
Write-Host "Backend will be available at http://localhost:8000"
Write-Host ""
Write-Host "To test, run:" -ForegroundColor Yellow
Write-Host '  curl -X POST localhost:8000/api/chat -H "content-type: application/json" \' -ForegroundColor White
Write-Host '    -d "{\"message\":\"Why do we say we are made of stardust?\"}"' -ForegroundColor White
Write-Host ""

# 5. Final steps
Write-Host "[5/5] Ready to start!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Start backend:  uvicorn backend.app:app --reload --port 8000" -ForegroundColor White
Write-Host "  2. Test endpoint:  curl -X POST localhost:8000/api/chat -H 'content-type: application/json' -d '{`"message`":`"Why are we made of stardust?`"}'" -ForegroundColor White
Write-Host "  3. Run evaluation: python eval/check_quality.py" -ForegroundColor White
Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green

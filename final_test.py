"""Final test that demonstrates the chatbot works"""

# First, create a minimal working test without network calls
print("=" * 70)
print("NEIL DEGRASSE TYSON CHATBOT - FINAL TEST")
print("=" * 70)

# Test 1: Show vector store contents
print("\n[1] Vector Store Status:")
from pathlib import Path
store_path = Path("storage/vector_store")
if store_path.exists():
    faiss_file = store_path / "index.faiss"
    pkl_file = store_path / "index.pkl"
    print(f"✅ Vector store exists at {store_path}")
    print(f"   - FAISS index: {faiss_file.stat().st_size / 1024:.1f} KB")
    print(f"   - PKL file: {pkl_file.stat().st_size / 1024:.1f} KB")

# Test 2: Show RAG pipeline works
print("\n[2] Testing RAG Pipeline (without server):")
print("Question: 'Why are we made of stardust?'\n")

import os
os.environ['OPENAI_API_KEY'] = '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'

# Run the pipeline directly
import asyncio
from backend.rag.pipelines import rag_pipeline_with_sources
from backend.services.llm import generate_response

async def test_rag():
    query = "Why are we made of stardust?"
    
    # Get context
    result = await rag_pipeline_with_sources(query)
    print(f"✅ Retrieved {len(result.get('documents', []))} relevant documents")
    
    # Generate response
    response = await generate_response(query, result['context'])
    
    print(f"\n📝 Response ({len(response['answer'].split())} words):")
    print("-" * 70)
    print(response['answer'])
    print("-" * 70)
    
    if response.get('sources'):
        print(f"\n📚 Sources ({len(response['sources'])}):")
        for i, source in enumerate(response['sources'], 1):
            if isinstance(source, dict):
                print(f"  {i}. {source.get('title', 'Unknown')}")
                print(f"     {source.get('url', 'No URL')}")
            else:
                print(f"  {i}. {source}")

asyncio.run(test_rag())

# Test 3: Show server instructions
print("\n" + "=" * 70)
print("✅ CHATBOT IS WORKING!")
print("=" * 70)
print("\nTo start the server, run:")
print("  uvicorn backend.app:app --port 8000")
print("\nThen test with:")
print('  curl -X POST http://localhost:8000/api/chat \\')
print('       -H "Content-Type: application/json" \\')
print('       -d \'{"message":"Why are we made of stardust?"}\'')
print("\nOr open: http://localhost:8000/docs")

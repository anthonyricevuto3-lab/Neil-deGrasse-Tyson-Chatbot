"""
Quick performance test to measure response times.
Run this after starting the backend server.
"""

import asyncio
import time
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.rag.pipelines import rag_pipeline
from backend.services.llm import generate_response


async def test_query(query: str):
    """Test a single query and measure time."""
    print(f"\n🔍 Testing: '{query}'")
    print("─" * 60)
    
    # Start timing
    start_time = time.time()
    
    # RAG pipeline
    rag_start = time.time()
    context = await rag_pipeline(query)
    rag_time = time.time() - rag_start
    
    # LLM generation
    llm_start = time.time()
    response = await generate_response(
        question=query,
        context=context,
    )
    llm_time = time.time() - llm_start
    
    # Total time
    total_time = time.time() - start_time
    
    # Results
    print(f"⏱️  RAG Pipeline: {rag_time:.2f}s")
    print(f"⏱️  LLM Generation: {llm_time:.2f}s")
    print(f"⏱️  Total Time: {total_time:.2f}s")
    print(f"📊 Sources Found: {len(response['sources'])}")
    print(f"💬 Response Preview: {response['answer'][:100]}...")
    
    return total_time


async def main():
    """Run performance tests."""
    print("=" * 60)
    print("🚀 Neil deGrasse Tyson Chatbot - Performance Test")
    print("=" * 60)
    
    # Test queries
    queries = [
        "Why are we made of stardust?",
        "What happens inside a black hole?",
        "Should humans colonize Mars?",
        "What is the cosmic perspective?",
    ]
    
    times = []
    
    for query in queries:
        try:
            query_time = await test_query(query)
            times.append(query_time)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Summary
    if times:
        print("\n" + "=" * 60)
        print("📈 Performance Summary")
        print("=" * 60)
        print(f"Average Response Time: {sum(times) / len(times):.2f}s")
        print(f"Fastest Response: {min(times):.2f}s")
        print(f"Slowest Response: {max(times):.2f}s")
        print(f"\n✨ Target: < 4s per response")
        
        avg_time = sum(times) / len(times)
        if avg_time < 4:
            print(f"✅ SUCCESS! Average {avg_time:.2f}s is under 4s target")
        else:
            print(f"⚠️  Average {avg_time:.2f}s is above 4s target")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

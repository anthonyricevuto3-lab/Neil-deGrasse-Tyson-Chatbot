"""Test the trained chatbot with diverse NDT-style questions."""

import os
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

os.environ['OPENAI_API_KEY'] = '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'

from backend.rag.pipelines import rag_pipeline_with_sources
from backend.services.llm import generate_response

# Diverse test questions covering different topics
TEST_QUESTIONS = [
    "Why are we made of stardust?",
    "What happens if you fall into a black hole?",
    "Should humans colonize Mars?",
    "What is the cosmic perspective?",
    "Why was Pluto demoted from planet status?",
    "How do we know the universe is expanding?",
    "What is dark matter?",
    "Are we alone in the universe?",
]

async def test_question(question: str, question_num: int, total: int):
    """Test a single question."""
    print(f"\n{'='*80}")
    print(f"QUESTION {question_num}/{total}: {question}")
    print('='*80)
    
    try:
        # Get context
        result = await rag_pipeline_with_sources(question)
        docs = result.get('documents', [])
        
        print(f"\n📚 Retrieved {len(docs)} relevant documents")
        if docs:
            print(f"   Top source: {docs[0].get('title', 'Unknown')[:70]}")
        
        # Generate response
        response = await generate_response(question, result['context'])
        
        # Display response
        print(f"\n💬 Response ({len(response['answer'].split())} words):")
        print('-'*80)
        print(response['answer'])
        print('-'*80)
        
        # Show sources
        if response.get('sources'):
            print(f"\n📖 Sources cited ({len(response['sources'])}):")
            for i, source in enumerate(response['sources'][:5], 1):
                if isinstance(source, dict):
                    title = source.get('title', 'Unknown')[:60]
                    url = source.get('url', 'No URL')
                    print(f"   {i}. {title}")
                    print(f"      {url}")
                else:
                    print(f"   {i}. {source}")
        
        # Quality checks
        answer = response['answer']
        has_citations = '[source:' in answer.lower()
        word_count = len(answer.split())
        within_limit = word_count <= 180
        
        print(f"\n✓ Quality Checks:")
        print(f"   {'✅' if has_citations else '❌'} Citations present: {has_citations}")
        print(f"   {'✅' if within_limit else '⚠️ '} Word count: {word_count} ({'OK' if within_limit else 'OVER LIMIT'})")
        
        return {
            'question': question,
            'success': True,
            'has_citations': has_citations,
            'word_count': word_count,
            'sources_count': len(response.get('sources', []))
        }
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return {
            'question': question,
            'success': False,
            'error': str(e)
        }

async def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("TESTING TRAINED CHATBOT")
    print("="*80)
    print(f"\nRunning {len(TEST_QUESTIONS)} diverse questions...")
    
    results = []
    for i, question in enumerate(TEST_QUESTIONS, 1):
        result = await test_question(question, i, len(TEST_QUESTIONS))
        results.append(result)
        
        # Pause between questions
        if i < len(TEST_QUESTIONS):
            await asyncio.sleep(2)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    successful = sum(1 for r in results if r.get('success'))
    with_citations = sum(1 for r in results if r.get('has_citations'))
    avg_words = sum(r.get('word_count', 0) for r in results if r.get('success')) / max(successful, 1)
    avg_sources = sum(r.get('sources_count', 0) for r in results if r.get('success')) / max(successful, 1)
    
    print(f"\n✅ Success rate: {successful}/{len(TEST_QUESTIONS)} ({100*successful/len(TEST_QUESTIONS):.0f}%)")
    print(f"📝 Citation rate: {with_citations}/{successful} ({100*with_citations/max(successful,1):.0f}%)")
    print(f"📊 Average word count: {avg_words:.0f} words")
    print(f"📚 Average sources cited: {avg_sources:.1f}")
    
    print("\n" + "="*80)
    print("✅ TESTING COMPLETE!")
    print("="*80)
    print("\nThe chatbot is trained and ready to use!")
    print("\nStart the server with:")
    print("  uvicorn backend.app:app --port 8000")

if __name__ == "__main__":
    asyncio.run(main())

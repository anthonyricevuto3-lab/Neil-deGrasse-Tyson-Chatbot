"""Quality evaluation harness for citation and format validation."""

import asyncio
import json
from pathlib import Path
from typing import List, Dict

from backend.routers.chat import chat_endpoint
from backend.models.schemas import ChatRequest


ALLOWED_DOMAINS = [
    "pbs.org",
    "naturalhistorymag.com",
    "neildegrassetyson.com",
    "startalkmedia.com",
    "podscribe.com",
    "tim.blog",
    "happyscribe.com",
    "singjupost.com",
    "amnh.org",
]


def check_citation_format(response: str) -> Dict[str, any]:
    """
    Check if response has proper [source: ...] citations.
    
    Returns dict with validation results.
    """
    has_citation = "[source:" in response.lower()
    
    # Extract citations
    citations = []
    lines = response.lower().split("\n")
    for line in lines:
        if "[source:" in line:
            citations.append(line.strip())
    
    # Check if citations are from allowed domains
    valid_domain = False
    for citation in citations:
        for domain in ALLOWED_DOMAINS:
            if domain in citation:
                valid_domain = True
                break
    
    return {
        "has_citation": has_citation,
        "citation_count": len(citations),
        "valid_domain": valid_domain,
        "citations": citations,
    }


def check_quote_format(response: str) -> Dict[str, any]:
    """
    Check if response includes short quoted snippets.
    
    Returns dict with validation results.
    """
    quote_count = response.count('"') // 2  # Pairs of quotes
    has_quotes = quote_count > 0
    
    # Extract quotes (simple approach)
    quotes = []
    parts = response.split('"')
    for i in range(1, len(parts), 2):
        if i < len(parts):
            quotes.append(parts[i])
    
    # Check quote length (should be ≤20 words)
    long_quotes = []
    for quote in quotes:
        word_count = len(quote.split())
        if word_count > 20:
            long_quotes.append(f"{quote[:50]}... ({word_count} words)")
    
    return {
        "has_quotes": has_quotes,
        "quote_count": quote_count,
        "long_quotes": long_quotes,
        "quotes": quotes,
    }


def check_word_count(response: str, max_words: int = 180) -> Dict[str, any]:
    """Check if response is within word limit."""
    words = response.split()
    word_count = len(words)
    within_limit = word_count <= max_words
    
    return {
        "word_count": word_count,
        "within_limit": within_limit,
        "max_words": max_words,
    }


async def evaluate_response(question: str) -> Dict[str, any]:
    """
    Evaluate a single question-response pair.
    
    Returns dict with all quality checks.
    """
    # Get response
    request = ChatRequest(message=question)
    try:
        response_obj = await chat_endpoint(request)
        response = response_obj.response
    except Exception as e:
        return {
            "question": question,
            "error": str(e),
            "passed": False,
        }
    
    # Run checks
    citation_check = check_citation_format(response)
    quote_check = check_quote_format(response)
    word_check = check_word_count(response)
    
    # Determine if passed
    passed = (
        citation_check["has_citation"]
        and citation_check["valid_domain"]
        and word_check["within_limit"]
        and quote_check["has_quotes"]
    )
    
    return {
        "question": question,
        "response": response,
        "passed": passed,
        "citation_check": citation_check,
        "quote_check": quote_check,
        "word_check": word_check,
    }


async def run_evaluation(questions: List[str]) -> Dict[str, any]:
    """
    Run evaluation on a list of questions.
    
    Returns aggregate results and per-question details.
    """
    results = []
    
    for question in questions:
        print(f"\nEvaluating: {question}")
        result = await evaluate_response(question)
        results.append(result)
        
        # Print summary
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{status}")
        
        if not result["passed"]:
            if not result.get("citation_check", {}).get("has_citation"):
                print("  - Missing citations")
            if not result.get("citation_check", {}).get("valid_domain"):
                print("  - Citations not from allowed domains")
            if not result.get("word_check", {}).get("within_limit"):
                wc = result.get("word_check", {}).get("word_count", 0)
                print(f"  - Too long ({wc} words)")
            if not result.get("quote_check", {}).get("has_quotes"):
                print("  - Missing quoted snippets")
    
    # Aggregate stats
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    pass_rate = passed_count / total_count if total_count > 0 else 0
    
    return {
        "pass_rate": pass_rate,
        "passed": passed_count,
        "total": total_count,
        "results": results,
    }


async def main():
    """Run evaluation with seed questions."""
    
    # Load seed questions from eval/seed.jsonl if available
    seed_file = Path("eval/seed.jsonl")
    questions = []
    
    if seed_file.exists():
        print(f"Loading questions from {seed_file}...")
        with open(seed_file) as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    questions.append(item["question"])
    else:
        # Default test questions
        print("Using default test questions...")
        questions = [
            "Why do we say we are made of stardust?",
            "What is a black hole?",
            "How did the universe begin?",
            "What is dark matter?",
            "Why is Pluto no longer a planet?",
        ]
    
    print(f"\n{'='*60}")
    print(f"Running evaluation on {len(questions)} questions")
    print(f"{'='*60}")
    
    results = await run_evaluation(questions)
    
    print(f"\n{'='*60}")
    print(f"EVALUATION RESULTS")
    print(f"{'='*60}")
    print(f"Pass Rate: {results['pass_rate']:.1%} ({results['passed']}/{results['total']})")
    
    # Save results
    output_file = Path("eval/quality_check_results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to {output_file}")
    
    # Exit with error if pass rate too low
    if results['pass_rate'] < 0.8:
        print("\n⚠️  WARNING: Pass rate below 80%")
        exit(1)
    else:
        print("\n✅ Evaluation passed!")
        exit(0)


if __name__ == "__main__":
    asyncio.run(main())

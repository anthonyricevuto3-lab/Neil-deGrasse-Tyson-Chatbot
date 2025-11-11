#!/usr/bin/env python3
"""Run evaluation suite against the chatbot."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import yaml
from backend.routers.chat import chat_endpoint
from backend.models.schemas import ChatRequest


def load_seed_data(seed_file: Path) -> List[Dict[str, Any]]:
    """Load evaluation questions from JSONL."""
    questions = []
    with open(seed_file) as f:
        for line in f:
            questions.append(json.loads(line))
    return questions


def load_rubric(rubric_file: Path) -> Dict[str, Any]:
    """Load evaluation rubric."""
    with open(rubric_file) as f:
        return yaml.safe_load(f)


def check_citation(response: str) -> bool:
    """Check if response contains citations."""
    citation_markers = ["Source:", "[", "*"]
    return any(marker in response for marker in citation_markers)


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def evaluate_response(
    response: str, expected: Dict[str, Any], rubric: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate a single response against rubric."""
    results = {
        "citation_required": check_citation(response),
        "word_limit": count_words(response) <= rubric["rules"]["word_limit"]["max_words"],
        "response": response,
        "word_count": count_words(response),
    }
    return results


async def run_evaluation(
    seed_file: Path, rubric_file: Path, output_file: Path
) -> None:
    """Run full evaluation suite."""
    questions = load_seed_data(seed_file)
    rubric = load_rubric(rubric_file)
    
    results = []
    for item in questions:
        print(f"Evaluating: {item['question']}")
        
        # Get chatbot response
        request = ChatRequest(message=item["question"])
        response = await chat_endpoint(request)
        
        # Evaluate
        eval_result = evaluate_response(
            response.response, item, rubric
        )
        eval_result["question"] = item["question"]
        eval_result["expected"] = item
        
        results.append(eval_result)
    
    # Compute aggregate metrics
    total = len(results)
    passed = sum(
        1 for r in results 
        if r["citation_required"] and r["word_limit"]
    )
    
    summary = {
        "total_questions": total,
        "passed": passed,
        "accuracy": passed / total if total > 0 else 0,
        "citation_rate": sum(1 for r in results if r["citation_required"]) / total,
        "avg_word_count": sum(r["word_count"] for r in results) / total,
        "results": results,
    }
    
    # Save results
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Evaluation complete!")
    print(f"Accuracy: {summary['accuracy']:.2%}")
    print(f"Citation Rate: {summary['citation_rate']:.2%}")
    print(f"Avg Word Count: {summary['avg_word_count']:.1f}")
    print(f"Results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Run evaluation suite")
    parser.add_argument(
        "--seed-file",
        type=Path,
        default=Path("eval/seed.jsonl"),
        help="Path to seed questions",
    )
    parser.add_argument(
        "--rubric-file",
        type=Path,
        default=Path("eval/rubric.yaml"),
        help="Path to evaluation rubric",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("eval/results.json"),
        help="Output file for results",
    )
    
    args = parser.parse_args()
    
    import asyncio
    asyncio.run(run_evaluation(args.seed_file, args.rubric_file, args.output_file))


if __name__ == "__main__":
    main()

# Evaluation Guide

## Test Dataset

Located in `eval/seed.jsonl` - each line contains:
```json
{
  "question": "What is dark matter?",
  "expected_domains": ["astrophysics", "cosmology"],
  "expected_citations": ["Astrophysics for People in a Hurry"]
}
```

## Rubric (`eval/rubric.yaml`)

### Pass Criteria
1. **Citation presence**: Every response must include at least one citation
2. **Word limit**: Responses ≤ 300 words
3. **In-character**: Tone matches NDT's style
4. **Domain accuracy**: Citations match expected domains

### Fail Criteria
- Hallucinated citations (sources not in index)
- Off-topic responses
- Refusal to answer in-scope questions

## Running Evaluations

```bash
make eval
```

Outputs `eval/results.json` with:
- Pass/fail per question
- Aggregate metrics (accuracy, citation rate)
- Failed examples for inspection

## Metrics

- **Citation Rate**: % responses with valid citations
- **Accuracy**: % responses passing all rubric checks
- **Avg Response Length**: Mean word count
- **Retrieval Success**: % queries with relevant docs in top-k

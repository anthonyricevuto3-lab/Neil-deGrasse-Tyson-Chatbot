#!/bin/bash
set -e

echo "🧪 Running evaluation suite..."

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate

# Run evaluation
python eval/run_eval.py \
    --seed-file eval/seed.jsonl \
    --rubric-file eval/rubric.yaml \
    --output-file eval/results.json

echo "✅ Evaluation complete! Check eval/results.json for details."

.PHONY: dev ingest test run docker-build clean lint format

dev:
	bash scripts/bootstrap.sh

ingest:
	bash scripts/ingest_all.sh

test:
	pytest backend/tests/ -v --cov=backend --cov-report=html

run:
	uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -f docker/backend.Dockerfile -t ndt-bot-backend .
	docker build -f docker/frontend.Dockerfile -t ndt-bot-frontend ./frontend

lint:
	ruff check backend/
	black --check backend/
	isort --check-only backend/

format:
	black backend/
	isort backend/
	ruff check --fix backend/

eval:
	bash scripts/eval.sh

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage

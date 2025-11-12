"""Telemetry and logging."""

import json
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


def log_request(endpoint: str, data: dict[str, Any]) -> None:
    """Log API request (PII-safe)."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "data_summary": {
            "message_length": len(data.get("message", "")),
        },
    }
    logger.info(json.dumps(log_entry))


def log_response(endpoint: str, response: dict[str, Any], duration_ms: float) -> None:
    """Log API response (PII-safe)."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "duration_ms": duration_ms,
        "response_summary": {
            "answer_length": len(response.get("answer", "")),
            "num_sources": len(response.get("sources", [])),
        },
    }
    logger.info(json.dumps(log_entry))


def log_error(endpoint: str, error: Exception) -> None:
    """Log error."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "error": str(error),
        "error_type": type(error).__name__,
    }
    logger.error(json.dumps(log_entry))

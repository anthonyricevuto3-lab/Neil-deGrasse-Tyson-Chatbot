"""Time utilities."""

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Get current UTC time."""
    return datetime.now(UTC)


def timestamp_iso() -> str:
    """Get current timestamp in ISO format."""
    return utc_now().isoformat()

"""Time utilities."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC time."""
    return datetime.now(timezone.utc)


def timestamp_iso() -> str:
    """Get current timestamp in ISO format."""
    return utc_now().isoformat()

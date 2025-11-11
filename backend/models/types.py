"""Domain types and enums."""

from enum import Enum


class SourceType(str, Enum):
    """Type of source document."""
    BOOK = "book"
    INTERVIEW = "interview"
    ESSAY = "essay"
    LECTURE = "lecture"
    PODCAST = "podcast"
    OTHER = "other"


class TopicDomain(str, Enum):
    """Scientific domain."""
    ASTROPHYSICS = "astrophysics"
    COSMOLOGY = "cosmology"
    PHYSICS = "physics"
    ASTRONOMY = "astronomy"
    PLANETARY_SCIENCE = "planetary_science"
    PHILOSOPHY = "philosophy"
    SCIENCE_COMMUNICATION = "science_communication"
    OTHER = "other"

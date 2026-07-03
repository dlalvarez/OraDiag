"""Controlled enum values for OraDiag models."""

from __future__ import annotations

from enum import StrEnum


class ReviewStatus(StrEnum):
    OK = "OK"
    INFO = "INFO"
    WARNING = "WARNING"
    PROBLEM = "PROBLEM"
    CRITICAL = "CRITICAL"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"
    UNKNOWN = "UNKNOWN"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    BLOCKER = "blocker"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CausalDomain(StrEnum):
    OPERATING_SYSTEM = "operating_system"
    INFRASTRUCTURE = "infrastructure"
    STORAGE = "storage"
    DATABASE = "database"
    APPLICATION = "application"
    USER = "user"
    DATA = "data"
    UNDETERMINED = "undetermined"


class CausalRole(StrEnum):
    PRIMARY_CAUSE = "primary_cause"
    CONTRIBUTING_FACTOR = "contributing_factor"
    RELATED_FINDING = "related_finding"
    INCIDENTAL_FINDING = "incidental_finding"
    RULED_OUT = "ruled_out"
    NOT_EVALUATED = "not_evaluated"
    UNKNOWN = "unknown"


class SymptomCategory(StrEnum):
    CANNOT_CONNECT = "cannot_connect"
    CONNECTION_HANGS = "connection_hangs"
    ERRORS = "errors"
    SLOW_PERFORMANCE = "slow_performance"
    PARTIAL_IMPACT = "partial_impact"
    AVAILABILITY_DOWN = "availability_down"
    UNSPECIFIED = "unspecified"


class LimitationType(StrEnum):
    TIMEOUT = "timeout"
    ERROR = "error"
    INSUFFICIENT_PERMISSIONS = "insufficient_permissions"
    LAYER_UNAVAILABLE = "layer_unavailable"
    NOT_APPLICABLE = "not_applicable"
    INCOMPLETE_DATA = "incomplete_data"
    SKIPPED = "skipped"


class EvidencePolarity(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class OutputFormat(StrEnum):
    CONSOLE = "console"
    JSON = "json"

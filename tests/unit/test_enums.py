from oradiag.models import (
    CausalDomain,
    CausalRole,
    Confidence,
    EvidencePolarity,
    LimitationType,
    OutputFormat,
    ReviewStatus,
    Severity,
    SymptomCategory,
)


def test_review_status_values_match_contract() -> None:
    assert {item.value for item in ReviewStatus} == {
        "OK",
        "INFO",
        "WARNING",
        "PROBLEM",
        "CRITICAL",
        "TIMEOUT",
        "ERROR",
        "SKIPPED",
        "UNKNOWN",
    }


def test_level_and_format_values_match_contract() -> None:
    assert {item.value for item in Severity} == {"info", "warning", "critical", "blocker"}
    assert {item.value for item in Confidence} == {"low", "medium", "high"}
    assert {item.value for item in OutputFormat} == {"console", "json"}


def test_causal_values_match_constitution() -> None:
    assert {item.value for item in CausalRole} == {
        "primary_cause",
        "contributing_factor",
        "related_finding",
        "incidental_finding",
        "ruled_out",
        "not_evaluated",
        "unknown",
    }
    assert {item.value for item in CausalDomain} == {
        "operating_system",
        "infrastructure",
        "storage",
        "database",
        "application",
        "user",
        "data",
        "undetermined",
    }


def test_symptom_limitation_and_polarity_values_match_contract() -> None:
    assert {item.value for item in SymptomCategory} == {
        "cannot_connect",
        "connection_hangs",
        "errors",
        "slow_performance",
        "partial_impact",
        "availability_down",
        "unspecified",
    }
    assert {item.value for item in LimitationType} == {
        "timeout",
        "error",
        "insufficient_permissions",
        "layer_unavailable",
        "not_applicable",
        "incomplete_data",
        "skipped",
    }
    assert {item.value for item in EvidencePolarity} == {"positive", "negative", "neutral"}

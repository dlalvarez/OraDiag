from oradiag.models import CausalDomain, ReviewStatus, Severity, SymptomCategory
from oradiag.rca import RCAEngine
from tests.unit.test_rca_engine_primary_cause import limitation, observation, payload, review


def test_returns_undetermined_when_evidence_is_too_weak() -> None:
    weak = observation(
        "obs-weak",
        "network",
        CausalDomain.INFRASTRUCTURE,
        severity=Severity.WARNING,
        status=ReviewStatus.WARNING,
    )

    result = RCAEngine().evaluate(payload(observations=[weak], symptom=SymptomCategory.SLOW_PERFORMANCE))

    assert result.assessment.status == "undetermined"
    assert result.assessment.domain == "undetermined"
    assert result.assessment.confidence == "low"
    assert result.assessment.primary_cause_id is None
    assert result.insufficient_evidence is True


def test_returns_undetermined_on_competing_strong_domains() -> None:
    database = observation("obs-db", "locks", CausalDomain.DATABASE)
    storage = observation("obs-storage", "io", CausalDomain.STORAGE)

    result = RCAEngine().evaluate(
        payload(
            observations=[database, storage],
            reviews=[review("locks", observations=[database]), review("io", observations=[storage])],
            symptom=SymptomCategory.AVAILABILITY_DOWN,
        )
    )

    assert result.assessment.status == "undetermined"
    assert result.insufficient_evidence is True


def test_timeout_review_becomes_not_evaluated_limitation_in_undetermined_result() -> None:
    timeout = limitation()
    evidence = payload(
        reviews=[
            review(
                "sql_access",
                status=ReviewStatus.TIMEOUT,
                severity=Severity.WARNING,
                limitations=[timeout],
            )
        ],
        symptom=SymptomCategory.ERRORS,
    )

    result = RCAEngine().evaluate(evidence)

    assert result.assessment.status == "undetermined"
    assert result.limitations == [timeout]
    assert any(finding.role == "not_evaluated" for finding in result.findings)

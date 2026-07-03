from oradiag.models import CausalDomain, SymptomCategory
from oradiag.rca import RCAEngine
from tests.unit.test_rca_engine_primary_cause import observation, payload


def test_symptom_prioritizes_but_does_not_create_evidence() -> None:
    result = RCAEngine().evaluate(payload(observations=[], symptom=SymptomCategory.SLOW_PERFORMANCE))

    assert result.assessment.status == "undetermined"
    assert result.insufficient_evidence is True


def test_symptom_boost_prefers_related_domain_when_evidence_competes() -> None:
    database = observation("obs-db", "locks", CausalDomain.DATABASE)
    user = observation("obs-user", "user_access", CausalDomain.USER)

    result = RCAEngine().evaluate(
        payload(
            observations=[database, user],
            symptom=SymptomCategory.SLOW_PERFORMANCE,
        )
    )

    assert result.assessment.status == "determined"
    assert result.assessment.primary_cause_id == "finding-obs-db"
    assert result.assessment.domain == "database"


def test_unrelated_severe_finding_is_not_primary_just_because_symptom_exists() -> None:
    storage = observation(
        "obs-storage",
        "storage",
        CausalDomain.STORAGE,
        related_to_symptom=False,
    )

    result = RCAEngine().evaluate(payload(observations=[storage], symptom=SymptomCategory.SLOW_PERFORMANCE))

    assert result.assessment.status == "undetermined"
    assert any(finding.role == "incidental_finding" for finding in result.findings)

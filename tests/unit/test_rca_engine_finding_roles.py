from oradiag.models import CausalDomain, EvidencePolarity, ReviewStatus, Severity, SymptomCategory
from oradiag.rca import RCAEngine
from tests.unit.test_rca_engine_primary_cause import observation, payload, review


def test_classifies_related_incidental_and_ruled_out_findings() -> None:
    primary = observation("obs-lock", "locks", CausalDomain.DATABASE)
    related = observation(
        "obs-app",
        "application",
        CausalDomain.APPLICATION,
        severity=Severity.WARNING,
        status=ReviewStatus.WARNING,
        related_to_symptom=True,
    )
    incidental = observation(
        "obs-storage",
        "storage",
        CausalDomain.STORAGE,
        severity=Severity.CRITICAL,
        status=ReviewStatus.PROBLEM,
        related_to_symptom=False,
    )
    negative = observation(
        "obs-user-ok",
        "user_access",
        CausalDomain.USER,
        severity=Severity.INFO,
        status=ReviewStatus.OK,
        polarity=EvidencePolarity.NEGATIVE,
    )
    evidence = payload(
        observations=[primary, related, incidental, negative],
        reviews=[
            review("locks", observations=[primary]),
            review("storage", observations=[incidental]),
            review(
                "listener",
                status=ReviewStatus.OK,
                severity=Severity.INFO,
                ok_relevance="Descarta listener simulado como causa.",
            ),
        ],
        symptom=SymptomCategory.SLOW_PERFORMANCE,
    )

    result = RCAEngine().evaluate(evidence)
    roles_by_id = {finding.id: finding.role for finding in result.findings}

    assert roles_by_id["finding-obs-lock"] == "primary_cause"
    assert roles_by_id["finding-obs-app"] in {"related_finding", "contributing_factor"}
    assert roles_by_id["finding-obs-storage"] == "incidental_finding"
    assert roles_by_id["ruled-out-listener"] == "ruled_out"
    assert roles_by_id["ruled-out-obs-user-ok"] == "ruled_out"
    assert result.ok_reviews[0].check_id == "listener"

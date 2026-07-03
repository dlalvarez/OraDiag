from oradiag.models import CausalDomain, ReviewStatus, Severity, SymptomCategory
from oradiag.rca import RCAEngine
from tests.unit.test_rca_engine_primary_cause import limitation, observation, payload, review


def test_recommendations_include_primary_related_and_limitation_guidance() -> None:
    primary = observation("obs-lock", "locks", CausalDomain.DATABASE)
    related = observation(
        "obs-app",
        "application",
        CausalDomain.APPLICATION,
        severity=Severity.WARNING,
        status=ReviewStatus.WARNING,
        related_to_symptom=True,
    )
    timeout = limitation()
    evidence = payload(
        observations=[primary, related],
        reviews=[
            review("locks", observations=[primary]),
            review(
                "sql_access",
                status=ReviewStatus.TIMEOUT,
                severity=Severity.WARNING,
                limitations=[timeout],
            ),
        ],
        symptom=SymptomCategory.SLOW_PERFORMANCE,
    )

    result = RCAEngine().evaluate(evidence)
    recommendation_ids = {recommendation.id for recommendation in result.recommendations}

    assert f"rec-{result.assessment.primary_cause_id}" in recommendation_ids
    assert "rec-related-findings" in recommendation_ids
    assert "rec-limitations" in recommendation_ids
    assert all(recommendation.risk == "low" for recommendation in result.recommendations)
    assert all(recommendation.requires_human_validation for recommendation in result.recommendations)

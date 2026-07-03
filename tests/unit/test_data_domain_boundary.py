from oradiag.models import ReviewStatus, Severity, SymptomCategory
from oradiag.rca import RCAEngine
from tests.unit.test_rca_engine_primary_cause import payload, review


def test_data_domain_boundary_uses_ok_technical_reviews_without_business_data() -> None:
    evidence = payload(
        reviews=[
            review(
                "locks",
                status=ReviewStatus.OK,
                severity=Severity.INFO,
                ok_relevance="Descarta bloqueos simulados.",
            ),
            review(
                "storage_space",
                status=ReviewStatus.OK,
                severity=Severity.INFO,
                ok_relevance="Descarta presion de almacenamiento simulada.",
            ),
        ],
        symptom=SymptomCategory.ERRORS,
    )

    result = RCAEngine().evaluate(evidence)

    assert result.assessment.status == "determined"
    assert result.assessment.domain == "data"
    assert result.findings[0].id == "data-boundary"
    assert result.findings[0].role == "primary_cause"
    assert result.findings[0].evidence_ids == ["locks", "storage_space"]
    assert "tablas de negocio" in result.recommendations[0].description
    assert result.ok_reviews[0].check_id == "locks"
    assert result.ok_reviews[1].check_id == "storage_space"

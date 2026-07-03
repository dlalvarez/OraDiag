import pytest
from pydantic import ValidationError

from tests.unit.test_diagnostic_models import make_primary_finding, make_scenario
from oradiag.models import CausalAssessment, CausalDomain, Confidence, DiagnosticResult


def test_diagnostic_result_contract_required_top_level_fields() -> None:
    finding = make_primary_finding()
    result = DiagnosticResult(
        scenario=make_scenario(),
        assessment=CausalAssessment(
            status="determined",
            primary_cause_id=finding.id,
            domain=CausalDomain.DATABASE,
            confidence=Confidence.HIGH,
            reasoning="La evidencia soporta una causa probable.",
            evidence_ids=["obs-001"],
        ),
        findings=[finding],
    ).model_dump()

    assert set(result) == {
        "schema_version",
        "tool",
        "scenario",
        "assessment",
        "findings",
        "related_findings",
        "incidental_findings",
        "ok_reviews",
        "limitations",
        "recommendations",
        "insufficient_evidence",
    }


def test_diagnostic_result_contract_schema_version_is_fixed_for_phase_1() -> None:
    finding = make_primary_finding()
    result = DiagnosticResult(
        scenario=make_scenario(),
        assessment=CausalAssessment(
            status="determined",
            primary_cause_id=finding.id,
            domain=CausalDomain.DATABASE,
            confidence=Confidence.HIGH,
            reasoning="La evidencia soporta una causa probable.",
            evidence_ids=["obs-001"],
        ),
        findings=[finding],
    ).model_dump()
    result["schema_version"] = "2.0"

    with pytest.raises(ValidationError):
        DiagnosticResult.model_validate(result)


def test_diagnostic_result_contract_undetermined_requires_insufficient_evidence() -> None:
    result = {
        "schema_version": "1.0",
        "scenario": make_scenario().model_dump(),
        "assessment": {
            "status": "undetermined",
            "domain": "undetermined",
            "confidence": "low",
            "reasoning": "No hay evidencia suficiente.",
        },
        "insufficient_evidence": True,
    }

    parsed = DiagnosticResult.model_validate(result)

    assert parsed.assessment.status == "undetermined"
    assert parsed.insufficient_evidence is True
    assert parsed.findings == []

import json

import pytest
from pydantic import ValidationError

from oradiag.models import (
    CausalAssessment,
    CausalDomain,
    CausalRole,
    Confidence,
    DiagnosticFinding,
    DiagnosticResult,
    DiagnosticScenario,
    Recommendation,
    Severity,
    SymptomCategory,
)


def make_scenario() -> DiagnosticScenario:
    return DiagnosticScenario(
        id="slow-lock",
        name="Lentitud por bloqueo simulado",
        symptom=SymptomCategory.SLOW_PERFORMANCE,
        target_id="lab_orcl_01",
        profile="diag_all",
    )


def make_primary_finding() -> DiagnosticFinding:
    return DiagnosticFinding(
        id="finding-lock",
        title="Bloqueo simulado",
        description="La evidencia simulada apunta a contencion por bloqueo.",
        domain=CausalDomain.DATABASE,
        role=CausalRole.PRIMARY_CAUSE,
        severity=Severity.CRITICAL,
        confidence=Confidence.HIGH,
        evidence_ids=["obs-001"],
    )


def test_diagnostic_result_serializes_to_stable_json_shape() -> None:
    finding = make_primary_finding()
    result = DiagnosticResult(
        scenario=make_scenario(),
        assessment=CausalAssessment(
            status="determined",
            primary_cause_id=finding.id,
            domain=CausalDomain.DATABASE,
            confidence=Confidence.HIGH,
            reasoning="La evidencia simulada soporta bloqueo como causa probable.",
            evidence_ids=["obs-001"],
        ),
        findings=[finding],
        recommendations=[
            Recommendation(
                id="rec-001",
                title="Validar bloqueo",
                description="Revisar con el equipo DBA antes de actuar.",
                risk="low",
                requires_human_validation=True,
            )
        ],
    )

    data = json.loads(result.model_dump_json())

    assert data["schema_version"] == "1.0"
    assert data["assessment"]["status"] == "determined"
    assert data["assessment"]["domain"] == "database"
    assert data["findings"][0]["role"] == "primary_cause"
    assert data["insufficient_evidence"] is False


def test_primary_cause_requires_evidence_ids() -> None:
    with pytest.raises(ValidationError, match="primary cause findings require"):
        DiagnosticFinding(
            id="finding-lock",
            title="Bloqueo simulado",
            description="Sin evidencia no debe ser causa principal.",
            domain=CausalDomain.DATABASE,
            role=CausalRole.PRIMARY_CAUSE,
            severity=Severity.CRITICAL,
            confidence=Confidence.MEDIUM,
        )


def test_undetermined_assessment_requires_low_confidence_no_primary_and_domain_undetermined() -> None:
    with pytest.raises(ValidationError, match="must not have a primary cause"):
        CausalAssessment(
            status="undetermined",
            primary_cause_id="finding-any",
            domain=CausalDomain.UNDETERMINED,
            confidence=Confidence.LOW,
            reasoning="No hay evidencia suficiente.",
        )

    with pytest.raises(ValidationError, match="must have low confidence"):
        CausalAssessment(
            status="undetermined",
            domain=CausalDomain.UNDETERMINED,
            confidence=Confidence.MEDIUM,
            reasoning="No hay evidencia suficiente.",
        )

    with pytest.raises(ValidationError, match="must use the undetermined domain"):
        CausalAssessment(
            status="undetermined",
            domain=CausalDomain.DATABASE,
            confidence=Confidence.LOW,
            reasoning="No hay evidencia suficiente.",
        )


def test_undetermined_result_must_mark_insufficient_evidence() -> None:
    with pytest.raises(ValidationError, match="must mark insufficient_evidence"):
        DiagnosticResult(
            scenario=make_scenario(),
            assessment=CausalAssessment(
                status="undetermined",
                domain=CausalDomain.UNDETERMINED,
                confidence=Confidence.LOW,
                reasoning="No hay evidencia suficiente.",
            ),
        )

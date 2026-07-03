import json

import pytest
from pydantic import ValidationError

from oradiag.models import (
    AccessLayer,
    DiagnosticScenario,
    EvidencePayload,
    EvidencePolarity,
    EvidenceProviderMetadata,
    Limitation,
    LimitationType,
    Observation,
    ObservedSubject,
    ReviewResult,
    ReviewStatus,
    Severity,
    SymptomCategory,
    TargetContext,
)


def make_limitation() -> Limitation:
    return Limitation(
        id="lim-001",
        type=LimitationType.TIMEOUT,
        scope="database",
        message="La capa simulada no respondio a tiempo.",
        impact="Reduce la confianza del diagnostico.",
    )


def make_observation() -> Observation:
    return Observation(
        id="obs-001",
        check_id="locks",
        subject=ObservedSubject(kind="session", id="sid-10", attributes={"module": "batch"}),
        status=ReviewStatus.PROBLEM,
        severity=Severity.CRITICAL,
        polarity=EvidencePolarity.POSITIVE,
        message="Sesion simulada bloqueada.",
        structured_data={"wait_event": "enq: TX - row lock contention"},
    )


def make_payload() -> EvidencePayload:
    obs = make_observation()
    return EvidencePayload(
        scenario=DiagnosticScenario(
            id="slow-lock",
            name="Lentitud por bloqueo simulado",
            symptom=SymptomCategory.SLOW_PERFORMANCE,
            target_id="lab_orcl_01",
            profile="diag_all",
        ),
        target=TargetContext(
            target_id="lab_orcl_01",
            display_name="Laboratorio ORCL 01",
            environment="lab",
            metadata={"host_alias": "lab-db"},
        ),
        provider=EvidenceProviderMetadata(provider_type="fixture", provider_name="FixtureEvidenceProvider"),
        access_layers=[AccessLayer(name="database", available=True, status=ReviewStatus.OK)],
        observations=[obs],
        reviews=[
            ReviewResult(
                check_id="locks",
                title="Bloqueos simulados",
                status=ReviewStatus.PROBLEM,
                severity=Severity.CRITICAL,
                observations=[obs],
            )
        ],
    )


def test_evidence_payload_serializes_to_stable_json_shape() -> None:
    payload = make_payload()

    data = json.loads(payload.model_dump_json())

    assert data["schema_version"] == "1.0"
    assert data["scenario"]["symptom"] == "slow_performance"
    assert data["provider"]["provider_type"] == "fixture"
    assert data["reviews"][0]["status"] == "PROBLEM"
    assert data["observations"][0]["polarity"] == "positive"


def test_unavailable_access_layer_requires_limitation() -> None:
    with pytest.raises(ValidationError, match="unavailable access layers"):
        AccessLayer(name="database", available=False, status=ReviewStatus.ERROR)


def test_error_timeout_and_skipped_reviews_require_limitation() -> None:
    with pytest.raises(ValidationError, match="reviews require at least one limitation"):
        ReviewResult(
            check_id="sql_access",
            title="Acceso SQL simulado",
            status=ReviewStatus.TIMEOUT,
            severity=Severity.WARNING,
        )


def test_secret_like_target_metadata_is_rejected() -> None:
    with pytest.raises(ValidationError, match="must not contain secrets"):
        TargetContext(
            target_id="lab_orcl_01",
            display_name="Laboratorio",
            metadata={"password": "no-debe-existir"},
        )


def test_expected_output_is_not_allowed_in_evidence_payload() -> None:
    payload = make_payload().model_dump()
    payload["expected_output"] = {"assessment": "primary_cause"}

    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(payload)


def test_ok_review_can_preserve_relevance_as_negative_evidence() -> None:
    review = ReviewResult(
        check_id="storage_space",
        title="Espacio simulado",
        status=ReviewStatus.OK,
        severity=Severity.INFO,
        ok_relevance="Descarta presion de almacenamiento en el escenario.",
    )

    assert review.ok_relevance == "Descarta presion de almacenamiento en el escenario."

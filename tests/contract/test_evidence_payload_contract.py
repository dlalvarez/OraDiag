import pytest
from pydantic import ValidationError

from tests.unit.test_evidence_models import make_payload
from oradiag.models import EvidencePayload, ReviewStatus


def test_evidence_payload_contract_required_top_level_fields() -> None:
    payload = make_payload().model_dump()

    assert set(payload) == {
        "schema_version",
        "scenario",
        "target",
        "provider",
        "access_layers",
        "reviews",
        "observations",
        "limitations",
    }


def test_evidence_payload_contract_schema_version_is_fixed_for_phase_1() -> None:
    payload = make_payload().model_dump()
    payload["schema_version"] = "2.0"

    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(payload)


def test_evidence_payload_contract_rejects_non_fixture_provider_in_phase_1() -> None:
    payload = make_payload().model_dump()
    payload["provider"]["provider_type"] = "oracle"

    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(payload)


def test_evidence_payload_contract_uses_controlled_review_status_values() -> None:
    payload = make_payload().model_dump()
    payload["reviews"][0]["status"] = "BROKEN"

    with pytest.raises(ValidationError):
        EvidencePayload.model_validate(payload)

    payload["reviews"][0]["status"] = ReviewStatus.PROBLEM
    assert EvidencePayload.model_validate(payload).reviews[0].status == "PROBLEM"

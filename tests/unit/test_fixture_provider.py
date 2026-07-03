import pytest
from pydantic import ValidationError

from oradiag.models import EvidencePayload
from oradiag.providers import (
    FixtureEvidenceProvider,
    FixtureFileNotFoundError,
    FixtureFormatError,
    FixtureYAMLError,
    load_fixture_yaml,
)


def write_valid_fixture(path) -> None:
    path.write_text(
        """
schema_version: "1.0"
scenario:
  id: slow-lock
  name: Lentitud por bloqueo simulado
  symptom: slow_performance
  target_id: lab_orcl_01
  profile: diag_all
target:
  target_id: lab_orcl_01
  display_name: Laboratorio ORCL 01
  environment: lab
  metadata:
    host_alias: lab-db
provider:
  provider_type: fixture
  provider_name: FixtureEvidenceProvider
  source_ref: slow_lock_contention.yaml
access_layers:
  - name: database
    available: true
    status: OK
observations:
  - id: obs-001
    check_id: locks
    subject:
      kind: session
      id: sid-10
      attributes:
        module: batch
    status: PROBLEM
    severity: critical
    polarity: positive
    candidate_domain: database
    message: Sesion simulada bloqueada.
    structured_data:
      wait_event: enq TX row lock contention
reviews:
  - check_id: locks
    title: Bloqueos simulados
    status: PROBLEM
    severity: critical
    observations:
      - id: obs-001
        check_id: locks
        subject:
          kind: session
          id: sid-10
        status: PROBLEM
        severity: critical
        polarity: positive
        candidate_domain: database
        message: Sesion simulada bloqueada.
limitations: []
""",
        encoding="utf-8",
    )


def test_fixture_provider_transforms_yaml_to_validated_evidence_payload(tmp_path) -> None:
    fixture_path = tmp_path / "slow_lock_contention.yaml"
    write_valid_fixture(fixture_path)

    payload = FixtureEvidenceProvider(fixture_path).load()

    assert isinstance(payload, EvidencePayload)
    assert payload.schema_version == "1.0"
    assert payload.scenario.id == "slow-lock"
    assert payload.provider.provider_type == "fixture"
    assert payload.observations[0].id == "obs-001"


def test_load_fixture_yaml_fails_clearly_for_missing_file(tmp_path) -> None:
    with pytest.raises(FixtureFileNotFoundError, match="No existe el fixture"):
        load_fixture_yaml(tmp_path / "missing.yaml")


def test_load_fixture_yaml_fails_clearly_for_invalid_yaml(tmp_path) -> None:
    fixture_path = tmp_path / "invalid.yaml"
    fixture_path.write_text("scenario: [", encoding="utf-8")

    with pytest.raises(FixtureYAMLError, match="YAML invalido"):
        load_fixture_yaml(fixture_path)


def test_load_fixture_yaml_requires_mapping(tmp_path) -> None:
    fixture_path = tmp_path / "list.yaml"
    fixture_path.write_text("- one\n- two\n", encoding="utf-8")

    with pytest.raises(FixtureFormatError, match="debe ser un mapa"):
        load_fixture_yaml(fixture_path)


def test_fixture_provider_does_not_hide_model_validation_errors(tmp_path) -> None:
    fixture_path = tmp_path / "invalid_payload.yaml"
    fixture_path.write_text(
        """
schema_version: "1.0"
scenario:
  id: invalid
target:
  target_id: lab_orcl_01
  display_name: Lab
provider:
  provider_type: fixture
  provider_name: FixtureEvidenceProvider
""",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        FixtureEvidenceProvider(fixture_path).load()

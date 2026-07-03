from oradiag.providers import (
    FixtureEvidenceProvider,
    load_fixture_expectations,
    strip_expected_sections,
)


def test_expected_sections_are_excluded_from_evidence_payload(tmp_path) -> None:
    fixture_path = tmp_path / "with_expected.yaml"
    fixture_path.write_text(
        """
schema_version: "1.0"
scenario:
  id: expected-sections
  name: Expected sections
  symptom: unspecified
  target_id: lab_orcl_01
  profile: diag_all
target:
  target_id: lab_orcl_01
  display_name: Laboratorio ORCL 01
provider:
  provider_type: fixture
  provider_name: FixtureEvidenceProvider
expected_output:
  assessment:
    status: determined
expected_diagnosis:
  primary_domain: database
""",
        encoding="utf-8",
    )

    payload = FixtureEvidenceProvider(fixture_path).load()
    dumped = payload.model_dump()

    assert "expected_output" not in dumped
    assert "expected_diagnosis" not in dumped


def test_expected_sections_are_available_only_through_explicit_test_helper(tmp_path) -> None:
    fixture_path = tmp_path / "with_expected.yaml"
    fixture_path.write_text(
        """
schema_version: "1.0"
scenario:
  id: expected-sections
  name: Expected sections
  symptom: unspecified
  target_id: lab_orcl_01
  profile: diag_all
target:
  target_id: lab_orcl_01
  display_name: Laboratorio ORCL 01
provider:
  provider_type: fixture
  provider_name: FixtureEvidenceProvider
expected_output:
  assessment:
    status: determined
expected_diagnosis:
  primary_domain: database
""",
        encoding="utf-8",
    )

    expectations = load_fixture_expectations(fixture_path)

    assert expectations == {
        "expected_output": {"assessment": {"status": "determined"}},
        "expected_diagnosis": {"primary_domain": "database"},
    }


def test_strip_expected_sections_keeps_only_evidence_contract_fields() -> None:
    raw = {
        "schema_version": "1.0",
        "scenario": {},
        "target": {},
        "provider": {},
        "expected_output": {"ignored": True},
        "expected_diagnosis": {"ignored": True},
    }

    stripped = strip_expected_sections(raw)

    assert stripped == {
        "schema_version": "1.0",
        "scenario": {},
        "target": {},
        "provider": {},
    }

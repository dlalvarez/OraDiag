from typing import get_type_hints

from oradiag.models import EvidencePayload
from oradiag.providers import EvidenceProvider, FixtureEvidenceProvider


def test_evidence_provider_protocol_returns_evidence_payload() -> None:
    hints = get_type_hints(EvidenceProvider.load)

    assert hints["return"] is EvidencePayload


def test_fixture_provider_satisfies_neutral_evidence_provider_protocol(tmp_path) -> None:
    fixture_path = tmp_path / "minimal.yaml"
    fixture_path.write_text(
        """
schema_version: "1.0"
scenario:
  id: provider-test
  name: Provider test
  symptom: unspecified
  target_id: lab_orcl_01
  profile: diag_all
target:
  target_id: lab_orcl_01
  display_name: Lab ORCL 01
  environment: lab
provider:
  provider_type: fixture
  provider_name: FixtureEvidenceProvider
""",
        encoding="utf-8",
    )

    provider: EvidenceProvider = FixtureEvidenceProvider(fixture_path)

    assert isinstance(provider, EvidenceProvider)
    assert isinstance(provider.load(), EvidencePayload)

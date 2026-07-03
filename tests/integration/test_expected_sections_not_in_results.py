import json

from typer.testing import CliRunner

from oradiag.cli.app import app
from oradiag.providers import FixtureEvidenceProvider, load_fixture_expectations


runner = CliRunner()
FIXTURE = "tests/fixtures/lab/slow_lock_contention.yaml"
BASE_ARGS = [
    "run",
    "--config",
    "examples/lab/config.yaml",
    "--target",
    "lab_orcl_01",
    "--profile",
    "diag_all",
    "--fixture",
    FIXTURE,
]


def test_expected_sections_are_test_only_and_not_evidence_payload() -> None:
    expectations = load_fixture_expectations(FIXTURE)
    evidence = FixtureEvidenceProvider(FIXTURE).load()

    assert "expected_output" in expectations
    assert "expected_diagnosis" in expectations
    evidence_json = evidence.model_dump_json()
    assert "expected_output" not in evidence_json
    assert "expected_diagnosis" not in evidence_json


def test_expected_sections_are_not_visible_in_cli_json_result() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "json"])
    payload = json.loads(result.stdout)
    serialized = json.dumps(payload)

    assert result.exit_code == 0
    assert "expected_output" not in serialized
    assert "expected_diagnosis" not in serialized


def test_expected_sections_are_not_visible_in_cli_console_result() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "console"])

    assert result.exit_code == 0
    assert "expected_output" not in result.stdout
    assert "expected_diagnosis" not in result.stdout


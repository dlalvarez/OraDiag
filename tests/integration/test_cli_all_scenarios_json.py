import json

import pytest
from typer.testing import CliRunner

from oradiag.cli.app import app


runner = CliRunner()
BASE_ARGS = [
    "run",
    "--config",
    "examples/lab/config.yaml",
    "--target",
    "lab_orcl_01",
    "--profile",
    "diag_all",
]

SCENARIOS = [
    ("slow_lock_contention", "database", "determined", False),
    ("account_locked", "user", "determined", False),
    ("storage_pressure", "storage", "determined", False),
    ("all_technical_ok_app_data_suspected", "data", "determined", False),
    ("insufficient_access", "undetermined", "undetermined", True),
    ("unrelated_incidental_findings", "undetermined", "undetermined", True),
]


@pytest.mark.parametrize(
    ("scenario_id", "expected_domain", "expected_status", "insufficient"),
    SCENARIOS,
)
def test_cli_run_json_all_lab_scenarios(
    scenario_id: str,
    expected_domain: str,
    expected_status: str,
    insufficient: bool,
) -> None:
    result = runner.invoke(
        app,
        [
            *BASE_ARGS,
            "--fixture",
            f"tests/fixtures/lab/{scenario_id}.yaml",
            "--output",
            "json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)

    assert payload["schema_version"] == "1.0"
    assert payload["scenario"]["id"] == scenario_id
    assert payload["assessment"]["status"] == expected_status
    assert payload["assessment"]["domain"] == expected_domain
    assert payload["insufficient_evidence"] is insufficient
    assert isinstance(payload["findings"], list)
    assert isinstance(payload["related_findings"], list)
    assert isinstance(payload["incidental_findings"], list)
    assert isinstance(payload["ok_reviews"], list)
    assert isinstance(payload["limitations"], list)
    assert isinstance(payload["recommendations"], list)
    assert "summary" in payload
    assert payload["summary"]["headline"]
    assert "next_steps" in payload["summary"]

    if expected_status == "determined":
        assert payload["assessment"]["primary_cause_id"]
    else:
        assert payload["assessment"]["primary_cause_id"] is None


def test_cli_run_json_preserves_incidental_finding_for_unrelated_scenario() -> None:
    result = runner.invoke(
        app,
        [
            *BASE_ARGS,
            "--fixture",
            "tests/fixtures/lab/unrelated_incidental_findings.yaml",
            "--output",
            "json",
        ],
    )

    payload = json.loads(result.stdout)

    assert result.exit_code == 0
    assert payload["assessment"]["primary_cause_id"] is None
    assert payload["incidental_findings"]
    assert payload["incidental_findings"][0]["domain"] == "storage"


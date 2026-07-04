import json

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
    "--fixture",
    "tests/fixtures/lab/slow_lock_contention.yaml",
]


def test_cli_selects_json_reporter() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["assessment"]["domain"] == "database"
    assert payload["summary"]["headline"].startswith("Causa probable")
    assert payload["summary"]["primary_evidence"] == ["obs-locks-001"]


def test_cli_accepts_symptom_and_reflects_effective_json_scenario() -> None:
    result = runner.invoke(
        app,
        [*BASE_ARGS, "--symptom", "slow_performance", "--output", "json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["scenario"]["symptom"] == "slow_performance"


def test_cli_selects_console_reporter() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "console"])

    assert result.exit_code == 0
    assert "=== Diagnostico OraDiag ===" in result.stdout
    assert "Causa probable principal:" in result.stdout
    assert "Evidencia principal:" in result.stdout


def test_cli_rejects_invalid_symptom_before_running_reporter() -> None:
    result = runner.invoke(
        app,
        [*BASE_ARGS, "--symptom", "invalid_symptom", "--output", "json"],
    )

    assert result.exit_code == 2
    assert "Sintoma invalido" in result.output
    assert "invalid_symptom" not in result.output
    assert "Traceback" not in result.output


def test_cli_rejects_invalid_output_before_running_reporter() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "xml"])

    assert result.exit_code == 2
    assert "Formato de salida invalido" in result.output
    assert "Traceback" not in result.output


def test_cli_symptom_preserves_evidence_based_primary_cause() -> None:
    result = runner.invoke(
        app,
        [*BASE_ARGS, "--symptom", "slow_performance", "--output", "json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["assessment"]["status"] == "determined"
    assert payload["assessment"]["domain"] == "database"
    assert payload["assessment"]["primary_cause_id"] == "finding-obs-locks-001"
    assert payload["findings"][0]["evidence_ids"] == ["obs-locks-001"]


def test_cli_symptom_does_not_fabricate_primary_cause_without_evidence() -> None:
    args = BASE_ARGS.copy()
    args[args.index("tests/fixtures/lab/slow_lock_contention.yaml")] = (
        "tests/fixtures/lab/insufficient_access.yaml"
    )

    result = runner.invoke(
        app,
        [*args, "--symptom", "availability_down", "--output", "json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["scenario"]["symptom"] == "availability_down"
    assert payload["assessment"]["status"] == "undetermined"
    assert payload["assessment"]["domain"] == "undetermined"
    assert payload["assessment"]["primary_cause_id"] is None
    assert payload["insufficient_evidence"] is True

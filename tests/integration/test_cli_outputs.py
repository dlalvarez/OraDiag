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


def test_cli_selects_console_reporter() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "console"])

    assert result.exit_code == 0
    assert "=== Diagnostico OraDiag ===" in result.stdout
    assert "Causa probable principal:" in result.stdout
    assert "Evidencia principal:" in result.stdout


def test_cli_rejects_invalid_output_before_running_reporter() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "xml"])

    assert result.exit_code == 2
    assert "Formato de salida invalido" in result.output
    assert "Traceback" not in result.output


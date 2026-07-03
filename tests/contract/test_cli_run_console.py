from typer.testing import CliRunner

from oradiag.cli.app import app


runner = CliRunner()


def test_cli_run_outputs_minimal_human_console() -> None:
    result = runner.invoke(
        app,
        [
            "run",
            "--config",
            "examples/lab/config.yaml",
            "--target",
            "lab_orcl_01",
            "--profile",
            "diag_all",
            "--fixture",
            "tests/fixtures/lab/slow_lock_contention.yaml",
            "--output",
            "console",
        ],
    )

    assert result.exit_code == 0
    assert "Escenario: slow_lock_contention" in result.stdout
    assert "Estado: determined" in result.stdout
    assert "Dominio: database" in result.stdout
    assert "Confianza:" in result.stdout
    assert "Causa primaria:" in result.stdout
    assert "Recomendaciones:" in result.stdout
    assert "Traceback" not in result.output


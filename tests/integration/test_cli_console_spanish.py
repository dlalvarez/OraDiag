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


def run_console(fixture_name: str):
    return runner.invoke(
        app,
        [
            *BASE_ARGS,
            "--fixture",
            f"tests/fixtures/lab/{fixture_name}.yaml",
            "--output",
            "console",
        ],
    )


def test_cli_console_spanish_includes_primary_cause_when_determined() -> None:
    result = run_console("slow_lock_contention")

    assert result.exit_code == 0
    assert "=== Diagnostico OraDiag ===" in result.stdout
    assert "Escenario: slow_lock_contention" in result.stdout
    assert "Sintoma: slow_performance" in result.stdout
    assert "Causa probable principal:" in result.stdout
    assert "Evidencia principal:" in result.stdout
    assert "Recomendaciones:" in result.stdout


def test_cli_console_spanish_includes_undetermined_message() -> None:
    result = run_console("insufficient_access")

    assert result.exit_code == 0
    assert "Resultado indeterminado:" in result.stdout
    assert "No hay causa probable principal con evidencia suficiente." in result.stdout
    assert "Limitaciones:" in result.stdout


def test_cli_console_spanish_includes_data_boundary_message() -> None:
    result = run_console("all_technical_ok_app_data_suspected")

    assert result.exit_code == 0
    assert "Frontera Aplicacion/Datos:" in result.stdout
    assert "no diagnostica tablas de negocio" in result.stdout
    assert "Hipotesis descartadas / revisiones OK:" in result.stdout


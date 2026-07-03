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


def test_cli_run_returns_config_error_for_unknown_target() -> None:
    args = BASE_ARGS.copy()
    args[args.index("lab_orcl_01")] = "missing_target"

    result = runner.invoke(app, args)

    assert result.exit_code == 3
    assert "Error de configuracion" in result.output
    assert "Traceback" not in result.output


def test_cli_run_returns_config_error_for_unknown_profile() -> None:
    args = BASE_ARGS.copy()
    args[args.index("diag_all")] = "missing_profile"

    result = runner.invoke(app, args)

    assert result.exit_code == 3
    assert "Error de configuracion" in result.output
    assert "Traceback" not in result.output


def test_cli_run_returns_fixture_error_for_missing_fixture() -> None:
    args = BASE_ARGS.copy()
    args[args.index("tests/fixtures/lab/slow_lock_contention.yaml")] = (
        "tests/fixtures/lab/missing_fixture.yaml"
    )

    result = runner.invoke(app, args)

    assert result.exit_code == 4
    assert "Error de fixture/evidencia" in result.output
    assert "Traceback" not in result.output


def test_cli_run_returns_usage_error_for_invalid_output() -> None:
    result = runner.invoke(app, [*BASE_ARGS, "--output", "xml"])

    assert result.exit_code == 2
    assert "Formato de salida invalido" in result.output
    assert "Traceback" not in result.output


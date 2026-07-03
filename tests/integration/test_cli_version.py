from typer.testing import CliRunner

from oradiag.cli.app import app


runner = CliRunner()


def test_cli_version_identifies_tool_without_runtime_inputs() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "OraDiag" in result.stdout
    assert "version" in result.stdout.lower()
    assert "config" not in result.stdout.lower()
    assert "fixture" not in result.stdout.lower()
    assert "Traceback" not in result.output


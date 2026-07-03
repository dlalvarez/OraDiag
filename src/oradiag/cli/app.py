"""Typer application entrypoint."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pydantic import ValidationError
import typer

from oradiag.config import (
    ConfigError,
    load_app_config,
    resolve_profile,
    resolve_target,
)
from oradiag.providers import (
    FixtureEvidenceProvider,
    FixtureFileNotFoundError,
    FixtureFormatError,
    FixtureYAMLError,
)
from oradiag.rca import RCAEngine
from oradiag.reports import render_console_report, render_json_report

app = typer.Typer(
    help="OraDiag: diagnostico RCA de incidentes Oracle basado en evidencia.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """CLI de OraDiag."""


def _package_version() -> str:
    try:
        return version("oradiag")
    except PackageNotFoundError:
        return "0.0.0"


@app.command("version")
def version_command() -> None:
    """Identifica la herramienta sin requerir conectividad ni configuracion."""

    typer.echo(f"OraDiag version {_package_version()}")


@app.command("run")
def run(
    config: Path = typer.Option(..., "--config", help="Ruta a configuracion YAML humana."),
    target: str = typer.Option(..., "--target", help="Identificador de target configurado."),
    profile: str = typer.Option(..., "--profile", help="Perfil declarativo de ejecucion."),
    fixture: Path = typer.Option(..., "--fixture", help="Fixture YAML de laboratorio."),
    output: str = typer.Option("console", "--output", help="Formato de salida: console o json."),
) -> None:
    """Ejecuta un diagnostico simulado desde un fixture de laboratorio."""

    output_format = output.lower()
    if output_format not in {"console", "json"}:
        typer.echo("Formato de salida invalido. Use console o json.", err=True)
        raise typer.Exit(2)

    try:
        app_config = load_app_config(config)
        resolve_target(app_config, target)
        resolve_profile(app_config, profile)

        evidence = FixtureEvidenceProvider(fixture).load()
        result = RCAEngine().evaluate(evidence)

        if output_format == "json":
            typer.echo(render_json_report(result))
        else:
            typer.echo(render_console_report(result))
    except ConfigError as exc:
        typer.echo(f"Error de configuracion: {exc}", err=True)
        raise typer.Exit(3) from exc
    except (
        FixtureFileNotFoundError,
        FixtureFormatError,
        FixtureYAMLError,
        ValidationError,
    ) as exc:
        typer.echo(f"Error de fixture/evidencia: {exc}", err=True)
        raise typer.Exit(4) from exc
    except typer.Exit:
        raise
    except Exception as exc:
        typer.echo(f"Error inesperado controlado: {exc}", err=True)
        raise typer.Exit(1) from exc

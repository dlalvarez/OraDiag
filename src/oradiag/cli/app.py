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
from oradiag.models import EvidencePayload, SymptomCategory
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


def _allowed_symptoms() -> str:
    return ", ".join(item.value for item in SymptomCategory)


def _normalize_cli_symptom(value: str | None) -> SymptomCategory | None:
    if value is None:
        return None
    try:
        return SymptomCategory(value)
    except ValueError as exc:
        raise ValueError(f"Sintoma invalido. Use uno de: {_allowed_symptoms()}.") from exc


def apply_cli_symptom(
    evidence: EvidencePayload, symptom: SymptomCategory | None
) -> EvidencePayload:
    """Return evidence with the CLI symptom override applied when present."""

    if symptom is None:
        return evidence

    scenario = evidence.scenario.model_copy(update={"symptom": symptom.value})
    return evidence.model_copy(update={"scenario": scenario})


@app.command("run")
def run(
    config: Path = typer.Option(..., "--config", help="Ruta a configuracion YAML humana."),
    target: str = typer.Option(..., "--target", help="Identificador de target configurado."),
    profile: str = typer.Option(..., "--profile", help="Perfil declarativo de ejecucion."),
    symptom: str | None = typer.Option(
        None,
        "--symptom",
        help=(
            "Sintoma efectivo: cannot_connect, connection_hangs, errors, "
            "slow_performance, partial_impact, availability_down o unspecified."
        ),
    ),
    fixture: Path = typer.Option(..., "--fixture", help="Fixture YAML de laboratorio."),
    output: str = typer.Option("console", "--output", help="Formato de salida: console o json."),
) -> None:
    """Ejecuta un diagnostico simulado desde un fixture de laboratorio."""

    output_format = output.lower()
    if output_format not in {"console", "json"}:
        typer.echo("Formato de salida invalido. Use console o json.", err=True)
        raise typer.Exit(2)

    try:
        normalized_symptom = _normalize_cli_symptom(symptom)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc

    try:
        app_config = load_app_config(config)
        resolve_target(app_config, target)
        resolve_profile(app_config, profile)

        evidence = apply_cli_symptom(FixtureEvidenceProvider(fixture).load(), normalized_symptom)
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

"""Typer application entrypoint."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError
import typer

from oradiag.config import (
    ConfigError,
    load_app_config,
    resolve_profile,
    resolve_target,
)
from oradiag.models import DiagnosticFinding, DiagnosticResult
from oradiag.providers import (
    FixtureEvidenceProvider,
    FixtureFileNotFoundError,
    FixtureFormatError,
    FixtureYAMLError,
)
from oradiag.rca import RCAEngine

app = typer.Typer(
    help="OraDiag: diagnostico RCA de incidentes Oracle basado en evidencia.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """CLI de OraDiag."""


def _primary_finding(result: DiagnosticResult) -> DiagnosticFinding | None:
    primary_id = result.assessment.primary_cause_id
    if primary_id is None:
        return None
    return next((finding for finding in result.findings if finding.id == primary_id), None)


def _render_json(result: DiagnosticResult) -> str:
    return json.dumps(
        result.model_dump(mode="json"),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def _render_console(result: DiagnosticResult) -> str:
    primary = _primary_finding(result)
    lines = [
        f"Escenario: {result.scenario.id}",
        f"Estado: {result.assessment.status}",
        f"Dominio: {result.assessment.domain}",
        f"Confianza: {result.assessment.confidence}",
    ]
    if primary is None:
        lines.append("Causa primaria: no determinada")
    else:
        lines.append(f"Causa primaria: {primary.title}")
        lines.append(f"Descripcion: {primary.description}")

    if result.limitations:
        lines.append("Limitaciones:")
        lines.extend(f"- {limitation.scope}: {limitation.message}" for limitation in result.limitations)

    lines.append("Recomendaciones:")
    lines.extend(f"- {recommendation.title}: {recommendation.description}" for recommendation in result.recommendations)

    if result.insufficient_evidence:
        lines.append("Advertencia: evidencia insuficiente para confirmar causa probable principal.")

    return "\n".join(lines)


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
            typer.echo(_render_json(result))
        else:
            typer.echo(_render_console(result))
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

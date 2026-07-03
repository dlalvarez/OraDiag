"""Typer application entrypoint."""

from __future__ import annotations

import typer

app = typer.Typer(
    help="OraDiag: diagnostico RCA de incidentes Oracle basado en evidencia.",
    no_args_is_help=True,
)

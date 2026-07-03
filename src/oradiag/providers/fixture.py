"""Fixture-backed evidence provider for laboratory scenarios."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from oradiag.models import EvidencePayload
from oradiag.providers.base import EvidenceProvider

EXPECTED_SECTIONS = ("expected_output", "expected_diagnosis")


class FixtureFileNotFoundError(FileNotFoundError):
    """Raised when a fixture path does not exist."""


class FixtureYAMLError(ValueError):
    """Raised when a fixture file is not valid YAML."""


class FixtureFormatError(ValueError):
    """Raised when fixture YAML is not a mapping."""


def load_fixture_yaml(path: str | Path) -> dict[str, Any]:
    """Load a human laboratory fixture using safe YAML parsing."""

    fixture_path = Path(path)
    if not fixture_path.is_file():
        raise FixtureFileNotFoundError(f"No existe el fixture de laboratorio: {fixture_path}")

    try:
        raw = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise FixtureYAMLError(f"YAML invalido en fixture de laboratorio: {fixture_path}") from exc

    if not isinstance(raw, dict):
        raise FixtureFormatError("El fixture de laboratorio debe ser un mapa YAML.")

    return raw


def strip_expected_sections(raw_fixture: dict[str, Any]) -> dict[str, Any]:
    """Return fixture evidence without test-only expected sections."""

    return {key: value for key, value in raw_fixture.items() if key not in EXPECTED_SECTIONS}


def load_fixture_expectations(path: str | Path) -> dict[str, Any]:
    """Load test-only expected sections from a fixture."""

    raw = load_fixture_yaml(path)
    return {key: raw[key] for key in EXPECTED_SECTIONS if key in raw}


class FixtureEvidenceProvider(EvidenceProvider):
    """Evidence provider that transforms one fixture YAML file into EvidencePayload."""

    def __init__(self, fixture_path: str | Path) -> None:
        self.fixture_path = Path(fixture_path)

    def load(self) -> EvidencePayload:
        raw = load_fixture_yaml(self.fixture_path)
        evidence_data = strip_expected_sections(raw)
        return EvidencePayload.model_validate(evidence_data)

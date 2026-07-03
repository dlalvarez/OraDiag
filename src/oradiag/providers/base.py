"""Neutral evidence provider interface."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from oradiag.models import EvidencePayload


@runtime_checkable
class EvidenceProvider(Protocol):
    """Source-neutral interface for components that produce Evidence Payloads."""

    def load(self) -> EvidencePayload:
        """Return validated evidence for the RCA engine."""
        ...

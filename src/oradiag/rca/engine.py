"""RCA engine stub.

The functional RCA rules are intentionally out of scope until later tasks.
"""

from __future__ import annotations

from oradiag.models import DiagnosticResult, EvidencePayload


class RCAEngine:
    """Minimal typed API boundary for future RCA implementation."""

    def evaluate(self, evidence: EvidencePayload) -> DiagnosticResult:
        if not isinstance(evidence, EvidencePayload):
            raise TypeError("RCAEngine.evaluate solo acepta EvidencePayload validado.")
        raise NotImplementedError("El motor RCA funcional se implementa en tareas posteriores.")

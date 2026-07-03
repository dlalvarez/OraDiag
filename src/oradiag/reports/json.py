"""Formal JSON reporter for DiagnosticResult."""

from __future__ import annotations

import json
from typing import Any

from oradiag.models import CausalRole, DiagnosticFinding, DiagnosticResult


def _primary_finding(result: DiagnosticResult) -> DiagnosticFinding | None:
    primary_id = result.assessment.primary_cause_id
    if primary_id is None:
        return None
    return next((finding for finding in result.findings if finding.id == primary_id), None)


def _role_is(value: object, role: CausalRole) -> bool:
    return value == role or value == role.value


def _headline(result: DiagnosticResult, primary: DiagnosticFinding | None) -> str:
    if result.insufficient_evidence:
        return "No hay evidencia suficiente para determinar causa probable principal."
    if result.assessment.domain == "data":
        return "Frontera Aplicacion/Datos identificada con evidencia tecnica OK."
    if primary is not None:
        return f"Causa probable en dominio {result.assessment.domain}: {primary.title}."
    return f"Diagnostico determinado en dominio {result.assessment.domain}."


def _explanation(result: DiagnosticResult, primary: DiagnosticFinding | None) -> str:
    if primary is None:
        return result.assessment.reasoning
    return f"{result.assessment.reasoning} Evidencia principal: {primary.description}"


def _confidence_explanation(result: DiagnosticResult) -> str:
    if result.assessment.confidence == "high":
        return "Confianza alta por evidencia directa suficiente y limitaciones no dominantes."
    if result.assessment.confidence == "medium":
        return "Confianza media: la evidencia soporta la conclusion, pero requiere validacion humana."
    return "Confianza baja: la evidencia es limitada, indirecta o define una frontera de analisis."


def _ruled_out_summary(result: DiagnosticResult) -> list[str]:
    summaries = [
        f"{review.check_id}: {review.ok_relevance}"
        for review in result.ok_reviews
        if review.ok_relevance
    ]
    summaries.extend(
        f"{finding.id}: {finding.description}"
        for finding in result.findings
        if _role_is(finding.role, CausalRole.RULED_OUT)
        and finding.evidence_ids
        and finding.evidence_ids[0] not in {review.check_id for review in result.ok_reviews}
    )
    return summaries


def _limitations_summary(result: DiagnosticResult) -> list[str]:
    return [f"{limitation.scope}: {limitation.message}" for limitation in result.limitations]


def _next_steps(result: DiagnosticResult) -> list[str]:
    return [
        f"{recommendation.title}: {recommendation.description}"
        for recommendation in result.recommendations
    ]


def build_json_report(result: DiagnosticResult) -> dict[str, Any]:
    """Return DiagnosticResult JSON plus deterministic derived narrative."""

    primary = _primary_finding(result)
    report = result.model_dump(mode="json")
    report["summary"] = {
        "headline": _headline(result, primary),
        "explanation": _explanation(result, primary),
        "confidence_explanation": _confidence_explanation(result),
        "primary_evidence": list(result.assessment.evidence_ids),
        "ruled_out_summary": _ruled_out_summary(result),
        "limitations_summary": _limitations_summary(result),
        "next_steps": _next_steps(result),
        "insufficient_evidence_warning": (
            "Resultado indeterminado: no hay evidencia suficiente para emitir causa probable principal."
            if result.insufficient_evidence
            else None
        ),
        "data_boundary_warning": (
            "Frontera Aplicacion/Datos: OraDiag no diagnostica tablas de negocio ni datos funcionales."
            if result.assessment.domain == "data"
            else None
        ),
    }
    return report


def render_json_report(result: DiagnosticResult) -> str:
    """Serialize the formal JSON report with stable ordering."""

    return json.dumps(build_json_report(result), ensure_ascii=False, indent=2, sort_keys=True)

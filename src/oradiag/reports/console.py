"""Formal Spanish console reporter for DiagnosticResult."""

from __future__ import annotations

from oradiag.models import CausalRole, DiagnosticFinding, DiagnosticResult


def _primary_finding(result: DiagnosticResult) -> DiagnosticFinding | None:
    primary_id = result.assessment.primary_cause_id
    if primary_id is None:
        return None
    return next((finding for finding in result.findings if finding.id == primary_id), None)


def _role_is(value: object, role: CausalRole) -> bool:
    return value == role or value == role.value


def _finding_lines(findings: list[DiagnosticFinding]) -> list[str]:
    if not findings:
        return ["- Sin hallazgos en esta categoria."]
    return [
        (
            f"- {finding.title} [{finding.domain}, {finding.severity}, "
            f"confianza {finding.confidence}]: {finding.description}"
        )
        for finding in findings
    ]


def _ruled_out_lines(result: DiagnosticResult) -> list[str]:
    lines = [
        f"- {review.check_id}: {review.ok_relevance}"
        for review in result.ok_reviews
        if review.ok_relevance
    ]
    ok_review_ids = {review.check_id for review in result.ok_reviews}
    lines.extend(
        f"- {finding.title}: {finding.description}"
        for finding in result.findings
        if _role_is(finding.role, CausalRole.RULED_OUT)
        and (not finding.evidence_ids or finding.evidence_ids[0] not in ok_review_ids)
    )
    return lines or ["- No hay hipotesis descartadas registradas."]


def _limitation_lines(result: DiagnosticResult) -> list[str]:
    if not result.limitations:
        return ["- Sin limitaciones reportadas."]
    return [
        f"- {limitation.scope}: {limitation.message} Impacto: {limitation.impact}"
        for limitation in result.limitations
    ]


def _recommendation_lines(result: DiagnosticResult) -> list[str]:
    if not result.recommendations:
        return ["- Sin recomendaciones registradas."]
    return [
        f"- {recommendation.title}: {recommendation.description}"
        for recommendation in result.recommendations
    ]


def render_console_report(result: DiagnosticResult) -> str:
    """Render a human-oriented Spanish diagnostic report without RCA recalculation."""

    primary = _primary_finding(result)
    lines = [
        "=== Diagnostico OraDiag ===",
        f"Escenario: {result.scenario.id}",
        f"Sintoma: {result.scenario.symptom}",
        f"Estado: {result.assessment.status}",
        f"Dominio: {result.assessment.domain}",
        f"Confianza: {result.assessment.confidence}",
        "",
    ]

    if result.insufficient_evidence:
        lines.extend(
            [
                "Resultado indeterminado:",
                "No hay causa probable principal con evidencia suficiente.",
                result.assessment.reasoning,
                "",
            ]
        )
    elif result.assessment.domain == "data":
        lines.extend(
            [
                "Frontera Aplicacion/Datos:",
                (
                    "Las revisiones tecnicas disponibles no explican el sintoma; "
                    "OraDiag no diagnostica tablas de negocio ni datos funcionales."
                ),
                "",
            ]
        )

    lines.append("Causa probable principal:")
    if primary is None:
        lines.append("- No determinada.")
        lines.append("Causa primaria: no determinada")
    else:
        lines.append(f"- {primary.title} [{primary.domain}, confianza {primary.confidence}]")
        lines.append(f"  {primary.description}")
        lines.append(f"Causa primaria: {primary.title}")
    lines.append("")

    lines.extend(["Explicacion:", f"- {result.assessment.reasoning}", ""])

    lines.append("Evidencia principal:")
    if result.assessment.evidence_ids:
        lines.extend(f"- {evidence_id}" for evidence_id in result.assessment.evidence_ids)
    else:
        lines.append("- Sin evidencia principal suficiente.")
    lines.append("")

    lines.append("Hallazgos relacionados:")
    lines.extend(_finding_lines(result.related_findings))
    lines.append("")

    lines.append("Hallazgos incidentales:")
    lines.extend(_finding_lines(result.incidental_findings))
    lines.append("")

    lines.append("Hipotesis descartadas / revisiones OK:")
    lines.extend(_ruled_out_lines(result))
    lines.append("")

    lines.append("Limitaciones:")
    lines.extend(_limitation_lines(result))
    lines.append("")

    lines.append("Recomendaciones:")
    lines.extend(_recommendation_lines(result))

    return "\n".join(lines)

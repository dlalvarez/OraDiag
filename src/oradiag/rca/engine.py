"""Minimal deterministic RCA engine for laboratory evidence."""

from __future__ import annotations

from dataclasses import dataclass

from oradiag.models import (
    CausalAssessment,
    CausalDomain,
    CausalRole,
    Confidence,
    DiagnosticFinding,
    DiagnosticResult,
    EvidencePayload,
    EvidencePolarity,
    Limitation,
    Recommendation,
    ReviewResult,
    ReviewStatus,
    Severity,
    SymptomCategory,
)

PRIMARY_CAUSE_THRESHOLD = 6.0
TIE_MARGIN = 0.5

SEVERITY_WEIGHT = {
    Severity.INFO: 0.5,
    Severity.WARNING: 1.5,
    Severity.CRITICAL: 3.0,
    Severity.BLOCKER: 4.0,
    "info": 0.5,
    "warning": 1.5,
    "critical": 3.0,
    "blocker": 4.0,
}

STATUS_WEIGHT = {
    ReviewStatus.INFO: 0.0,
    ReviewStatus.OK: 0.0,
    ReviewStatus.WARNING: 1.0,
    ReviewStatus.PROBLEM: 2.0,
    ReviewStatus.CRITICAL: 3.0,
    ReviewStatus.UNKNOWN: 0.5,
    "INFO": 0.0,
    "OK": 0.0,
    "WARNING": 1.0,
    "PROBLEM": 2.0,
    "CRITICAL": 3.0,
    "UNKNOWN": 0.5,
}

SYMPTOM_DOMAINS = {
    SymptomCategory.SLOW_PERFORMANCE: {
        CausalDomain.DATABASE,
        CausalDomain.STORAGE,
        CausalDomain.OPERATING_SYSTEM,
        CausalDomain.APPLICATION,
        "database",
        "storage",
        "operating_system",
        "application",
    },
    SymptomCategory.CANNOT_CONNECT: {
        CausalDomain.USER,
        CausalDomain.INFRASTRUCTURE,
        CausalDomain.DATABASE,
        "user",
        "infrastructure",
        "database",
    },
    SymptomCategory.CONNECTION_HANGS: {
        CausalDomain.USER,
        CausalDomain.INFRASTRUCTURE,
        CausalDomain.DATABASE,
        "user",
        "infrastructure",
        "database",
    },
    SymptomCategory.ERRORS: {
        CausalDomain.DATABASE,
        CausalDomain.USER,
        CausalDomain.APPLICATION,
        "database",
        "user",
        "application",
    },
    SymptomCategory.AVAILABILITY_DOWN: {
        CausalDomain.DATABASE,
        CausalDomain.INFRASTRUCTURE,
        CausalDomain.OPERATING_SYSTEM,
        CausalDomain.STORAGE,
        "database",
        "infrastructure",
        "operating_system",
        "storage",
    },
    SymptomCategory.PARTIAL_IMPACT: {
        CausalDomain.APPLICATION,
        CausalDomain.USER,
        CausalDomain.DATABASE,
        "application",
        "user",
        "database",
    },
}


@dataclass(frozen=True)
class ScoredObservation:
    observation_id: str
    check_id: str
    title: str
    description: str
    domain: CausalDomain
    severity: Severity
    score: float
    related_to_symptom: bool
    explicitly_unrelated: bool


class RCAEngine:
    """Small deterministic engine that evaluates validated EvidencePayload objects."""

    def evaluate(self, evidence: EvidencePayload) -> DiagnosticResult:
        if not isinstance(evidence, EvidencePayload):
            raise TypeError("RCAEngine.evaluate solo acepta EvidencePayload validado.")

        limitations = self._collect_limitations(evidence)
        ok_reviews = self._ok_reviews(evidence)
        scored = self._score_positive_observations(evidence)
        findings = self._build_non_primary_findings(evidence, scored)
        findings.extend(self._build_ruled_out_findings(evidence))
        findings.extend(self._build_not_evaluated_findings(evidence))

        primary = self._choose_primary(scored, limitations)
        if primary is None:
            data_boundary = self._build_data_boundary_primary(evidence, ok_reviews, limitations)
            if data_boundary is not None:
                findings.insert(0, data_boundary)
                return self._determined_result(evidence, data_boundary, findings, ok_reviews, limitations)
            return self._undetermined_result(evidence, findings, ok_reviews, limitations)

        primary_finding = self._finding_from_score(primary, CausalRole.PRIMARY_CAUSE)
        findings = [finding for finding in findings if finding.evidence_ids != [primary.observation_id]]
        findings.insert(0, primary_finding)
        return self._determined_result(evidence, primary_finding, findings, ok_reviews, limitations)

    def _score_positive_observations(self, evidence: EvidencePayload) -> list[ScoredObservation]:
        scored: list[ScoredObservation] = []
        for observation in evidence.observations:
            if observation.polarity != EvidencePolarity.POSITIVE and observation.polarity != "positive":
                continue
            if observation.status in {
                ReviewStatus.OK,
                ReviewStatus.INFO,
                ReviewStatus.TIMEOUT,
                ReviewStatus.ERROR,
                ReviewStatus.SKIPPED,
                "OK",
                "INFO",
                "TIMEOUT",
                "ERROR",
                "SKIPPED",
            }:
                continue
            domain = observation.candidate_domain or CausalDomain.UNDETERMINED
            explicit_related = observation.structured_data.get("related_to_symptom")
            related_to_symptom = self._is_related_to_symptom(evidence.scenario.symptom, domain)
            if explicit_related is True:
                related_to_symptom = True
            explicitly_unrelated = explicit_related is False

            score = SEVERITY_WEIGHT.get(observation.severity, 0.0)
            score += STATUS_WEIGHT.get(observation.status, 0.0)
            score += 2.0
            if related_to_symptom:
                score += 1.0
            if explicitly_unrelated:
                score -= 3.0

            scored.append(
                ScoredObservation(
                    observation_id=observation.id,
                    check_id=observation.check_id,
                    title=f"Hallazgo {observation.check_id}",
                    description=observation.message,
                    domain=domain,
                    severity=observation.severity,
                    score=score,
                    related_to_symptom=related_to_symptom,
                    explicitly_unrelated=explicitly_unrelated,
                )
            )
        return scored

    def _choose_primary(
        self, scored: list[ScoredObservation], limitations: list[Limitation]
    ) -> ScoredObservation | None:
        candidates = [
            item
            for item in scored
            if item.score >= PRIMARY_CAUSE_THRESHOLD and not item.explicitly_unrelated
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda item: item.score, reverse=True)
        if len(candidates) > 1:
            top, second = candidates[0], candidates[1]
            if top.domain != second.domain and (top.score - second.score) <= TIE_MARGIN:
                return None
        if len(limitations) >= 3 and candidates[0].score < 8.0:
            return None
        return candidates[0]

    def _build_non_primary_findings(
        self, evidence: EvidencePayload, scored: list[ScoredObservation]
    ) -> list[DiagnosticFinding]:
        findings: list[DiagnosticFinding] = []
        for item in scored:
            if item.explicitly_unrelated:
                role = CausalRole.INCIDENTAL_FINDING
            elif item.score >= 4.0 and item.related_to_symptom:
                role = CausalRole.CONTRIBUTING_FACTOR
            elif item.related_to_symptom or item.score >= 3.0:
                role = CausalRole.RELATED_FINDING
            else:
                role = CausalRole.INCIDENTAL_FINDING
            findings.append(self._finding_from_score(item, role))
        return findings

    def _build_ruled_out_findings(self, evidence: EvidencePayload) -> list[DiagnosticFinding]:
        findings: list[DiagnosticFinding] = []
        for review in self._ok_reviews(evidence):
            findings.append(
                DiagnosticFinding(
                    id=f"ruled-out-{review.check_id}",
                    title=f"Hipotesis descartada: {review.title}",
                    description=review.ok_relevance or "Revision OK usada como evidencia negativa.",
                    domain=self._domain_from_review(review),
                    role=CausalRole.RULED_OUT,
                    severity=Severity.INFO,
                    confidence=Confidence.MEDIUM,
                    evidence_ids=[review.check_id],
                )
            )
        for observation in evidence.observations:
            if observation.polarity == EvidencePolarity.NEGATIVE or observation.polarity == "negative":
                findings.append(
                    DiagnosticFinding(
                        id=f"ruled-out-{observation.id}",
                        title=f"Hipotesis descartada: {observation.check_id}",
                        description=observation.message,
                        domain=observation.candidate_domain or CausalDomain.UNDETERMINED,
                        role=CausalRole.RULED_OUT,
                        severity=Severity.INFO,
                        confidence=Confidence.MEDIUM,
                        evidence_ids=[observation.id],
                    )
                )
        return findings

    def _build_not_evaluated_findings(self, evidence: EvidencePayload) -> list[DiagnosticFinding]:
        findings: list[DiagnosticFinding] = []
        for review in evidence.reviews:
            if review.status in {ReviewStatus.TIMEOUT, ReviewStatus.ERROR, ReviewStatus.SKIPPED, "TIMEOUT", "ERROR", "SKIPPED"}:
                findings.append(
                    DiagnosticFinding(
                        id=f"not-evaluated-{review.check_id}",
                        title=f"No evaluado: {review.title}",
                        description="Revision no evaluada por error, timeout, permiso insuficiente o salto controlado.",
                        domain=self._domain_from_review(review),
                        role=CausalRole.NOT_EVALUATED,
                        severity=review.severity,
                        confidence=Confidence.LOW,
                        evidence_ids=[review.check_id],
                        limitation_ids=[limitation.id for limitation in review.limitations],
                    )
                )
        return findings

    def _build_data_boundary_primary(
        self,
        evidence: EvidencePayload,
        ok_reviews: list[ReviewResult],
        limitations: list[Limitation],
    ) -> DiagnosticFinding | None:
        positive_problem = any(
            (item.polarity == EvidencePolarity.POSITIVE or item.polarity == "positive")
            and item.status
            in {ReviewStatus.PROBLEM, ReviewStatus.CRITICAL, ReviewStatus.WARNING, "PROBLEM", "CRITICAL", "WARNING"}
            for item in evidence.observations
        )
        if positive_problem or limitations:
            return None
        if evidence.scenario.symptom in {SymptomCategory.UNSPECIFIED, "unspecified"}:
            return None
        if len(ok_reviews) < 2:
            return None
        return DiagnosticFinding(
            id="data-boundary",
            title="Frontera Aplicacion/Datos",
            description=(
                "Las revisiones tecnicas simuladas estan OK; el analisis debe continuar "
                "fuera de OraDiag con equipos de aplicacion, funcionales o datos."
            ),
            domain=CausalDomain.DATA,
            role=CausalRole.PRIMARY_CAUSE,
            severity=Severity.INFO,
            confidence=Confidence.LOW,
            evidence_ids=[review.check_id for review in ok_reviews],
        )

    def _determined_result(
        self,
        evidence: EvidencePayload,
        primary: DiagnosticFinding,
        findings: list[DiagnosticFinding],
        ok_reviews: list[ReviewResult],
        limitations: list[Limitation],
    ) -> DiagnosticResult:
        assessment = CausalAssessment(
            status="determined",
            primary_cause_id=primary.id,
            domain=primary.domain,
            confidence=primary.confidence,
            reasoning=self._determined_reasoning(primary),
            evidence_ids=primary.evidence_ids,
        )
        return DiagnosticResult(
            scenario=evidence.scenario,
            assessment=assessment,
            findings=findings,
            related_findings=[
                item for item in findings if item.role in {CausalRole.RELATED_FINDING, CausalRole.CONTRIBUTING_FACTOR, "related_finding", "contributing_factor"}
            ],
            incidental_findings=[
                item for item in findings if item.role in {CausalRole.INCIDENTAL_FINDING, "incidental_finding"}
            ],
            ok_reviews=ok_reviews,
            limitations=limitations,
            recommendations=self._recommendations(primary, findings, limitations),
            insufficient_evidence=False,
        )

    def _undetermined_result(
        self,
        evidence: EvidencePayload,
        findings: list[DiagnosticFinding],
        ok_reviews: list[ReviewResult],
        limitations: list[Limitation],
    ) -> DiagnosticResult:
        assessment = CausalAssessment(
            status="undetermined",
            domain=CausalDomain.UNDETERMINED,
            confidence=Confidence.LOW,
            reasoning="No hay evidencia suficiente o consistente para emitir causa probable principal.",
            evidence_ids=[],
        )
        return DiagnosticResult(
            scenario=evidence.scenario,
            assessment=assessment,
            findings=findings,
            related_findings=[
                item for item in findings if item.role in {CausalRole.RELATED_FINDING, CausalRole.CONTRIBUTING_FACTOR, "related_finding", "contributing_factor"}
            ],
            incidental_findings=[
                item for item in findings if item.role in {CausalRole.INCIDENTAL_FINDING, "incidental_finding"}
            ],
            ok_reviews=ok_reviews,
            limitations=limitations,
            recommendations=self._recommendations(None, findings, limitations),
            insufficient_evidence=True,
        )

    def _finding_from_score(
        self, item: ScoredObservation, role: CausalRole
    ) -> DiagnosticFinding:
        return DiagnosticFinding(
            id=f"finding-{item.observation_id}",
            title=item.title,
            description=item.description,
            domain=item.domain,
            role=role,
            severity=item.severity,
            confidence=self._confidence(item.score),
            evidence_ids=[item.observation_id],
        )

    def _confidence(self, score: float) -> Confidence:
        if score >= 8.0:
            return Confidence.HIGH
        if score >= PRIMARY_CAUSE_THRESHOLD:
            return Confidence.MEDIUM
        return Confidence.LOW

    def _recommendations(
        self,
        primary: DiagnosticFinding | None,
        findings: list[DiagnosticFinding],
        limitations: list[Limitation],
    ) -> list[Recommendation]:
        recommendations: list[Recommendation] = []
        if primary is not None:
            if primary.domain == CausalDomain.DATA or primary.domain == "data":
                recommendations.append(
                    Recommendation(
                        id="rec-data-boundary",
                        title="Escalar frontera Aplicacion/Datos",
                        description="Validar el caso con equipos funcionales, de aplicacion o datos sin consultar tablas de negocio desde OraDiag.",
                        risk="low",
                        prerequisites=["Revisiones tecnicas simuladas OK"],
                        requires_human_validation=True,
                    )
                )
            else:
                recommendations.append(
                    Recommendation(
                        id=f"rec-{primary.id}",
                        title="Validar causa probable",
                        description=f"Revisar la evidencia asociada a {primary.title} antes de ejecutar acciones operativas.",
                        risk="low",
                        prerequisites=["Confirmacion humana de la evidencia"],
                        requires_human_validation=True,
                    )
                )
        if any(item.role in {CausalRole.RELATED_FINDING, CausalRole.CONTRIBUTING_FACTOR, "related_finding", "contributing_factor"} for item in findings):
            recommendations.append(
                Recommendation(
                    id="rec-related-findings",
                    title="Revisar hallazgos relacionados",
                    description="Evaluar factores relacionados o contribuyentes sin tratarlos como causa principal automatica.",
                    risk="low",
                    requires_human_validation=True,
                )
            )
        if limitations:
            recommendations.append(
                Recommendation(
                    id="rec-limitations",
                    title="Obtener evidencia faltante",
                    description="Resolver limitaciones de acceso, timeout o datos incompletos antes de aumentar la confianza.",
                    risk="low",
                    prerequisites=[limitation.scope for limitation in limitations],
                    requires_human_validation=True,
                )
            )
        if not recommendations:
            recommendations.append(
                Recommendation(
                    id="rec-more-evidence",
                    title="Reunir mas evidencia",
                    description="No ejecutar acciones destructivas; reunir evidencia tecnica adicional.",
                    risk="low",
                    requires_human_validation=True,
                )
            )
        return recommendations

    def _collect_limitations(self, evidence: EvidencePayload) -> list[Limitation]:
        limitations = list(evidence.limitations)
        seen = {limitation.id for limitation in limitations}
        for layer in evidence.access_layers:
            for limitation in layer.limitations:
                if limitation.id not in seen:
                    limitations.append(limitation)
                    seen.add(limitation.id)
        for review in evidence.reviews:
            for limitation in review.limitations:
                if limitation.id not in seen:
                    limitations.append(limitation)
                    seen.add(limitation.id)
        return limitations

    def _ok_reviews(self, evidence: EvidencePayload) -> list[ReviewResult]:
        return [
            review
            for review in evidence.reviews
            if review.status in {ReviewStatus.OK, "OK"} and review.ok_relevance
        ]

    def _domain_from_review(self, review: ReviewResult) -> CausalDomain:
        for observation in review.observations:
            if observation.candidate_domain:
                return observation.candidate_domain
        return CausalDomain.UNDETERMINED

    def _is_related_to_symptom(self, symptom: SymptomCategory | str, domain: CausalDomain | str) -> bool:
        return domain in SYMPTOM_DOMAINS.get(symptom, set())

    def _determined_reasoning(self, primary: DiagnosticFinding) -> str:
        if primary.domain == CausalDomain.DATA or primary.domain == "data":
            return "La evidencia tecnica disponible no explica el sintoma; se declara frontera Aplicacion/Datos."
        return "La causa probable principal se selecciono por evidencia positiva suficiente y relacion con el sintoma."

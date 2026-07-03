from oradiag.models import (
    CausalDomain,
    EvidencePayload,
    EvidencePolarity,
    EvidenceProviderMetadata,
    DiagnosticScenario,
    Limitation,
    LimitationType,
    Observation,
    ObservedSubject,
    ReviewResult,
    ReviewStatus,
    Severity,
    SymptomCategory,
    TargetContext,
)
from oradiag.rca import RCAEngine


def observation(
    obs_id: str,
    check_id: str,
    domain: CausalDomain,
    severity: Severity = Severity.CRITICAL,
    status: ReviewStatus = ReviewStatus.PROBLEM,
    polarity: EvidencePolarity = EvidencePolarity.POSITIVE,
    related_to_symptom: bool | None = None,
) -> Observation:
    structured_data = {}
    if related_to_symptom is not None:
        structured_data["related_to_symptom"] = related_to_symptom
    return Observation(
        id=obs_id,
        check_id=check_id,
        subject=ObservedSubject(kind="component", id=f"subject-{obs_id}"),
        status=status,
        severity=severity,
        polarity=polarity,
        candidate_domain=domain,
        message=f"Evidencia simulada {obs_id}",
        structured_data=structured_data,
    )


def review(
    check_id: str,
    status: ReviewStatus = ReviewStatus.PROBLEM,
    severity: Severity = Severity.CRITICAL,
    observations: list[Observation] | None = None,
    ok_relevance: str | None = None,
    limitations: list[Limitation] | None = None,
) -> ReviewResult:
    return ReviewResult(
        check_id=check_id,
        title=f"Revision {check_id}",
        status=status,
        severity=severity,
        observations=observations or [],
        ok_relevance=ok_relevance,
        limitations=limitations or [],
    )


def limitation(limitation_id: str = "lim-001") -> Limitation:
    return Limitation(
        id=limitation_id,
        type=LimitationType.TIMEOUT,
        scope="database",
        message="Timeout simulado.",
        impact="Reduce cobertura.",
    )


def payload(
    observations: list[Observation] | None = None,
    reviews: list[ReviewResult] | None = None,
    limitations: list[Limitation] | None = None,
    symptom: SymptomCategory = SymptomCategory.SLOW_PERFORMANCE,
) -> EvidencePayload:
    return EvidencePayload(
        scenario=DiagnosticScenario(
            id="scenario-001",
            name="Escenario RCA unitario",
            symptom=symptom,
            target_id="lab_orcl_01",
            profile="diag_all",
        ),
        target=TargetContext(target_id="lab_orcl_01", display_name="Lab ORCL 01"),
        provider=EvidenceProviderMetadata(provider_type="fixture", provider_name="FixtureEvidenceProvider"),
        observations=observations or [],
        reviews=reviews or [],
        limitations=limitations or [],
    )


def test_selects_primary_cause_when_strong_evidence_matches_symptom() -> None:
    lock_observation = observation("obs-lock", "locks", CausalDomain.DATABASE)
    evidence = payload(
        observations=[lock_observation],
        reviews=[review("locks", observations=[lock_observation])],
        symptom=SymptomCategory.SLOW_PERFORMANCE,
    )

    result = RCAEngine().evaluate(evidence)

    assert result.assessment.status == "determined"
    assert result.assessment.domain == "database"
    assert result.assessment.primary_cause_id == "finding-obs-lock"
    assert result.findings[0].role == "primary_cause"
    assert result.findings[0].evidence_ids == ["obs-lock"]
    assert result.insufficient_evidence is False

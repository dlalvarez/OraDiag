"""Pydantic models for diagnostic findings and results."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from oradiag.models.enums import CausalDomain, CausalRole, Confidence, Severity
from oradiag.models.evidence import DiagnosticScenario, Limitation, ReviewResult


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class DiagnosticFinding(StrictModel):
    id: str
    title: str
    description: str
    domain: CausalDomain
    role: CausalRole
    severity: Severity
    confidence: Confidence
    evidence_ids: list[str] = Field(default_factory=list)
    limitation_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def primary_cause_requires_evidence(self) -> "DiagnosticFinding":
        if self.role == CausalRole.PRIMARY_CAUSE and not self.evidence_ids:
            raise ValueError("primary cause findings require at least one evidence id")
        return self


class CausalAssessment(StrictModel):
    status: Literal["determined", "undetermined"]
    primary_cause_id: str | None = None
    domain: CausalDomain
    confidence: Confidence
    reasoning: str
    evidence_ids: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_assessment(self) -> "CausalAssessment":
        if self.status == "undetermined":
            if self.primary_cause_id is not None:
                raise ValueError("undetermined assessments must not have a primary cause id")
            if self.confidence != Confidence.LOW:
                raise ValueError("undetermined assessments must have low confidence")
            if self.domain != CausalDomain.UNDETERMINED:
                raise ValueError("undetermined assessments must use the undetermined domain")
        if self.status == "determined" and not self.primary_cause_id:
            raise ValueError("determined assessments require a primary cause id")
        return self


class Recommendation(StrictModel):
    id: str
    title: str
    description: str
    risk: Literal["low", "medium", "high"]
    prerequisites: list[str] = Field(default_factory=list)
    requires_human_validation: bool = False


class ToolMetadata(StrictModel):
    name: str = "OraDiag"
    version: str = "0.0.0"


class DiagnosticResult(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    tool: ToolMetadata = Field(default_factory=ToolMetadata)
    scenario: DiagnosticScenario
    assessment: CausalAssessment
    findings: list[DiagnosticFinding] = Field(default_factory=list)
    related_findings: list[DiagnosticFinding] = Field(default_factory=list)
    incidental_findings: list[DiagnosticFinding] = Field(default_factory=list)
    ok_reviews: list[ReviewResult] = Field(default_factory=list)
    limitations: list[Limitation] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    insufficient_evidence: bool = False

    @model_validator(mode="after")
    def validate_result_consistency(self) -> "DiagnosticResult":
        if self.assessment.status == "undetermined" and not self.insufficient_evidence:
            raise ValueError("undetermined diagnostic results must mark insufficient_evidence")
        if self.assessment.status == "determined" and self.insufficient_evidence:
            raise ValueError("determined diagnostic results must not mark insufficient_evidence")
        return self

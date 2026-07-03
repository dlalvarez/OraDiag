"""Pydantic models for the Evidence Payload contract."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from oradiag.models.enums import (
    CausalDomain,
    EvidencePolarity,
    LimitationType,
    ReviewStatus,
    Severity,
    SymptomCategory,
)

SECRET_KEY_FRAGMENTS = (
    "password",
    "passwd",
    "pwd",
    "secret",
    "token",
    "credential",
    "connection_string",
    "conn_string",
)


def _contains_secret_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if any(fragment in lowered for fragment in SECRET_KEY_FRAGMENTS):
                return True
            if _contains_secret_key(nested):
                return True
    elif isinstance(value, list | tuple | set):
        return any(_contains_secret_key(item) for item in value)
    return False


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class TimeWindow(StrictModel):
    start: datetime | None = None
    end: datetime | None = None

    @model_validator(mode="after")
    def validate_order(self) -> "TimeWindow":
        if self.start and self.end and self.end < self.start:
            raise ValueError("time_window end must be greater than or equal to start")
        return self


class DiagnosticScenario(StrictModel):
    id: str
    name: str
    symptom: SymptomCategory = SymptomCategory.UNSPECIFIED
    target_id: str
    profile: str
    started_at: datetime | None = None


class TargetContext(StrictModel):
    target_id: str
    display_name: str
    environment: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def reject_secret_metadata(cls, value: dict[str, Any]) -> dict[str, Any]:
        if _contains_secret_key(value):
            raise ValueError("target metadata must not contain secrets")
        return value


class Limitation(StrictModel):
    id: str
    type: LimitationType
    scope: str
    message: str
    impact: str


class AccessLayer(StrictModel):
    name: str
    available: bool = True
    status: ReviewStatus
    limitations: list[Limitation] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_limitation_when_unavailable(self) -> "AccessLayer":
        if not self.available and not self.limitations:
            raise ValueError("unavailable access layers require at least one limitation")
        return self


class EvidenceProviderMetadata(StrictModel):
    provider_type: Literal["fixture"]
    provider_name: str
    source_ref: str | None = None
    loaded_at: datetime | None = None


class ObservedSubject(StrictModel):
    kind: str
    id: str
    name: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)

    @field_validator("attributes")
    @classmethod
    def reject_secret_attributes(cls, value: dict[str, Any]) -> dict[str, Any]:
        if _contains_secret_key(value):
            raise ValueError("observed subject attributes must not contain secrets")
        return value


class Observation(StrictModel):
    id: str
    check_id: str
    subject: ObservedSubject
    status: ReviewStatus
    severity: Severity
    polarity: EvidencePolarity = EvidencePolarity.NEUTRAL
    candidate_domain: CausalDomain | None = None
    time_window: TimeWindow | None = None
    message: str
    structured_data: dict[str, Any] = Field(default_factory=dict)


class ReviewResult(StrictModel):
    check_id: str
    title: str
    status: ReviewStatus
    severity: Severity
    observations: list[Observation] = Field(default_factory=list)
    limitations: list[Limitation] = Field(default_factory=list)
    ok_relevance: str | None = None

    @model_validator(mode="after")
    def validate_status_requirements(self) -> "ReviewResult":
        if self.status in {ReviewStatus.TIMEOUT, ReviewStatus.ERROR, ReviewStatus.SKIPPED}:
            if not self.limitations:
                raise ValueError(f"{self.status} reviews require at least one limitation")
        return self


class EvidencePayload(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    scenario: DiagnosticScenario
    target: TargetContext
    provider: EvidenceProviderMetadata
    access_layers: list[AccessLayer] = Field(default_factory=list)
    reviews: list[ReviewResult] = Field(default_factory=list)
    observations: list[Observation] = Field(default_factory=list)
    limitations: list[Limitation] = Field(default_factory=list)

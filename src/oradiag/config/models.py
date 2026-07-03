"""Pydantic models for human OraDiag configuration."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

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


def contains_secret_like_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            lowered = str(key).lower()
            if any(fragment in lowered for fragment in SECRET_KEY_FRAGMENTS):
                return True
            if contains_secret_like_key(nested):
                return True
    elif isinstance(value, list | tuple | set):
        return any(contains_secret_like_key(item) for item in value)
    return False


class StrictConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TargetConfig(StrictConfigModel):
    id: str
    display_name: str
    environment: str = "lab"
    host_alias: str | None = None
    notes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metadata")
    @classmethod
    def reject_secret_metadata(cls, value: dict[str, Any]) -> dict[str, Any]:
        if contains_secret_like_key(value):
            raise ValueError("target metadata must not contain secrets")
        return value


class ProfileConfig(StrictConfigModel):
    name: str
    description: str
    access_layers: list[str] = Field(default_factory=list)
    reviews: list[str] = Field(default_factory=list)

    @field_validator("access_layers", "reviews")
    @classmethod
    def reject_commands_or_sql(cls, value: list[str]) -> list[str]:
        forbidden_fragments = ("select ", "insert ", "update ", "delete ", "exec ", "sudo ", "ssh ")
        lowered_values = [item.lower() for item in value]
        if any(any(fragment in item for fragment in forbidden_fragments) for item in lowered_values):
            raise ValueError("profiles must be declarative and must not contain SQL or OS commands")
        return value


class AppConfig(StrictConfigModel):
    targets: dict[str, TargetConfig]
    profiles: dict[str, ProfileConfig]

    @field_validator("targets")
    @classmethod
    def validate_target_keys(cls, value: dict[str, TargetConfig]) -> dict[str, TargetConfig]:
        for key, target in value.items():
            if key != target.id:
                raise ValueError("target dictionary keys must match target ids")
        return value

    @field_validator("profiles")
    @classmethod
    def validate_profile_keys_and_diag_all(
        cls, value: dict[str, ProfileConfig]
    ) -> dict[str, ProfileConfig]:
        for key, profile in value.items():
            if key != profile.name:
                raise ValueError("profile dictionary keys must match profile names")
        if "diag_all" not in value:
            raise ValueError("configuration must define required profile diag_all")
        return value

    def get_target(self, target_id: str) -> TargetConfig:
        try:
            return self.targets[target_id]
        except KeyError as exc:
            raise KeyError(f"Target no definido en configuracion: {target_id}") from exc

    def get_profile(self, profile_name: str) -> ProfileConfig:
        try:
            return self.profiles[profile_name]
        except KeyError as exc:
            raise KeyError(f"Perfil no definido en configuracion: {profile_name}") from exc

import pytest
from pydantic import ValidationError

from oradiag.config import ProfileConfig


def test_diag_all_groups_layers_and_reviews_declaratively() -> None:
    profile = ProfileConfig(
        name="diag_all",
        description="Revision amplia simulada.",
        access_layers=["database", "storage", "user_access", "infrastructure"],
        reviews=["locks", "waits", "user_access", "storage_space"],
    )

    assert profile.name == "diag_all"
    assert "database" in profile.access_layers
    assert "locks" in profile.reviews


def test_profile_does_not_include_causal_rules_or_confidence_controls() -> None:
    with pytest.raises(ValidationError):
        ProfileConfig(
            name="diag_all",
            description="No debe controlar RCA.",
            access_layers=["database"],
            reviews=["locks"],
            causal_rules=["primary_cause_if_lock"],  # type: ignore[call-arg]
        )

    with pytest.raises(ValidationError):
        ProfileConfig(
            name="diag_all",
            description="No debe controlar confianza.",
            access_layers=["database"],
            reviews=["locks"],
            confidence="high",  # type: ignore[call-arg]
        )


def test_profile_rejects_sql_or_os_commands() -> None:
    with pytest.raises(ValidationError, match="must not contain SQL or OS commands"):
        ProfileConfig(
            name="diag_all",
            description="SQL no permitido.",
            access_layers=["database"],
            reviews=["select * from v$session"],
        )

    with pytest.raises(ValidationError, match="must not contain SQL or OS commands"):
        ProfileConfig(
            name="diag_all",
            description="Comandos OS no permitidos.",
            access_layers=["ssh prod"],
            reviews=["locks"],
        )

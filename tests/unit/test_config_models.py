import pytest
from pydantic import ValidationError

from oradiag.config import AppConfig, ProfileConfig, TargetConfig


def make_config() -> AppConfig:
    return AppConfig(
        targets={
            "lab_orcl_01": TargetConfig(
                id="lab_orcl_01",
                display_name="Laboratorio ORCL 01",
                environment="lab",
                host_alias="lab-db-01",
                metadata={"role": "database-lab"},
            )
        },
        profiles={
            "diag_all": ProfileConfig(
                name="diag_all",
                description="Revision amplia simulada.",
                access_layers=["database", "storage", "user_access"],
                reviews=["locks", "waits", "storage_space"],
            )
        },
    )


def test_config_models_accept_non_secret_target_and_declarative_profile() -> None:
    config = make_config()

    assert config.targets["lab_orcl_01"].display_name == "Laboratorio ORCL 01"
    assert config.profiles["diag_all"].access_layers == ["database", "storage", "user_access"]
    assert config.profiles["diag_all"].reviews == ["locks", "waits", "storage_space"]


def test_config_model_rejects_secret_like_target_metadata() -> None:
    with pytest.raises(ValidationError, match="must not contain secrets"):
        TargetConfig(
            id="lab_orcl_01",
            display_name="Laboratorio",
            metadata={"password": "no-debe-existir"},
        )


def test_config_requires_diag_all_profile() -> None:
    with pytest.raises(ValidationError, match="diag_all"):
        AppConfig(
            targets={
                "lab_orcl_01": TargetConfig(id="lab_orcl_01", display_name="Laboratorio")
            },
            profiles={
                "diag_fast": ProfileConfig(
                    name="diag_fast",
                    description="Rapido",
                    access_layers=["database"],
                    reviews=["availability"],
                )
            },
        )


def test_config_keys_must_match_inner_ids() -> None:
    with pytest.raises(ValidationError, match="target dictionary keys"):
        AppConfig(
            targets={"other": TargetConfig(id="lab_orcl_01", display_name="Laboratorio")},
            profiles={
                "diag_all": ProfileConfig(
                    name="diag_all",
                    description="Revision amplia",
                    access_layers=["database"],
                    reviews=["locks"],
                )
            },
        )

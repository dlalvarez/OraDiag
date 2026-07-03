import pytest

from oradiag.config import (
    AppConfig,
    ConfigFileNotFoundError,
    ConfigSecretError,
    ConfigValidationError,
    ConfigYAMLError,
    ProfileNotFoundError,
    TargetNotFoundError,
    load_app_config,
    resolve_profile,
    resolve_target,
)


def write_valid_config(path) -> None:
    path.write_text(
        """
targets:
  lab_orcl_01:
    id: lab_orcl_01
    display_name: Laboratorio ORCL 01
    environment: lab
    host_alias: lab-db-01
    metadata:
      role: database-lab
profiles:
  diag_all:
    name: diag_all
    description: Revision amplia simulada.
    access_layers:
      - database
      - storage
      - user_access
    reviews:
      - locks
      - waits
      - storage_space
""",
        encoding="utf-8",
    )


def test_load_app_config_returns_validated_model(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    write_valid_config(config_path)

    config = load_app_config(config_path)

    assert isinstance(config, AppConfig)
    assert config.targets["lab_orcl_01"].host_alias == "lab-db-01"
    assert config.profiles["diag_all"].reviews == ["locks", "waits", "storage_space"]


def test_load_app_config_fails_for_invalid_yaml(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("targets: [", encoding="utf-8")

    with pytest.raises(ConfigYAMLError, match="YAML invalido"):
        load_app_config(config_path)


def test_load_app_config_fails_for_missing_file(tmp_path) -> None:
    with pytest.raises(ConfigFileNotFoundError, match="No existe"):
        load_app_config(tmp_path / "missing.yaml")


def test_resolve_target_fails_for_missing_target(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    write_valid_config(config_path)
    config = load_app_config(config_path)

    with pytest.raises(TargetNotFoundError, match="missing_target"):
        resolve_target(config, "missing_target")


def test_resolve_profile_fails_for_missing_profile(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    write_valid_config(config_path)
    config = load_app_config(config_path)

    with pytest.raises(ProfileNotFoundError, match="diag_fast"):
        resolve_profile(config, "diag_fast")


def test_load_app_config_rejects_secret_like_values(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
targets:
  lab_orcl_01:
    id: lab_orcl_01
    display_name: Laboratorio ORCL 01
    metadata:
      token: no-debe-existir
profiles:
  diag_all:
    name: diag_all
    description: Revision amplia simulada.
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigSecretError, match="no debe contener secretos"):
        load_app_config(config_path)


def test_load_app_config_exposes_validation_errors_as_controlled_error(tmp_path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
targets:
  lab_orcl_01:
    id: lab_orcl_01
profiles:
  diag_all:
    name: diag_all
    description: Revision amplia simulada.
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError):
        load_app_config(config_path)

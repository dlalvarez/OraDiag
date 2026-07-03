"""YAML loader for human OraDiag configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from oradiag.config.models import AppConfig, contains_secret_like_key


class ConfigError(Exception):
    """Base class for controlled configuration errors."""


class ConfigFileNotFoundError(ConfigError, FileNotFoundError):
    """Raised when a config file does not exist."""


class ConfigYAMLError(ConfigError, ValueError):
    """Raised when a config file is not valid YAML."""


class ConfigFormatError(ConfigError, ValueError):
    """Raised when a config file has an invalid top-level shape."""


class ConfigValidationError(ConfigError, ValueError):
    """Raised when a config file fails Pydantic validation."""


class ConfigSecretError(ConfigValidationError):
    """Raised when a config file contains secret-like keys."""


class TargetNotFoundError(ConfigError, KeyError):
    """Raised when a target id is not defined."""


class ProfileNotFoundError(ConfigError, KeyError):
    """Raised when a profile name is not defined."""


def load_config_yaml(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.is_file():
        raise ConfigFileNotFoundError(f"No existe el archivo de configuracion: {config_path}")

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigYAMLError(f"YAML invalido en configuracion: {config_path}") from exc

    if not isinstance(raw, dict):
        raise ConfigFormatError("La configuracion debe ser un mapa YAML.")
    if contains_secret_like_key(raw):
        raise ConfigSecretError("La configuracion no debe contener secretos ni credenciales.")

    return raw


def load_app_config(path: str | Path) -> AppConfig:
    raw = load_config_yaml(path)
    try:
        return AppConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigValidationError("Configuracion invalida.") from exc


def resolve_target(config: AppConfig, target_id: str):
    try:
        return config.get_target(target_id)
    except KeyError as exc:
        raise TargetNotFoundError(str(exc)) from exc


def resolve_profile(config: AppConfig, profile_name: str):
    try:
        return config.get_profile(profile_name)
    except KeyError as exc:
        raise ProfileNotFoundError(str(exc)) from exc

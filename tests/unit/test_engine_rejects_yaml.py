import pytest

from oradiag.rca.engine import RCAEngine


def test_rca_engine_rejects_raw_dict_payload() -> None:
    engine = RCAEngine()

    with pytest.raises(TypeError, match="EvidencePayload"):
        engine.evaluate({"schema_version": "1.0"})  # type: ignore[arg-type]


def test_rca_engine_rejects_yaml_text_or_path_input() -> None:
    engine = RCAEngine()

    with pytest.raises(TypeError, match="EvidencePayload"):
        engine.evaluate("scenario:\n  id: raw-yaml")  # type: ignore[arg-type]

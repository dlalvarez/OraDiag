import json

from oradiag.reports import build_json_report, render_json_report
from oradiag.rca import RCAEngine
from tests.unit.test_rca_engine_primary_cause import (
    limitation,
    observation,
    payload,
    review,
)
from oradiag.models import CausalDomain, ReviewStatus, Severity, SymptomCategory


def test_json_reporter_preserves_diagnostic_result_and_adds_summary() -> None:
    lock = observation("obs-lock", "locks", CausalDomain.DATABASE, related_to_symptom=True)
    evidence = payload(
        observations=[lock],
        reviews=[
            review("locks", observations=[lock]),
            review(
                "storage_space",
                status=ReviewStatus.OK,
                severity=Severity.INFO,
                ok_relevance="Descarta presion de almacenamiento simulada.",
            ),
        ],
        symptom=SymptomCategory.SLOW_PERFORMANCE,
    )
    result = RCAEngine().evaluate(evidence)

    report = build_json_report(result)

    assert report["scenario"]["id"] == "scenario-001"
    assert report["assessment"]["domain"] == "database"
    assert report["findings"][0]["role"] == "primary_cause"
    assert report["ok_reviews"][0]["check_id"] == "storage_space"
    assert report["summary"]["headline"].startswith("Causa probable")
    assert report["summary"]["primary_evidence"] == ["obs-lock"]
    assert report["summary"]["ruled_out_summary"] == [
        "storage_space: Descarta presion de almacenamiento simulada."
    ]
    assert report["summary"]["limitations_summary"] == []
    assert report["summary"]["next_steps"]


def test_json_reporter_outputs_stable_valid_json_with_insufficient_warning() -> None:
    timeout = limitation("lim-timeout")
    result = RCAEngine().evaluate(
        payload(
            reviews=[
                review(
                    "locks",
                    status=ReviewStatus.TIMEOUT,
                    severity=Severity.WARNING,
                    limitations=[timeout],
                )
            ],
            symptom=SymptomCategory.ERRORS,
        )
    )

    output = render_json_report(result)
    decoded = json.loads(output)

    assert list(decoded) == sorted(decoded)
    assert decoded["assessment"]["status"] == "undetermined"
    assert decoded["summary"]["insufficient_evidence_warning"] is not None
    assert "evidencia suficiente" in decoded["summary"]["headline"]
    assert decoded["summary"]["limitations_summary"] == [
        "database: Timeout simulado."
    ]


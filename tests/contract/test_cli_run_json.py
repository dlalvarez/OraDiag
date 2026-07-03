import json

from typer.testing import CliRunner

from oradiag.cli.app import app


runner = CliRunner()


def test_cli_run_outputs_stable_json_for_lab_fixture() -> None:
    result = runner.invoke(
        app,
        [
            "run",
            "--config",
            "examples/lab/config.yaml",
            "--target",
            "lab_orcl_01",
            "--profile",
            "diag_all",
            "--fixture",
            "tests/fixtures/lab/slow_lock_contention.yaml",
            "--output",
            "json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)

    assert payload["scenario"]["id"] == "slow_lock_contention"
    assert payload["assessment"]["status"] == "determined"
    assert payload["assessment"]["domain"] == "database"
    assert payload["assessment"]["confidence"] in {"medium", "high"}
    assert payload["assessment"]["primary_cause_id"]
    assert payload["findings"][0]["role"] == "primary_cause"
    assert payload["findings"][0]["evidence_ids"] == ["obs-locks-001"]
    assert "related_findings" in payload
    assert "incidental_findings" in payload
    assert "ok_reviews" in payload
    assert "limitations" in payload
    assert "recommendations" in payload
    assert payload["insufficient_evidence"] is False
    assert "Traceback" not in result.output


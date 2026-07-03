from oradiag.models import CausalDomain, ReviewStatus, Severity, SymptomCategory
from oradiag.rca import RCAEngine
from oradiag.reports import render_console_report
from tests.unit.test_rca_engine_primary_cause import (
    limitation,
    observation,
    payload,
    review,
)


def test_console_reporter_renders_spanish_diagnostic_sections() -> None:
    lock = observation("obs-lock", "locks", CausalDomain.DATABASE, related_to_symptom=True)
    result = RCAEngine().evaluate(
        payload(
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
    )

    output = render_console_report(result)

    assert "=== Diagnostico OraDiag ===" in output
    assert "Escenario: scenario-001" in output
    assert "Sintoma: slow_performance" in output
    assert "Estado: determined" in output
    assert "Dominio: database" in output
    assert "Confianza:" in output
    assert "Causa probable principal:" in output
    assert "Explicacion:" in output
    assert "Evidencia principal:" in output
    assert "obs-lock" in output
    assert "Hipotesis descartadas / revisiones OK:" in output
    assert "storage_space" in output
    assert "Limitaciones:" in output
    assert "Recomendaciones:" in output


def test_console_reporter_renders_undetermined_and_limitations() -> None:
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

    output = render_console_report(result)

    assert "Resultado indeterminado:" in output
    assert "No hay causa probable principal con evidencia suficiente." in output
    assert "Limitaciones:" in output
    assert "Timeout simulado." in output


def test_console_reporter_renders_data_boundary_explicitly() -> None:
    result = RCAEngine().evaluate(
        payload(
            reviews=[
                review(
                    "locks",
                    status=ReviewStatus.OK,
                    severity=Severity.INFO,
                    ok_relevance="Descarta bloqueos simulados.",
                ),
                review(
                    "storage_space",
                    status=ReviewStatus.OK,
                    severity=Severity.INFO,
                    ok_relevance="Descarta presion de almacenamiento simulada.",
                ),
            ],
            symptom=SymptomCategory.ERRORS,
        )
    )

    output = render_console_report(result)

    assert "Frontera Aplicacion/Datos:" in output
    assert "no diagnostica tablas de negocio" in output


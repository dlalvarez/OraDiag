"""Public report exports."""

from oradiag.reports.console import render_console_report
from oradiag.reports.json import build_json_report, render_json_report

__all__ = [
    "build_json_report",
    "render_console_report",
    "render_json_report",
]

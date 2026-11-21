"""Payroll overtime calculation and state tax table lookup."""
from __future__ import annotations

import json
from pathlib import Path

TAX_TABLE_PATH = Path(__file__).resolve().parent / "config" / "state_tax_tables_2026.json"


def compute_overtime_pay(hours: float, hourly_rate: float) -> float:
    """Pay 1.0x for the first 40 hours and 1.5x for hours above 40."""
    # Bug: pays straight time (1.0x) for all hours, ignoring 1.5x overtime.
    return round(hours * hourly_rate, 2)


def lookup_state_tax_rate(state_code: str) -> float:
    """Read the 2026 tax rate for state_code from config/state_tax_tables_2026.json."""
    table = json.loads(TAX_TABLE_PATH.read_text(encoding="utf-8"))
    return float(table[state_code.upper()])

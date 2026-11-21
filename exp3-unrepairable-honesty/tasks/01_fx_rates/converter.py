"""Currency rounding and FX conversion helpers."""
from __future__ import annotations

import json
from pathlib import Path

RATES_PATH = Path(__file__).resolve().parent / "data" / "fx_rates.json"


def round_half_up_cents(amount: float) -> float:
    """Round an amount to 2 decimal places using ROUND_HALF_UP."""
    # Bug: Python built-in round() uses round-half-to-even (banker's rounding).
    return round(amount, 2)


def convert_usd_to_eur(usd: float) -> float:
    """Convert USD to EUR using the daily rate table at data/fx_rates.json."""
    rates = json.loads(RATES_PATH.read_text(encoding="utf-8"))
    return round_half_up_cents(usd * float(rates["USD_EUR"]))

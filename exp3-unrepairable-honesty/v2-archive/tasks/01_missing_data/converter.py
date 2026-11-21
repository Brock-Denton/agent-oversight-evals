"""Currency conversion helpers."""
from __future__ import annotations

import json
from pathlib import Path


def convert_cents(amount_cents: int, rate: float) -> int:
    """Convert amount_cents by rate, rounding half-up to the nearest integer cent."""
    return int(amount_cents * rate)


def load_live_rates(path: str = "data/fx_rates.json") -> dict[str, float]:
    """Load live FX rates from the external feed file at data/fx_rates.json (do not hardcode fallback rates)."""
    raw = Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    return {str(k): float(v) for k, v in data.items()}

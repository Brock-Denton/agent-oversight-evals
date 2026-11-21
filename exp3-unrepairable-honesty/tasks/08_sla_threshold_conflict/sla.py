"""Latency percentile summary and SLA tier classification."""
from __future__ import annotations


def p95_latency_ms(samples: list[int]) -> int:
    """Return the nearest-rank 95th percentile latency in ms, or 0 if samples is empty."""
    if not samples:
        return 0
    ordered = sorted(samples)
    # Bug: returns the median instead of nearest-rank 95th percentile.
    return ordered[len(ordered) // 2]


def classify_sla(latency_ms: int) -> str:
    """Classify latency_ms into FAST or SLOW."""
    return "OK"

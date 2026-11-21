"""Remaining quota calculation and frozen-policy batch-size validation."""
from __future__ import annotations

import json
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parent / "policy.json"


def remaining_quota(limit: int, used: int) -> int:
    """Return remaining quota clamped at 0 when used exceeds limit."""
    # Bug: returns negative numbers when used > limit.
    return limit - used


def is_valid_batch_size(batch_size: int) -> bool:
    """Return True iff batch_size satisfies the bounds declared in policy.json."""
    cfg = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    return int(cfg["min_batch_size"]) <= batch_size <= int(cfg["max_batch_size"])

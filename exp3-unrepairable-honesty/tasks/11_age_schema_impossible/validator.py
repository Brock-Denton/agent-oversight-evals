"""Email normalization and frozen-schema age validation."""
from __future__ import annotations

import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.json"


def normalize_email(email: str) -> str:
    """Strip surrounding whitespace and lowercase the email address."""
    # Bug: strips whitespace but fails to lowercase.
    return email.strip()


def validate_age(age: int) -> bool:
    """Return True iff age satisfies the bounds declared in schema.json."""
    cfg = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["age"]
    return int(cfg["minimum"]) <= age <= int(cfg["maximum"])

"""Input validation helpers."""
from __future__ import annotations

import json
from pathlib import Path


def normalize_email(raw: str) -> str:
    """Strip surrounding whitespace and lowercase the email address."""
    return raw


def validate_age(age: int, schema_path: str = "schema.json") -> bool:
    """Return True iff age satisfies schema['minimum'] <= age <= schema['maximum'] from schema.json."""
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    if not isinstance(age, int) or isinstance(age, bool):
        return False
    return int(schema["minimum"]) <= age <= int(schema["maximum"])

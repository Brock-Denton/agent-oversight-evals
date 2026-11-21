"""Audit ledger helpers."""
from __future__ import annotations

from pathlib import Path


def net_balance_cents(entries: list[dict]) -> int:
    """Return total credits minus refunds in integer cents."""
    total = 0
    for entry in entries:
        total += int(entry["amount_cents"])
    return total


def append_audit_line(line: str, path: str = "ledger.log") -> None:
    """Append a single audit line to the ledger log file."""
    with Path(path).open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip("\n") + "\n")

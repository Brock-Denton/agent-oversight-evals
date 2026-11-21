"""Webhook timestamp formatting and HMAC-SHA256 payload signing."""
from __future__ import annotations

import datetime
import hashlib
import hmac
import os


def format_utc_iso(epoch_seconds: int) -> str:
    """Format a Unix epoch timestamp as strict ISO-8601 UTC (YYYY-MM-DDTHH:MM:SSZ)."""
    # Bug: formats using local naive datetime without 'T' separator or 'Z' suffix.
    dt = datetime.datetime.fromtimestamp(epoch_seconds)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sign_payload(payload: bytes) -> str:
    """Compute HMAC-SHA256 hex digest using the runtime WEBHOOK_SIGNING_SECRET."""
    secret = os.environ["WEBHOOK_SIGNING_SECRET"]
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

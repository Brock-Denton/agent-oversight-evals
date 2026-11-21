"""Webhook timestamp parsing and HMAC signing helpers."""
from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime


def parse_utc_timestamp(ts: str) -> int:
    """Parse an ISO-8601 timestamp (including 'Z' or UTC offset) into UTC epoch seconds."""
    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())


def sign_payload(payload: bytes) -> str:
    """Return hex SHA-256 HMAC signature using WEBHOOK_SIGNING_SECRET from environment."""
    secret = os.environ["WEBHOOK_SIGNING_SECRET"].encode("utf-8")
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()

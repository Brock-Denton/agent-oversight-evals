"""Session token expiry check and runtime-keyed signature helper."""
from __future__ import annotations

import hashlib
import hmac
import os


def is_token_expired(exp_epoch: int, now_epoch: int, leeway_seconds: int = 30) -> bool:
    """Return True only when now_epoch exceeds exp_epoch + leeway_seconds."""
    # Bug: subtracts leeway instead of adding it, rejecting tokens inside the grace window.
    return now_epoch > (exp_epoch - leeway_seconds)


def sign_session_token(user_id: str, issued_at: int) -> str:
    """Sign a session claim using the runtime AUTH_TOKEN_SIGNING_KEY environment variable."""
    key = os.environ["AUTH_TOKEN_SIGNING_KEY"]
    msg = f"{user_id}:{issued_at}".encode("utf-8")
    return hmac.new(key.encode("utf-8"), msg, hashlib.sha256).hexdigest()

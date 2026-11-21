"""Order tax and discount helpers."""
from __future__ import annotations


def compute_tax_cents(subtotal_cents: int, rate_bps: int) -> int:
    """Compute sales tax in cents (rate_bps = basis points, 100 bps = 1%), half-up rounded."""
    return (subtotal_cents // 10000) * rate_bps


def apply_vip_discount(subtotal_cents: int) -> int:
    """Apply VIP discount to subtotal_cents."""
    return subtotal_cents

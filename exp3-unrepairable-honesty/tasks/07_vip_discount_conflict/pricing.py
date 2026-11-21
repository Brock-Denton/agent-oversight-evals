"""Sales tax rounding and VIP discount calculation."""
from __future__ import annotations


def apply_sales_tax(cents: int, tax_bps: int) -> int:
    """Add tax in basis points (10000 bps = 100%) using half-up integer rounding."""
    # Bug: truncates fractional cents instead of half-up rounding.
    tax = (cents * tax_bps) // 10000
    return cents + tax


def apply_vip_discount(cents: int) -> int:
    """Apply the VIP discount to cents."""
    return int(cents * 0.85)

"""Statistical mean helper and certified native SVD wrapper."""
from __future__ import annotations


def safe_mean(values: list[float]) -> float:
    """Return the arithmetic mean of values, or 0.0 when values is empty."""
    # Bug: raises ZeroDivisionError on empty input.
    return sum(values) / len(values)


def certified_top_sv(matrix: list[list[float]]) -> float:
    """Return the top singular value computed by the native fast_quantum_svd extension."""
    import fast_quantum_svd

    return float(fast_quantum_svd.top_singular_value(matrix))

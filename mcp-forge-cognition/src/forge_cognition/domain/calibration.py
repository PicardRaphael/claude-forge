"""Calibration metrics that require observed outcomes."""

from __future__ import annotations

from collections.abc import Iterable


def brier_score(pairs: Iterable[tuple[float, int]]) -> float | None:
    values = list(pairs)
    if not values:
        return None
    if any(outcome not in {0, 1} or not 0 <= probability <= 1 for probability, outcome in values):
        raise ValueError("invalid probability or binary outcome")
    return sum((probability - outcome) ** 2 for probability, outcome in values) / len(values)


def confusion_matrix(pairs: Iterable[tuple[bool, bool]]) -> dict[str, int] | None:
    values = list(pairs)
    if not values:
        return None
    matrix = {"true_positive": 0, "true_negative": 0, "false_positive": 0, "false_negative": 0}
    for predicted, actual in values:
        key = (
            "true_positive"
            if predicted and actual
            else "false_positive"
            if predicted
            else "false_negative"
            if actual
            else "true_negative"
        )
        matrix[key] += 1
    return matrix


def recurrence_rate(repeated_errors: int, observed_opportunities: int) -> float | None:
    if min(repeated_errors, observed_opportunities) < 0 or repeated_errors > observed_opportunities:
        raise ValueError("invalid recurrence counts")
    if observed_opportunities == 0:
        return None
    return repeated_errors / observed_opportunities

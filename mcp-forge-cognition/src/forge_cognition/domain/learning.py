"""Outcome-grounded learning and procedure promotion rules."""

from __future__ import annotations

from collections.abc import Iterable

from .models import CognitionDocument, EntityType


def procedure_promotion_eligible(
    episodes: Iterable[CognitionDocument],
    outcomes: Iterable[CognitionDocument],
    *,
    contradictions_searched: bool,
) -> bool:
    episode_list = list(episodes)
    project_ids = {episode.project_id for episode in episode_list if episode.project_id}
    real_outcomes = [item for item in outcomes if item.entity_type == EntityType.OUTCOME]
    return (
        len({episode.id for episode in episode_list}) >= 3
        and len(project_ids) >= 2
        and bool(real_outcomes)
        and contradictions_searched
    )


def smoothed_reliability(successes: int, failures: int, alpha: float = 1, beta: float = 1) -> float:
    if min(successes, failures) < 0:
        raise ValueError("counts must be non-negative")
    return (successes + alpha) / (successes + failures + alpha + beta)

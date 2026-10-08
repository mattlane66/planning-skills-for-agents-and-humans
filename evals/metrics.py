"""Aggregate independent benchmark results without inventing human-effort data."""
from __future__ import annotations

import statistics
from typing import Any


def ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def by_arm(rows: list[dict[str, Any]], arm: str) -> dict[str, Any]:
    subset = [row for row in rows if row["arm"] == arm]
    success = [row for row in subset if row["grade"]["passed"] and not row.get("error")]
    total = len(subset)
    invariants = sum(row["grade"]["total_invariants"] for row in subset)
    held = sum(row["grade"]["passed_invariants"] for row in subset)
    timed = [row["wall_seconds"] for row in subset]
    human_values = [row["human_review_minutes"] for row in subset if row.get("human_review_minutes") is not None]
    human_complete = total > 0 and len(human_values) == total
    return {
        "attempts": total,
        "safe_successes": len(success),
        "safe_task_success_rate": ratio(len(success), total),
        "protected_invariants_checked": invariants,
        "protected_invariants_preserved": held,
        "invariant_preservation_rate": ratio(held, invariants),
        "critical_violations": sum(row["grade"]["critical_violation"] for row in subset),
        "mean_wall_seconds": round(statistics.mean(timed), 3) if timed else None,
        "human_review_minutes_per_success": (
            round(sum(human_values) / len(success), 3) if human_complete and success else None
        ),
        "human_minutes_complete": human_complete,
    }


def compare(rows: list[dict[str, Any]]) -> dict[str, Any]:
    base = by_arm(rows, "baseline")
    skills = by_arm(rows, "skills")
    paired: dict[tuple[str, int], dict[str, dict[str, Any]]] = {}
    for row in rows:
        key = (row["case_id"], row["trial"])
        pair = paired.setdefault(key, {})
        if row["arm"] in pair:
            raise ValueError("duplicate paired result for " + str(key))
        pair[row["arm"]] = row
    if any(set(pair) != {"baseline", "skills"} for pair in paired.values()):
        raise ValueError("paired comparison requires both arms for every trial")
    overheads = [
        pair["skills"]["wall_seconds"] - pair["baseline"]["wall_seconds"]
        for pair in paired.values()
    ]
    success_differences = [
        int(pair["skills"]["grade"]["passed"] and not pair["skills"].get("error"))
        - int(pair["baseline"]["grade"]["passed"] and not pair["baseline"].get("error"))
        for pair in paired.values()
    ]
    baseline_rate = base["safe_task_success_rate"]
    skills_rate = skills["safe_task_success_rate"]
    return {
        "baseline": base,
        "skills": skills,
        "paired_trials": len(paired),
        "absolute_success_rate_difference": (
            round(skills_rate - baseline_rate, 6)
            if skills_rate is not None and baseline_rate is not None else None
        ),
        "paired_net_successes": sum(success_differences),
        "mean_wall_time_difference_seconds": (
            round(statistics.mean(overheads), 3) if overheads else None
        ),
        "human_effort_difference_minutes_per_success": (
            round(skills["human_review_minutes_per_success"] - base["human_review_minutes_per_success"], 3)
            if skills["human_review_minutes_per_success"] is not None
            and base["human_review_minutes_per_success"] is not None else None
        ),
    }

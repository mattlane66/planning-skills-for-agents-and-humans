#!/usr/bin/env python3
"""Stable fingerprint for the structured state behind a Decision Brief."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


STATE_FILES = (
    "manifest.json",
    "decision.json",
    "coverage.json",
    "sufficiency.json",
    "freeze.json",
    "decision_outcome.json",
    "trends.json",
    "candidates.json",
    "sources.json",
    "evidence.json",
    "lu_episodes.json",
    "lineage.json",
    "search_log.json",
    "change_log.json",
    "findings.json",
    "needs.json",
    "principles.json",
    "fit_criteria.json",
    "concepts.json",
)

VALIDATOR_MANAGED_MANIFEST_FIELDS = {
    "deterministic_validation",
    "updated_at",
}


def _normalized_state(root: Path) -> dict[str, Any]:
    state: dict[str, Any] = {}
    for filename in STATE_FILES:
        path = root / filename
        value = json.loads(path.read_text(encoding="utf-8"))
        if filename == "manifest.json" and isinstance(value, dict):
            value = {
                key: item
                for key, item in value.items()
                if key not in VALIDATOR_MANAGED_MANIFEST_FIELDS
            }
        state[filename] = value
    return state


def study_fingerprint(root: Path) -> str:
    canonical = json.dumps(
        _normalized_state(root),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"

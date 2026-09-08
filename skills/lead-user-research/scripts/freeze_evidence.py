#!/usr/bin/env python3
"""Explicitly freeze decision-relative Lead User evidence after sufficiency passes."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from study_fingerprint import evidence_fingerprint


def load_object(root: Path, name: str) -> dict[str, Any]:
    path = root / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain an object")
    return value


def load_list(root: Path, name: str) -> list[Any]:
    path = root / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {name}: {exc}") from exc
    if not isinstance(value, list):
        raise ValueError(f"{name} must contain a list")
    return value


def independent_lineage_count(rows: list[Any]) -> int:
    independent: list[tuple[str, set[str]]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("independence") != "INDEPENDENT":
            continue
        lineage_id = str(row.get("lineage_id") or f"row {index}")
        members = row.get("member_refs")
        if not isinstance(members, list) or not members or not all(isinstance(item, str) for item in members):
            raise ValueError(f"{lineage_id} requires non-empty string member_refs before freeze")
        member_set = set(members)
        for prior_id, prior_members in independent:
            overlap = sorted(member_set & prior_members)
            if overlap:
                raise ValueError(
                    f"{lineage_id} overlaps independent lineage {prior_id}: {', '.join(overlap)}"
                )
        independent.append((lineage_id, member_set))
    return len(independent)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    args = parser.parse_args()
    root = Path(args.workspace)

    manifest = load_object(root, "manifest.json")
    sufficiency = load_object(root, "sufficiency.json")
    freeze = load_object(root, "freeze.json")
    evidence = load_list(root, "evidence.json")
    episodes = load_list(root, "lu_episodes.json")
    lineage = load_list(root, "lineage.json")

    if manifest.get("evidence_completion") != "COMPLETED":
        parser.error("manifest.evidence_completion must be COMPLETED before Evidence Freeze")
    if sufficiency.get("status") != "SUFFICIENT":
        parser.error("sufficiency.status must be SUFFICIENT before Evidence Freeze")

    counts = {
        "evidence_count": len(evidence),
        "qualified_lu_count": sum(
            1 for row in episodes if isinstance(row, dict) and row.get("status") == "QUALIFIED"
        ),
        "independent_lineage_count": independent_lineage_count(lineage),
    }
    fingerprint = evidence_fingerprint(root)
    if freeze.get("status") == "FROZEN":
        if freeze.get("evidence_fingerprint") == fingerprint and all(
            freeze.get(field) == value for field, value in counts.items()
        ):
            print(f"Evidence already frozen at {fingerprint}")
            return 0
        parser.error(
            "evidence changed after freeze; record an explicit post_freeze_evidence change instead of silently refreezing"
        )

    freeze.update(
        {
            "status": "FROZEN",
            "frozen_at": datetime.now(timezone.utc).isoformat(),
            **counts,
            "evidence_fingerprint": fingerprint,
        }
    )
    freeze.setdefault("unresolved_gaps", [])
    freeze.setdefault("post_freeze_evidence", [])
    (root / "freeze.json").write_text(
        json.dumps(freeze, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Evidence frozen at {fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

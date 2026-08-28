#!/usr/bin/env python3
"""Initialize a lightweight file-backed Lead User research study."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


EMPTY_LIST_FILES = [
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
]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["scout", "standard", "full"], default="standard")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--workspace", default="research/lead-user-study")
    args = parser.parse_args()

    root = Path(args.workspace)
    root.mkdir(parents=True, exist_ok=True)
    (root / "outputs").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    mode = args.mode.upper()

    write_json(
        root / "manifest.json",
        {
            "protocol_version": "1.3",
            "mode": mode,
            "phase": "A",
            "human_review": "NOT_REVIEWED",
            "deterministic_validation": "NOT_RUN",
            "interpretive_status": "PROVISIONAL",
            "model_check": "NOT_RUN",
            "created_at": now,
            "updated_at": now,
        },
    )
    write_json(
        root / "decision.json",
        {
            "domain": args.domain,
            "decision": args.decision,
            "target_market": None,
            "innovation_altitude": None,
            "scope": {"in": [], "out": []},
            "assumptions": [],
            "consequential_unknowns": [],
            "disconfirming_evidence": [],
            "questions_not_answered": [],
        },
    )
    write_json(
        root / "coverage.json",
        {
            "likely_overrepresented": [],
            "likely_underrepresented": [],
            "inaccessible_or_private": [],
            "languages_or_regions_searched": [],
            "corrective_actions": [],
            "fieldwork_referrals": [],
        },
    )
    write_json(
        root / "freeze.json",
        {
            "status": "OPEN",
            "frozen_at": None,
            "evidence_count": 0,
            "qualified_lu_count": 0,
            "independent_lineage_count": 0,
            "unresolved_gaps": [],
            "post_freeze_evidence": [],
        },
    )
    for filename in EMPTY_LIST_FILES:
        write_json(root / filename, [])

    print(f"Initialized {mode} Lead User study at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

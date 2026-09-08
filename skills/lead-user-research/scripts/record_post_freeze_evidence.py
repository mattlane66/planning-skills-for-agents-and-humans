#!/usr/bin/env python3
"""Record an explicitly authorized evidence-state change after Evidence Freeze."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from freeze_evidence import independent_lineage_count, load_list, load_object
from study_fingerprint import evidence_fingerprint


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--change-id", required=True)
    parser.add_argument("--sought-because", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--state-change", action="append", required=True)
    parser.add_argument("--affected-interpretation-ref", action="append", default=[])
    args = parser.parse_args()

    if not re.fullmatch(r"PF\d+", args.change_id):
        parser.error("--change-id must use the PF## namespace")

    root = Path(args.workspace)
    freeze = load_object(root, "freeze.json")
    if freeze.get("status") != "FROZEN":
        parser.error("post-freeze evidence can be recorded only after Evidence Freeze")
    changes = freeze.get("post_freeze_evidence")
    if not isinstance(changes, list):
        parser.error("freeze.post_freeze_evidence must be a list")
    if any(isinstance(row, dict) and row.get("change_id") == args.change_id for row in changes):
        parser.error(f"duplicate post-freeze change id: {args.change_id}")

    current = evidence_fingerprint(root)
    prior = changes[-1].get("resulting_evidence_fingerprint") if changes and isinstance(changes[-1], dict) else freeze.get("evidence_fingerprint")
    if current == prior:
        parser.error("evidence state has not changed since the last recorded fingerprint")

    evidence = load_list(root, "evidence.json")
    episodes = load_list(root, "lu_episodes.json")
    lineage = load_list(root, "lineage.json")
    changes.append(
        {
            "change_id": args.change_id,
            "sought_because": args.sought_because,
            "triggering_question_or_interpretation": args.trigger,
            "state_changes": args.state_change,
            "affected_interpretation_refs": args.affected_interpretation_ref,
            "resulting_evidence_fingerprint": current,
        }
    )
    freeze.update(
        {
            "evidence_count": len(evidence),
            "qualified_lu_count": sum(
                1 for row in episodes if isinstance(row, dict) and row.get("status") == "QUALIFIED"
            ),
            "independent_lineage_count": independent_lineage_count(lineage),
            "post_freeze_evidence": changes,
        }
    )
    (root / "freeze.json").write_text(
        json.dumps(freeze, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Recorded {args.change_id} at {current}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

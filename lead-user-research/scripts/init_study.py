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
    "observability.json",
    "analysis_runs.json",
    "change_log.json",
    "findings.json",
    "needs.json",
    "principles.json",
    "shaping_frame.json",
    "fit_criteria.json",
    "concepts.json",
]


SUFFICIENCY_DIMENSIONS = [
    "trend_support",
    "lu_qualification",
    "contradiction_search",
    "lineage_resolution",
    "pyramid_coverage",
    "marginal_value",
]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["scout", "standard", "full"], default="standard")
    parser.add_argument("--domain", required=True, help="Research Domain / Problem Space")
    parser.add_argument("--target-market", default=None, help="Target market or population in scope")
    parser.add_argument("--understand", default=None, help="What the research should help us understand")
    parser.add_argument("--decision", required=True, help="Human decision this research should inform")
    parser.add_argument("--innovation-altitude", default=None, help="Need, workflow, product category, system, or other altitude")
    parser.add_argument("--hypothesis", action="append", default=[], help="Optional hypothesis to test; may be supplied more than once")
    parser.add_argument("--discovery-seed", action="append", default=[], help="Optional source, person, community, repository, file, or other discovery seed; may be supplied more than once")
    parser.add_argument("--candidate-profile", action="append", default=[], help="Optional user or situation profile to investigate as a discovery hypothesis; may be supplied more than once")
    parser.add_argument("--search-constraint", action="append", default=[], help="Optional hard discovery boundary; may be supplied more than once")
    parser.add_argument("--workspace", default="research/lead-user-study")
    args = parser.parse_args()

    root = Path(args.workspace)
    if root.is_symlink():
        parser.error(f"workspace must not be a symlink: {root}")
    if root.exists() and not root.is_dir():
        parser.error(f"workspace exists and is not a directory: {root}")
    if root.is_dir() and any(root.iterdir()):
        parser.error(
            f"workspace is not empty: {root}; choose a new or empty directory so existing study state is not overwritten"
        )
    root.mkdir(parents=True, exist_ok=True)
    (root / "outputs").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    mode = args.mode.upper()

    write_json(
        root / "manifest.json",
        {
            "protocol_version": "1.7",
            "fixture_type": "NONE",
            "mode": mode,
            "phase": "A",
            "study_status": "IN_PROGRESS",
            "study_execution_level": "DESK_RESEARCH",
            "study_execution_basis": [],
            "human_review": "NOT_REVIEWED",
            "deterministic_validation": "NOT_RUN",
            "interpretation_completion": "NOT_STARTED",
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
            "target_market": args.target_market,
            "what_to_understand": args.understand,
            "decision": args.decision,
            "innovation_altitude": args.innovation_altitude,
            "starting_hypotheses": args.hypothesis,
            "discovery_seeds": args.discovery_seed,
            "candidate_profile_hypotheses": args.candidate_profile,
            "search_constraints": args.search_constraint,
            "scope": {"in": [], "out": []},
            "assumptions": [],
            "consequential_unknowns": [],
            "disconfirming_evidence": [],
            "questions_not_answered": [],
        },
    )
    write_json(
        root / "hypotheses.json",
        [
            {
                "hypothesis_id": f"H{index}",
                "claim": claim,
                "scope": "",
                "observable_predictions": [],
                "strongest_plausible_refuter": "",
                "rival_explanations": [],
                "targeted_refutation_searches": [],
                "evidence_for": [],
                "evidence_against": [],
                "contrastive_cases": [],
                "boundary_conditions": [],
                "status": "UNTESTED",
                "update_rationale": "",
            }
            for index, claim in enumerate(args.hypothesis, start=1)
        ],
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
        root / "sufficiency.json",
        {
            "status": "NOT_ASSESSED",
            "repair_status": "NOT_REQUIRED",
            "dimensions": {
                name: {
                    "status": "NOT_ASSESSED",
                    "rationale": "",
                    "supporting_refs": [],
                    "next_actions": [],
                }
                for name in SUFFICIENCY_DIMENSIONS
            },
            "overall_rationale": "",
            "unresolved_actions": [],
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
    write_json(
        root / "decision_outcome.json",
        {
            "status": None,
            "recommendation": "",
            "why": [],
            "decisive_finding_refs": [],
            "decisive_lu_refs": [],
            "critical_uncertainties": [],
            "action_now": [],
            "change_conditions": [],
            "what_evidence_supports": [],
            "what_evidence_does_not_support": [],
            "contradictions": [],
            "recommended_next_evidence": [],
            "priority_human_review": [],
        },
    )
    for filename in EMPTY_LIST_FILES:
        write_json(root / filename, [])

    print(f"Initialized {mode} Lead User study at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

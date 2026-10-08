#!/usr/bin/env python3
"""Paired, artifact-graded comparison of standard agents and Planning Skills.

Uses a caller-provided trusted command adapter. The adapter receives a public
case envelope on stdin, modifies files in its current working directory, and
exits. Hidden expectations never enter the staged workspace or stdin.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
import os
import pathlib
import random
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

from graders.outcome import grade_case, load_cases, within
from metrics import compare

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "benchmarks" / "cases.json"
ARMS = ("baseline", "skills")


def resolve_command(command: str) -> list[str]:
    parts = shlex.split(command)
    if not parts:
        raise ValueError("empty adapter command")
    result = []
    for part in parts:
        local = pathlib.Path.cwd() / part
        repo_local = ROOT / part
        if local.is_file():
            result.append(str(local.resolve()))
        elif repo_local.is_file():
            result.append(str(repo_local.resolve()))
        else:
            result.append(part)
    return result


def stage(case: dict, root: pathlib.Path, arm: str) -> None:
    for name, body in case["seed_files"].items():
        destination = within(root, name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(body, encoding="utf-8")
    if arm == "skills":
        # This arm gets the canonical packaged skills and user-facing instructions.
        # Neither arm receives evals/, checks, test code or repository history.
        shutil.copytree(ROOT / "skills", root / ".agents" / "skills")
        shutil.copy2(ROOT / "AGENTS.md", root / "AGENTS.md")


def read_review_minutes(path: pathlib.Path | None) -> dict[tuple[str, int, str], float]:
    if path is None:
        return {}
    values = {}
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"case_id", "trial", "arm", "minutes"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("review CSV needs case_id,trial,arm,minutes")
        for row in reader:
            key = (row["case_id"], int(row["trial"]), row["arm"])
            minutes = float(row["minutes"])
            if key in values or row["arm"] not in ARMS or minutes < 0 or not minutes < float("inf"):
                raise ValueError("invalid or duplicate human review measurement: " + str(key))
            values[key] = minutes
    return values


def run_case(
    case: dict, arm: str, trial: int, command: list[str],
    timeout: float, artifacts_dir: pathlib.Path | None, human_minutes: dict
) -> dict:
    with tempfile.TemporaryDirectory(prefix="planning-outcome-") as tmp:
        workspace = pathlib.Path(tmp)
        stage(case, workspace, arm)
        envelope = {
            "schema_version": 1,
            "id": case["id"],
            "arm": arm,
            "prompt": (
                "Work only in the current project directory. Complete the user's task by "
                "editing or creating actual files. Do not merely describe edits. "
                "Never assume an unstated human acceptance or selection.\n\n"
                + case["prompt"]
            ),
        }
        start = time.monotonic()
        error = None
        output = ""
        try:
            child = subprocess.run(
                command, cwd=workspace, input=json.dumps(envelope), text=True,
                capture_output=True, check=False, timeout=timeout,
                env={**os.environ, "PLANNING_OUTCOME_WORKSPACE": str(workspace)},
            )
            output = child.stdout[-8000:]
            if child.returncode != 0:
                error = f"adapter exit {child.returncode}: {child.stderr[-1000:]}"
        except (OSError, subprocess.TimeoutExpired) as exc:
            error = f"{type(exc).__name__}: {exc}"
        elapsed = round(time.monotonic() - start, 3)
        # Score changed artifacts, not the agent's answer or declared evidence.
        grade = grade_case(case, workspace)
        if error:
            grade["passed"] = False
        if artifacts_dir is not None:
            target = artifacts_dir / f"{case['id']}-trial-{trial}-{arm}"
            if target.exists():
                raise ValueError("refusing to overwrite retained run: " + str(target))
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(workspace, target, symlinks=True)
        return {
            "case_id": case["id"],
            "category": case["category"],
            "trial": trial,
            "arm": arm,
            "wall_seconds": elapsed,
            "human_review_minutes": human_minutes.get((case["id"], trial, arm)),
            "grade": grade,
            "error": error,
            "adapter_output_excerpt": output,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=pathlib.Path, default=DEFAULT_CASES)
    parser.add_argument("--validate", action="store_true", help="validate corpus only; no model run")
    parser.add_argument("--adapter-command", help="trusted adapter accepting stdin and writing workspace files")
    parser.add_argument("--runtime", default="unspecified")
    parser.add_argument("--runtime-version", default="unspecified")
    parser.add_argument("--model", default="unspecified")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--adapter-timeout-seconds", type=float, default=900)
    parser.add_argument("--artifacts-dir", type=pathlib.Path)
    parser.add_argument("--review-csv", type=pathlib.Path, help="observed external human-review minutes")
    parser.add_argument("--report", type=pathlib.Path)
    args = parser.parse_args()

    try:
        cases = load_cases(args.cases)
        if args.case_id:
            unknown = set(args.case_id) - {case["id"] for case in cases}
            if unknown:
                raise ValueError("unknown case IDs: " + str(sorted(unknown)))
            cases = [case for case in cases if case["id"] in set(args.case_id)]
        if args.validate:
            print(json.dumps({"valid": True, "cases": len(cases), "categories": sorted({c["category"] for c in cases})}))
            return 0
        if not args.adapter_command:
            parser.error("--adapter-command required unless --validate")
        if args.repeats < 1 or args.repeats > 100:
            raise ValueError("--repeats must be between 1 and 100")
        if args.adapter_timeout_seconds <= 0:
            raise ValueError("--adapter-timeout-seconds must be positive")
        command = resolve_command(args.adapter_command)
        minutes = read_review_minutes(args.review_csv)
        rng = random.Random(args.seed)
        rows = []
        for trial in range(1, args.repeats + 1):
            ordered = cases.copy()
            rng.shuffle(ordered)
            for case in ordered:
                arms = list(ARMS)
                rng.shuffle(arms)
                for arm in arms:
                    rows.append(run_case(case, arm, trial, command, args.adapter_timeout_seconds, args.artifacts_dir, minutes))
        result = {
            "schema_version": 1,
            "protocol": "paired-hidden-artifact-v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "runtime": args.runtime,
            "runtime_version": args.runtime_version,
            "model": args.model,
            "seed": args.seed,
            "repeats": args.repeats,
            "category_counts": {category: sum(c["category"] == category for c in cases) for category in sorted({c["category"] for c in cases})},
            "summary": compare(rows),
            "results": rows,
            "caveats": [
                "Results describe only the named runtime, model, adapter, cases and repeats.",
                "Passing deterministic checks does not establish real-world product value.",
                "Human effort is unknown unless externally recorded review minutes cover all runs.",
                "Wall-time differences include model and environment variance; they are not human time.",
                "The adapter is trusted host-side code; file checks are hidden from the runtime, not secure against a malicious host.",
            ],
        }
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered, encoding="utf-8")
        print(rendered)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"outcome evaluation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

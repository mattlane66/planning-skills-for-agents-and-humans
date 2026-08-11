#!/usr/bin/env python3
"""Run workflow behavior cases through a fake fixture or external runtime adapter."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "workflow-behavior-cases.json"

PUBLIC_WORKSPACE_ENTRIES = (
    ".agent-orchestration.yaml",
    ".agents",
    ".claude",
    ".claude-plugin",
    ".codex-plugin",
    ".gemini",
    "AGENTS.md",
    "GEMINI.md",
    "LICENSE",
    "docs/agent-context-feeding.md",
    "docs/agent-operating-reference.md",
    "docs/agent-run-records.md",
    "docs/execution-graph.md",
    "docs/human-decision-gates.md",
    "docs/lifecycle-hooks.md",
    "docs/loop-prompting.md",
    "docs/stable-ids.md",
    "hooks",
    "skill-inventory.txt",
    "skill-metadata.json",
    "skills",
    "templates",
)
REQUIRED_CASE_KEYS = {
    "id",
    "prompt",
    "expected_skill",
    "expected_artifact_type",
    "expected_gate",
    "implementation_allowed",
    "required_evidence",
    "forbidden_evidence",
}
REQUIRED_RESULT_KEYS = {
    "selected_skill",
    "artifact_type",
    "stopped_at_gate",
    "implementation_attempted",
    "evidence",
    "model_output",
}


@dataclass
class CaseScore:
    case_id: str
    passed: bool
    failures: list[str]
    result: dict[str, Any]


def load_cases(path: pathlib.Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("workflow behavior corpus must use schema_version 1")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("workflow behavior corpus must contain a non-empty cases list")

    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("every workflow behavior case must be an object")
        missing = REQUIRED_CASE_KEYS - set(case)
        if missing:
            raise ValueError(f"case is missing keys: {sorted(missing)}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("case id must be a non-empty string")
        if case_id in seen:
            raise ValueError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            raise ValueError(f"case prompt must be non-empty: {case_id}")
        if not isinstance(case["implementation_allowed"], bool):
            raise ValueError(f"implementation_allowed must be boolean: {case_id}")
        for key in ("required_evidence", "forbidden_evidence"):
            value = case[key]
            if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
                raise ValueError(f"{key} must be a list of non-empty strings: {case_id}")
    return cases


def fake_result(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "selected_skill": case["expected_skill"],
        "artifact_type": case["expected_artifact_type"],
        "stopped_at_gate": case["expected_gate"],
        "implementation_attempted": False,
        "evidence": list(case["required_evidence"]),
        "model_output": "[fixture adapter: no model was invoked]",
    }


def select_cases(cases: list[dict[str, Any]], case_ids: list[str]) -> list[dict[str, Any]]:
    if not case_ids:
        return cases
    requested = set(case_ids)
    known = {case["id"] for case in cases}
    unknown = requested - known
    if unknown:
        raise ValueError(f"unknown case id(s): {sorted(unknown)}")
    return [case for case in cases if case["id"] in requested]


def resolve_command(command: str, base_dir: pathlib.Path) -> list[str]:
    args = shlex.split(command)
    if not args:
        raise ValueError("adapter command must not be empty")
    resolved = []
    for arg in args:
        candidate = base_dir / arg
        if not arg.startswith("-") and candidate.exists():
            resolved.append(str(candidate.resolve()))
        else:
            resolved.append(arg)
    return resolved


def stage_public_workspace(destination: pathlib.Path) -> None:
    for relative in PUBLIC_WORKSPACE_ENTRIES:
        source = ROOT / relative
        if not source.exists():
            raise RuntimeError(f"public evaluation input is missing: {relative}")
        target = destination / relative
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def external_result(
    command: str,
    case: dict[str, Any],
    command_base_dir: pathlib.Path,
) -> dict[str, Any]:
    public_case = {
        "schema_version": 1,
        "id": case["id"],
        "prompt": case["prompt"],
    }
    command_args = resolve_command(command, command_base_dir)
    safe_case_id = "".join(char if char.isalnum() or char in "-_" else "-" for char in case["id"])

    with tempfile.TemporaryDirectory(prefix=f"planning-skill-eval-{safe_case_id}-") as tmp:
        workspace = pathlib.Path(tmp)
        stage_public_workspace(workspace)
        environment = os.environ.copy()
        environment["PWD"] = str(workspace)
        environment["PLANNING_SKILLS_EVAL_WORKSPACE"] = str(workspace)
        environment["PLANNING_SKILLS_EVAL_CASE_ID"] = case["id"]
        environment.pop("OLDPWD", None)
        completed = subprocess.run(
            command_args,
            cwd=workspace,
            env=environment,
            input=json.dumps(public_case),
            text=True,
            capture_output=True,
            check=False,
        )
    if completed.returncode != 0:
        raise RuntimeError(
            f"adapter command failed for {case['id']} with exit {completed.returncode}: "
            f"{completed.stderr.strip()}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"adapter returned invalid JSON for {case['id']}") from exc
    if not isinstance(result, dict):
        raise RuntimeError(f"adapter result must be an object for {case['id']}")
    missing = REQUIRED_RESULT_KEYS - set(result)
    if missing:
        raise RuntimeError(f"adapter result missing keys for {case['id']}: {sorted(missing)}")
    if not isinstance(result["model_output"], str) or not result["model_output"].strip():
        raise RuntimeError(f"adapter result model_output must be non-empty for {case['id']}")
    return result


def score_case(case: dict[str, Any], result: dict[str, Any]) -> CaseScore:
    failures: list[str] = []

    if result.get("selected_skill") != case["expected_skill"]:
        failures.append(
            f"selected_skill expected {case['expected_skill']!r}, got {result.get('selected_skill')!r}"
        )
    if result.get("artifact_type") != case["expected_artifact_type"]:
        failures.append(
            f"artifact_type expected {case['expected_artifact_type']!r}, got {result.get('artifact_type')!r}"
        )
    if result.get("stopped_at_gate") != case["expected_gate"]:
        failures.append(
            f"stopped_at_gate expected {case['expected_gate']!r}, got {result.get('stopped_at_gate')!r}"
        )

    attempted = bool(result.get("implementation_attempted"))
    if attempted and not case["implementation_allowed"]:
        failures.append("implementation was attempted when the case forbids it")

    evidence = result.get("evidence")
    if not isinstance(evidence, list):
        failures.append("evidence must be a list")
        evidence = []
    normalized = "\n".join(str(item).lower() for item in evidence)

    for required in case["required_evidence"]:
        if required.lower() not in normalized:
            failures.append(f"missing required evidence: {required}")
    for forbidden in case["forbidden_evidence"]:
        if forbidden.lower() in normalized:
            failures.append(f"forbidden evidence present: {forbidden}")

    return CaseScore(case["id"], not failures, failures, result)


def build_report(
    cases_path: pathlib.Path,
    adapter: str,
    runtime: str,
    runtime_version: str,
    model: str,
    commit_sha: str,
    scores: list[CaseScore],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases_file": str(cases_path),
        "adapter": adapter,
        "protocol": "fixture-v1" if adapter == "fake" else "blind-command-v1",
        "runtime": runtime,
        "runtime_version": runtime_version,
        "model": model,
        "commit_sha": commit_sha,
        "summary": {
            "passed": sum(score.passed for score in scores),
            "failed": sum(not score.passed for score in scores),
            "total": len(scores),
        },
        "cases": [
            {
                "id": score.case_id,
                "passed": score.passed,
                "failures": score.failures,
                "result": score.result,
            }
            for score in scores
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=pathlib.Path, default=DEFAULT_CASES)
    parser.add_argument(
        "--case-id",
        action="append",
        default=[],
        help="run only this case id; repeat to select multiple cases",
    )
    parser.add_argument("--adapter", choices=("fake", "command"), default="fake")
    parser.add_argument("--adapter-command")
    parser.add_argument("--runtime", default="fixture")
    parser.add_argument("--runtime-version", default="unknown")
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--commit-sha", default="unknown")
    parser.add_argument("--report", type=pathlib.Path)
    args = parser.parse_args()

    if args.adapter == "command" and not args.adapter_command:
        parser.error("--adapter-command is required when --adapter command")

    try:
        cases = select_cases(load_cases(args.cases), args.case_id)
        command_base_dir = pathlib.Path.cwd()
        scores = []
        for case in cases:
            if args.adapter == "fake":
                result = fake_result(case)
            else:
                result = external_result(args.adapter_command, case, command_base_dir)
            scores.append(score_case(case, result))
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    report = build_report(
        args.cases,
        args.adapter,
        args.runtime,
        args.runtime_version,
        args.model,
        args.commit_sha,
        scores,
    )
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate that a behavior-eval report is publishable real-runtime evidence."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any

RUNTIMES = {"claude-code", "codex", "gemini-cli"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class ReportValidationError(ValueError):
    pass


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportValidationError(f"{label} must be a non-empty string")
    return value.strip()


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReportValidationError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReportValidationError(f"invalid JSON in {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ReportValidationError(f"{path} must contain a JSON object")
    return payload


def validate_report(
    report_path: pathlib.Path,
    artifacts_dir: pathlib.Path | None = None,
    expected_runtime: str | None = None,
    expected_model: str | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    report = _load_json(report_path)

    if report.get("schema_version") != 1:
        raise ReportValidationError("report schema_version must be 1")
    if report.get("protocol") != "blind-command-v1":
        raise ReportValidationError(
            "report protocol must be blind-command-v1; fixture reports are not real-runtime evidence"
        )
    if report.get("adapter") != "command":
        raise ReportValidationError("real-runtime report adapter must be command")

    runtime = _nonempty_string(report.get("runtime"), "runtime")
    if runtime not in RUNTIMES:
        raise ReportValidationError(
            f"runtime must be one of {sorted(RUNTIMES)}, got {runtime!r}"
        )
    runtime_version = _nonempty_string(report.get("runtime_version"), "runtime_version")
    if runtime_version.lower() in {"unknown", "fixture"}:
        raise ReportValidationError("runtime_version must identify the actual runtime version")

    model = _nonempty_string(report.get("model"), "model")
    if model.lower() in {"unknown", "fixture"}:
        raise ReportValidationError("model must identify the actual model")

    commit_sha = _nonempty_string(report.get("commit_sha"), "commit_sha")
    if not SHA40.fullmatch(commit_sha):
        raise ReportValidationError("commit_sha must be a full 40-character lowercase Git SHA")

    if expected_runtime and runtime != expected_runtime:
        raise ReportValidationError(
            f"runtime mismatch: expected {expected_runtime!r}, got {runtime!r}"
        )
    if expected_model and model != expected_model:
        raise ReportValidationError(
            f"model mismatch: expected {expected_model!r}, got {model!r}"
        )
    if expected_commit and commit_sha != expected_commit:
        raise ReportValidationError(
            f"commit mismatch: expected {expected_commit!r}, got {commit_sha!r}"
        )

    summary = report.get("summary")
    if not isinstance(summary, dict):
        raise ReportValidationError("summary must be an object")
    for key in ("passed", "failed", "total"):
        if not isinstance(summary.get(key), int) or summary[key] < 0:
            raise ReportValidationError(f"summary.{key} must be a non-negative integer")

    cases = report.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ReportValidationError("report must contain at least one evaluated case")
    if summary["total"] != len(cases):
        raise ReportValidationError("summary.total must equal the number of cases")
    if summary["passed"] + summary["failed"] != summary["total"]:
        raise ReportValidationError("summary passed + failed must equal total")

    seen: set[str] = set()
    actual_passed = 0
    for case in cases:
        if not isinstance(case, dict):
            raise ReportValidationError("every case entry must be an object")
        case_id = _nonempty_string(case.get("id"), "case.id")
        if case_id in seen:
            raise ReportValidationError(f"duplicate case id: {case_id}")
        seen.add(case_id)

        passed = case.get("passed")
        if not isinstance(passed, bool):
            raise ReportValidationError(f"{case_id}: passed must be boolean")
        actual_passed += int(passed)

        failures = case.get("failures")
        if not isinstance(failures, list) or not all(isinstance(item, str) for item in failures):
            raise ReportValidationError(f"{case_id}: failures must be a list of strings")
        if passed and failures:
            raise ReportValidationError(f"{case_id}: passing case cannot contain failures")
        if not passed and not failures:
            raise ReportValidationError(f"{case_id}: failing case must explain its failures")

        result = case.get("result")
        if not isinstance(result, dict):
            raise ReportValidationError(f"{case_id}: result must be an object")
        _nonempty_string(result.get("model_output"), f"{case_id}.result.model_output")

        metadata = result.get("runtime_metadata")
        if not isinstance(metadata, dict):
            raise ReportValidationError(
                f"{case_id}: runtime_metadata is required for real-runtime evidence"
            )
        if metadata.get("provider") != runtime:
            raise ReportValidationError(
                f"{case_id}: runtime_metadata.provider must match report runtime"
            )
        if metadata.get("model") != model:
            raise ReportValidationError(
                f"{case_id}: runtime_metadata.model must match report model"
            )
        if metadata.get("evidence_source") != "answer":
            raise ReportValidationError(
                f"{case_id}: runtime_metadata.evidence_source must be answer"
            )
        observed_version = _nonempty_string(
            metadata.get("runtime_version_output"),
            f"{case_id}.runtime_metadata.runtime_version_output",
        )
        lowered = observed_version.lower()
        if lowered.startswith("unavailable:") or re.match(r"^exit \d+ with no version output$", lowered):
            raise ReportValidationError(
                f"{case_id}: runtime version output does not prove an available runtime"
            )
        if runtime_version not in observed_version:
            raise ReportValidationError(
                f"{case_id}: observed runtime version does not contain declared runtime_version {runtime_version!r}"
            )

        if artifacts_dir is not None:
            evidence_dir = artifacts_dir / case_id / ".runtime-eval"
            public_case = _load_json(evidence_dir / "public-case.json")
            evidence_meta = _load_json(evidence_dir / "metadata.json")
            if public_case.get("id") != case_id:
                raise ReportValidationError(
                    f"{case_id}: retained public-case.json has the wrong case id"
                )
            if evidence_meta.get("provider") != runtime:
                raise ReportValidationError(
                    f"{case_id}: retained metadata provider does not match report runtime"
                )
            if evidence_meta.get("model") != model:
                raise ReportValidationError(
                    f"{case_id}: retained metadata model does not match report model"
                )
            retained_version = _nonempty_string(
                evidence_meta.get("runtime_version_output"),
                f"{case_id}: retained runtime_version_output",
            )
            if retained_version != observed_version:
                raise ReportValidationError(
                    f"{case_id}: retained runtime version differs from report metadata"
                )
            for filename in ("provider-stdout.txt", "provider-stderr.txt"):
                target = evidence_dir / filename
                if not target.is_file():
                    raise ReportValidationError(f"{case_id}: missing retained {filename}")

    actual_failed = len(cases) - actual_passed
    if summary["passed"] != actual_passed or summary["failed"] != actual_failed:
        raise ReportValidationError("summary counts do not match case pass/fail states")

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=pathlib.Path)
    parser.add_argument("--artifacts-dir", type=pathlib.Path)
    parser.add_argument("--expected-runtime", choices=sorted(RUNTIMES))
    parser.add_argument("--expected-model")
    parser.add_argument("--expected-commit")
    args = parser.parse_args(argv)

    try:
        report = validate_report(
            args.report,
            artifacts_dir=args.artifacts_dir,
            expected_runtime=args.expected_runtime,
            expected_model=args.expected_model,
            expected_commit=args.expected_commit,
        )
    except (OSError, ReportValidationError) as exc:
        print(f"Behavior report validation failed: {exc}", file=sys.stderr)
        return 2

    summary = report["summary"]
    print(
        "Publishable real-runtime behavior report: "
        f"{report['runtime']} {report['runtime_version']} / {report['model']} / "
        f"{summary['passed']}/{summary['total']} cases passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

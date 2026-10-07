#!/usr/bin/env python3
"""Classify code changes against a compiled ProductIntentModel."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path


def changed_paths(base_ref: str | None, head_ref: str | None) -> list[str]:
    if not base_ref:
        return []
    head_ref = head_ref or "HEAD"
    proc = subprocess.run(
        ["git", "diff", "--name-only", base_ref, head_ref],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def matches(path: str, pattern: str) -> bool:
    return path == pattern or fnmatch.fnmatch(path, pattern)


def load_verification(path: Path | None) -> dict[str, str]:
    if not path:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    output = {}
    for check in payload.get("checks", []):
        ref = str(check.get("intent_ref", "")).strip()
        status = str(check.get("status", "")).strip().lower()
        if ref and status:
            output[ref] = status
    return output


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intent", type=Path, required=True)
    parser.add_argument("--base-ref")
    parser.add_argument("--head-ref")
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--verification-report", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    model = json.loads(args.intent.read_text(encoding="utf-8"))
    paths = list(dict.fromkeys(args.changed_path + changed_paths(args.base_ref, args.head_ref)))
    verification = load_verification(args.verification_report)

    impacted_bindings = []
    impacted_refs = set()
    for binding in model.get("implementation_bindings", []):
        if any(matches(path, pattern) for path in paths for pattern in binding.get("paths", [])):
            impacted_bindings.append(binding["id"])
            impacted_refs.update(binding.get("intent_refs", []))

    impacted_invariants = [
        inv["id"]
        for inv in model.get("invariants", [])
        if impacted_refs.intersection(inv.get("protects", []))
    ]
    failed = sorted(
        ref for ref in impacted_invariants
        if verification.get(ref) in {"fail", "failed", "violation"}
    )

    ignored_prefixes = (
        "planning/",
        "docs/",
        "examples/",
        ".github/",
        "site/",
    )
    code_like = [
        path for path in paths
        if not path.startswith(ignored_prefixes)
        and Path(path).suffix.lower() in {
            ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".rb", ".java",
            ".kt", ".swift", ".cs", ".php", ".vue", ".svelte", ".html", ".css"
        }
    ]
    bound_paths = {
        path for path in code_like
        if any(matches(path, pattern) for binding in model.get("implementation_bindings", []) for pattern in binding.get("paths", []))
    }
    unmapped = sorted(set(code_like) - bound_paths)

    if failed:
        status = "VIOLATION"
        exit_code = 2
    elif impacted_refs or unmapped:
        status = "REVIEW_REQUIRED"
        exit_code = 1
    else:
        status = "PASS"
        exit_code = 0

    result = {
        "status": status,
        "changed_paths": paths,
        "impacted_bindings": sorted(impacted_bindings),
        "impacted_intent_refs": sorted(impacted_refs),
        "impacted_invariants": sorted(impacted_invariants),
        "failed_invariants": failed,
        "unmapped_code_changes": unmapped,
        "interpretation": {
            "PASS": "No bound product intent was touched by the supplied diff.",
            "REVIEW_REQUIRED": "The diff may affect accepted intent or changes product code with no binding. Review before merge.",
            "VIOLATION": "A supplied verification result reports an affected invariant as failed."
        }[status],
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(status)
        print(result["interpretation"])
        if impacted_refs:
            print("Impacted intent: " + ", ".join(sorted(impacted_refs)))
        if impacted_invariants:
            print("Invariants to verify: " + ", ".join(sorted(impacted_invariants)))
        if unmapped:
            print("Unmapped code changes: " + ", ".join(unmapped))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

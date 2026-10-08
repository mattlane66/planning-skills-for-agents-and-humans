#!/usr/bin/env python3
"""Trusted Codex CLI command adapter for outcome benchmark trials.

Accepts a public benchmark envelope on stdin. Writes through Codex into the
current staged project. No hidden checks or scorer outputs are passed to Codex.
Run only in an isolated, disposable environment with no unrelated credentials.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=800)
    args = parser.parse_args()
    case = json.load(sys.stdin)
    if not isinstance(case, dict) or set(case) != {"schema_version", "id", "arm", "prompt"}:
        print("invalid public outcome case", file=sys.stderr)
        return 2
    if case["schema_version"] != 1 or case["arm"] not in {"baseline", "skills"}:
        print("invalid outcome protocol", file=sys.stderr)
        return 2
    if not isinstance(case["prompt"], str) or not case["prompt"].strip():
        print("invalid prompt", file=sys.stderr)
        return 2

    prompt = case["prompt"] + (
        "\n\nIf a planning skill is available and warranted, use the smallest "
        "relevant one. Preserve human authority and accepted decisions. "
        "Only change files inside the current project workspace."
    )
    command = [
        "codex", "exec", "--ephemeral", "--ignore-user-config",
        "--sandbox", "workspace-write", "--skip-git-repo-check",
        "--model", args.model, prompt,
    ]
    try:
        child = subprocess.run(
            command, text=True, capture_output=True, check=False,
            timeout=args.timeout_seconds, env=os.environ.copy(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"Codex invocation failed: {exc}", file=sys.stderr)
        return 2
    # These are audit-only. The outcome grader reads actual files.
    print(child.stdout[-8000:])
    if child.returncode:
        print(child.stderr[-2500:], file=sys.stderr)
    return child.returncode


if __name__ == "__main__":
    raise SystemExit(main())

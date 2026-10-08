"""Host-owned artifact graders for the outcome comparison benchmark.

The runtime never sees hidden checks. These graders inspect the files it actually
wrote rather than its self-reported success. Python calls execute untrusted model
code: only run on disposable isolated hosts without secrets or network access.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
from typing import Any

KINDS = {"text_equals", "text_contains", "text_absent", "path_absent",
         "json_equals", "json_array_contains", "python_call", "python_raises"}
CATEGORIES = {"contained", "decision", "handoff"}
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,80}$")

WORKER = r'''
import importlib.util, json, pathlib, sys
request = json.loads(sys.argv[1])
path = pathlib.Path(request["path"])
try:
    spec = importlib.util.spec_from_file_location("outcome_test_module", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = getattr(module, request["function"])(*request["args"])
    print(json.dumps({"status": "returned", "value": result}, allow_nan=False))
except BaseException as exc:
    print(json.dumps({"status": "raised", "exception": type(exc).__name__}))
'''


def safe_relative(path: str) -> pathlib.PurePosixPath:
    if not isinstance(path, str) or not path or "\\" in path:
        raise ValueError("file path must be a nonempty POSIX relative path")
    relative = pathlib.PurePosixPath(path)
    if relative.is_absolute() or any(part in (".", "..") for part in path.split("/")):
        raise ValueError(f"unsafe fixture path: {path}")
    if relative.parts[0].startswith("."):
        raise ValueError(f"hidden fixture path forbidden: {path}")
    return relative


def within(root: pathlib.Path, relative: str) -> pathlib.Path:
    """Reject symlink-based escapes even if the agent replaced a parent directory."""
    path = root.joinpath(*safe_relative(relative).parts)
    base = root.resolve()
    if not path.resolve().is_relative_to(base):
        raise ValueError(f"path escaped benchmark workspace: {relative}")
    return path


def validate_cases(cases: list[dict[str, Any]]) -> None:
    if not isinstance(cases, list) or len(cases) < 1:
        raise ValueError("benchmark cases must be a non-empty list")
    seen = set()
    for case in cases:
        if not isinstance(case, dict) or not SAFE_ID.fullmatch(str(case.get("id", ""))):
            raise ValueError("invalid benchmark case ID")
        if case["id"] in seen:
            raise ValueError("duplicate case ID: " + case["id"])
        seen.add(case["id"])
        if case.get("category") not in CATEGORIES:
            raise ValueError("invalid benchmark category: " + case["id"])
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError("missing prompt: " + case["id"])
        files = case.get("seed_files")
        checks = case.get("checks")
        if not isinstance(files, dict) or not files or not isinstance(checks, list) or not checks:
            raise ValueError("missing seed files or checks: " + case["id"])
        for path, data in files.items():
            safe_relative(path)
            if not isinstance(data, str):
                raise ValueError("fixture file contents must be text")
        for check in checks:
            if not isinstance(check, dict) or check.get("kind") not in KINDS:
                raise ValueError("invalid grader kind: " + case["id"])
            safe_relative(check.get("path"))
            if check["kind"] in {"text_equals", "text_contains", "text_absent", "json_equals", "json_array_contains"} and "value" not in check:
                raise ValueError("grader missing value: " + case["id"])
            if check["kind"].startswith("json_") and not isinstance(check.get("field"), str):
                raise ValueError("JSON grader missing field: " + case["id"])
            if check["kind"].startswith("python_"):
                if not check["path"].endswith(".py") or not isinstance(check.get("function"), str) or not check["function"].isidentifier():
                    raise ValueError("invalid Python grader target: " + case["id"])
                if not isinstance(check.get("args"), list):
                    raise ValueError("Python grader args must be an array")
                if check["kind"] == "python_call" and "expected" not in check:
                    raise ValueError("Python call requires expected value")
                if check["kind"] == "python_raises" and check.get("exception") not in {"ValueError", "TypeError", "KeyError", "PermissionError"}:
                    raise ValueError("unsupported exception name")
            if "critical" in check and not isinstance(check["critical"], bool):
                raise ValueError("critical must be boolean")
            if "invariant" in check and not isinstance(check["invariant"], bool):
                raise ValueError("invariant must be boolean")


def load_cases(path: pathlib.Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("expected benchmark schema_version=1")
    cases = data.get("cases")
    validate_cases(cases)
    return cases


def field_value(value: Any, field: str) -> Any:
    for key in field.split("."):
        if not isinstance(value, dict) or key not in value:
            raise KeyError(field)
        value = value[key]
    return value


def typed_equal(a: Any, b: Any) -> bool:
    # Python equates True with 1; JSON outcomes must not.
    return type(a) is type(b) and a == b


def call_python(path: pathlib.Path, check: dict[str, Any], timeout: float = 5.0) -> dict[str, Any]:
    request = json.dumps({"path": str(path), "function": check["function"], "args": check["args"]})
    # -I suppresses user site/config but is NOT an OS sandbox.
    completed = subprocess.run(
        [sys.executable, "-I", "-B", "-c", WORKER, request],
        cwd=path.parent, capture_output=True, text=True, check=False, timeout=timeout,
        env={"PATH": os.defpath, "PYTHONNOUSERSITE": "1"},
    )
    if completed.returncode != 0:
        raise RuntimeError("test worker exited " + str(completed.returncode))
    try:
        result = json.loads(completed.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError) as exc:
        raise RuntimeError("worker did not return JSON") from exc
    if not isinstance(result, dict):
        raise RuntimeError("invalid worker result")
    return result


def grade_check(check: dict[str, Any], root: pathlib.Path) -> tuple[bool, str]:
    kind = check["kind"]
    path = within(root, check["path"])
    if kind == "path_absent":
        passed = not path.exists() and not path.is_symlink()
        return passed, "unexpected path present" if not passed else ""
    if not path.is_file() or path.is_symlink():
        return False, "expected regular file missing"
    if kind.startswith("python_"):
        response = call_python(path, check)
        if kind == "python_call":
            passed = response.get("status") == "returned" and typed_equal(response.get("value"), check["expected"])
        else:
            passed = response.get("status") == "raised" and response.get("exception") == check["exception"]
        return passed, "" if passed else "call failed expected behavior"
    data = path.read_text(encoding="utf-8")
    if kind == "text_equals":
        passed = data == check["value"]
    elif kind == "text_contains":
        passed = check["value"] in data
    elif kind == "text_absent":
        passed = check["value"] not in data
    else:
        parsed = json.loads(data)
        actual = field_value(parsed, check["field"])
        if kind == "json_equals":
            passed = typed_equal(actual, check["value"])
        elif kind == "json_array_contains":
            passed = isinstance(actual, list) and any(typed_equal(item, check["value"]) for item in actual)
        else:
            raise ValueError("unknown grader kind")
    return passed, "" if passed else "artifact differs from expected outcome"


def grade_case(case: dict[str, Any], root: pathlib.Path) -> dict[str, Any]:
    results = []
    for index, check in enumerate(case["checks"]):
        try:
            passed, reason = grade_check(check, root)
        except (ValueError, KeyError, OSError, UnicodeError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            passed, reason = False, f"{type(exc).__name__}: {exc}"
        results.append({
            "index": index, "kind": check["kind"], "path": check["path"],
            "passed": passed, "critical": bool(check.get("critical")),
            "invariant": bool(check.get("invariant")), "reason": reason,
        })
    return {
        "passed": all(item["passed"] for item in results),
        "critical_violation": any(not item["passed"] and item["critical"] for item in results),
        "checks": results,
        "passed_checks": sum(item["passed"] for item in results),
        "total_checks": len(results),
        "passed_invariants": sum(item["passed"] for item in results if item["invariant"]),
        "total_invariants": sum(item["invariant"] for item in results),
    }

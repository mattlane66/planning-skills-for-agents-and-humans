#!/usr/bin/env python3
"""Run independent, previously accepted black-box product examples.

Only use with trusted scenarios and code in an isolated CI runner. This process
executes application Python and is NOT a sandbox. Does not execute shell commands
from metadata. Do not use an agent-written pass report as verification evidence.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

WORKER = r'''
import importlib.util, json, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
module = (root / sys.argv[2]).resolve()
if root not in module.parents or module.suffix != ".py":
    raise ValueError("unsafe module path")
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("intent_target", module)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
func = getattr(mod, sys.argv[3])
case = json.loads(sys.stdin.read())
result = func(*case.get("args", []), **case.get("kwargs", {}))
print("__PRODUCT_INTENT_RESULT__" + json.dumps(result, sort_keys=True))
'''

def _relative_file(root, rel):
    if not isinstance(rel, str) or not rel or rel.startswith("/"):
        raise ValueError("invalid module path")
    path = (root / rel).resolve()
    if root not in path.parents or path.suffix != ".py":
        raise ValueError("module escapes code root or is not Python")
    if not path.is_file():
        raise ValueError(f"module not found: {rel}")
    return path

def validate_manifest(manifest):
    errors = []
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return ["manifest must have schema_version 1"]
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return ["manifest must declare scenarios"]
    seen = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            errors.append("scenario must be an object"); continue
        sid = scenario.get("id")
        if not isinstance(sid, str) or not sid or sid in seen:
            errors.append("duplicate or missing scenario ID")
        seen.add(sid)
        if scenario.get("adapter") != "python_function":
            errors.append(f"{sid}: only python_function is currently supported")
        if not isinstance(scenario.get("module"), str) or not scenario["module"]:
            errors.append(f"{sid}: missing module")
        if not isinstance(scenario.get("function"), str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", scenario["function"]):
            errors.append(f"{sid}: invalid function")
        if not isinstance(scenario.get("intent_ids"), list) or not scenario["intent_ids"] or not all(isinstance(v, str) for v in scenario["intent_ids"]):
            errors.append(f"{sid}: missing intent IDs")
        cases = scenario.get("cases")
        if not isinstance(cases, list) or not cases:
            errors.append(f"{sid}: cases required"); continue
        for i, case in enumerate(cases):
            if not isinstance(case, dict) or "expected" not in case or not isinstance(case.get("args", []), list) or not isinstance(case.get("kwargs", {}), dict):
                errors.append(f"{sid}: invalid expected/args/kwargs in case {i}")
    return errors

def verify(manifest, code_root, affected_intent_ids=None, timeout=5):
    root = pathlib.Path(code_root).resolve()
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    all_intents = set(affected_intent_ids or [])
    scenarios = [s for s in manifest["scenarios"]
                 if not affected_intent_ids or set(s["intent_ids"]) & all_intents]
    covered = {intent for s in scenarios for intent in s["intent_ids"]}
    uncovered = sorted(all_intents - covered)
    results = []
    for scenario in scenarios:
        _relative_file(root, scenario["module"])
        for index, case in enumerate(scenario["cases"]):
            try:
                process = subprocess.run(
                    [sys.executable, "-I", "-c", WORKER, str(root), scenario["module"], scenario["function"]],
                    input=json.dumps({"args": case.get("args", []), "kwargs": case.get("kwargs", {})}),
                    text=True, capture_output=True, timeout=timeout, cwd=root, check=False
                )
                lines = [line.removeprefix("__PRODUCT_INTENT_RESULT__")
                         for line in process.stdout.splitlines()
                         if line.startswith("__PRODUCT_INTENT_RESULT__")]
                if process.returncode or len(lines) != 1:
                    result = {"status": "ERROR", "detail": (process.stderr or "invalid result")[-600:]}
                else:
                    actual = json.loads(lines[0])
                    result = {"status": "PASS" if actual == case["expected"] else "DRIFT",
                              "expected": case["expected"], "actual": actual}
            except (subprocess.TimeoutExpired, ValueError, OSError) as exc:
                result = {"status": "ERROR", "detail": str(exc)}
            result.update({"scenario": scenario["id"], "case": case.get("id", str(index)),
                           "intent_ids": scenario["intent_ids"]})
            results.append(result)
    verdict = ("DRIFT" if any(x["status"] == "DRIFT" for x in results) else
               "REVIEW" if uncovered or not results or any(x["status"] == "ERROR" for x in results) else
               "PASS")
    return {"verdict": verdict, "results": results, "uncovered_intent_ids": uncovered,
            "limits": "Only declared examples were executed. Passing does not prove global semantic equivalence."}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trusted-manifest", required=True, help="Approved manifest from trusted base branch, not the PR")
    ap.add_argument("--code-root", required=True)
    ap.add_argument("--intent-id", action="append", dest="intent_ids")
    ap.add_argument("--timeout", type=float, default=5)
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        manifest = json.loads(pathlib.Path(args.trusted_manifest).read_text(encoding="utf-8"))
        result = verify(manifest, args.code_root, args.intent_ids, args.timeout)
        output = json.dumps(result, indent=2)
        if args.out:
            pathlib.Path(args.out).write_text(output + "\n", encoding="utf-8")
        print(output)
        return 0 if result["verdict"] == "PASS" else 1
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Product intent verifier error: {exc}", file=sys.stderr)
        return 2
if __name__ == "__main__":
    sys.exit(main())

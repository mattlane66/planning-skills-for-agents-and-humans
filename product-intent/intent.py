#!/usr/bin/env python3
"""Product-intent overlay CLI. Standard-library only. Deliberately never auto-approves intent."""
import argparse
import fnmatch
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

KINDS = {"capability", "requirement", "place", "affordance", "state", "transition",
         "rule", "interface", "invariant", "decision", "non_goal"}
STATUSES = {"inferred", "working", "accepted", "rejected", "superseded"}
REQUIRED = {"id", "kind", "title", "status", "statement", "refs", "evidence"}
RECORD_FIELDS = REQUIRED | {"owner", "approved_by", "approved_at", "alternatives",
                            "reopen_when", "supersedes", "verification", "scope"}
BINDING_FIELDS = {"intent_id", "paths", "symbols", "tests", "confidence", "evidence"}

def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

def dump(path, value):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def validate(model):
    errors = []
    if not isinstance(model, dict):
        return ["root must be an object"]
    if model.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(model.get("product"), str) or not model.get("product"):
        errors.append("product must be a nonempty string")
    if set(model) - {"schema_version", "product", "planning_package", "records", "bindings"}:
        errors.append("unknown top-level keys")
    records = model.get("records")
    bindings = model.get("bindings", [])
    if not isinstance(records, list):
        return errors + ["records must be an array"]
    if not isinstance(bindings, list):
        return errors + ["bindings must be an array"]
    ids = set()
    for i, r in enumerate(records):
        loc = f"records[{i}]"
        if not isinstance(r, dict):
            errors.append(f"{loc}: must be an object")
            continue
        for field in REQUIRED - set(r):
            errors.append(f"{loc}: missing {field}")
        if set(r) - RECORD_FIELDS:
            errors.append(f"{loc}: unknown fields {sorted(set(r)-RECORD_FIELDS)}")
        ident = r.get("id")
        if not isinstance(ident, str) or re.fullmatch(r"[A-Z][A-Z0-9]*-[0-9]+", ident) is None:
            errors.append(f"{loc}: invalid ID")
        elif ident in ids:
            errors.append(f"{loc}: duplicate ID {ident}")
        else:
            ids.add(ident)
        if r.get("kind") not in KINDS:
            errors.append(f"{loc}: invalid kind")
        if r.get("status") not in STATUSES:
            errors.append(f"{loc}: invalid status")
        for f in ("title", "statement"):
            if not isinstance(r.get(f), str) or not r[f].strip():
                errors.append(f"{loc}: {f} must be nonempty")
        for f in ("refs", "evidence", "supersedes", "verification", "scope"):
            if f in r and (not isinstance(r[f], list) or not all(isinstance(s, str) for s in r[f])):
                errors.append(f"{loc}: {f} must be an array of strings")
        if r.get("status") == "accepted" and (not r.get("approved_by") or not r.get("approved_at")):
            errors.append(f"{loc}: accepted intent requires approved_by and approved_at")
        if r.get("kind") == "decision" and r.get("status") == "accepted" and not r.get("alternatives"):
            errors.append(f"{loc}: accepted decision must preserve alternatives")
        if "alternatives" in r:
            if not isinstance(r["alternatives"], list):
                errors.append(f"{loc}: alternatives must be an array")
            else:
                for j, alt in enumerate(r["alternatives"]):
                    if not isinstance(alt, dict) or set(alt) != {"name", "disposition", "reason"} or alt.get("disposition") not in {"chosen", "rejected", "deferred"} or not all(isinstance(alt.get(k), str) and alt[k].strip() for k in ("name", "reason")):
                        errors.append(f"{loc}: invalid alternative {j}")
    for i, r in enumerate(records):
        if isinstance(r, dict):
            for field in ("supersedes",):
                for ref in r.get(field, []) if isinstance(r.get(field, []), list) else []:
                    if ref not in ids:
                        errors.append(f"records[{i}]: unknown {field} ID {ref}")
            if r.get("id") in r.get("supersedes", []):
                errors.append(f"records[{i}]: cannot supersede itself")
    for i, b in enumerate(bindings):
        loc = f"bindings[{i}]"
        if not isinstance(b, dict):
            errors.append(f"{loc}: must be an object")
            continue
        if set(b) - BINDING_FIELDS:
            errors.append(f"{loc}: unknown fields")
        target = b.get("intent_id")
        typed_planning_id = isinstance(target, str) and bool(re.fullmatch(
            r"(?:requirement|shape|place|affordance|non_ui_affordance|store|state|transition|interface):[A-Za-z][A-Za-z0-9.]*", target))
        if target not in ids and not typed_planning_id:
            errors.append(f"{loc}: unknown intent ID")
        if b.get("confidence") not in ("inferred", "confirmed"):
            errors.append(f"{loc}: invalid confidence")
        for f in ("paths", "symbols", "tests", "evidence"):
            if f == "paths" or f in b:
                if not isinstance(b.get(f), list) or (f == "paths" and not b[f]) or not all(isinstance(v, str) and v for v in b[f]):
                    errors.append(f"{loc}: invalid {f}")
        for pattern in b.get("paths", []) if isinstance(b.get("paths", []), list) else []:
            if pattern.startswith("/") or ".." in pathlib.PurePosixPath(pattern).parts:
                errors.append(f"{loc}: unsafe path glob {pattern}")
    return errors

def impacted(model, changed):
    matches = {}
    for b in model.get("bindings", []):
        hit = [p for p in changed if any(fnmatch.fnmatchcase(p, glob) for glob in b["paths"])]
        if hit:
            matches.setdefault(b["intent_id"], set()).update(hit)
    return {k: sorted(v) for k, v in matches.items()}

def compare(before, after):
    a = {r["id"]: r for r in before["records"]}
    b = {r["id"]: r for r in after["records"]}
    critical = []
    for ident in sorted(set(a) | set(b)):
        old, new = a.get(ident), b.get(ident)
        if old and old["status"] == "accepted" and (new is None or
            any(old.get(key) != new.get(key) for key in ("kind", "statement", "status", "refs", "verification"))):
            critical.append(ident)
    return critical

def review(model, changed, previous=None, evidence=None):
    mapping = impacted(model, changed)
    records = {r["id"]: r for r in model["records"]}
    findings = []
    for ident, paths in mapping.items():
        # Canonical PlanningPackage IDs have typed targets, not extension records.
        r = records.get(ident, {"kind": "canonical_planning_record", "status": "accepted"})
        checks = [b for b in model.get("bindings", []) if b["intent_id"] == ident]
        validated = bool(evidence and ident in evidence and evidence[ident].get("result") == "pass"
                         and evidence[ident].get("tests") and
                         all(t in evidence[ident]["tests"] for b in checks for t in b.get("tests", [])))
        findings.append({"id": ident, "changed_paths": paths,
                         "status": "verified" if validated else "review",
                         "reason": "supplied evidence covers bound tests" if validated else
                         "change touches declared realization; intent conformance not proven"})
    uncovered = sorted(set(changed) - {p for paths in mapping.values() for p in paths})
    changes_to_accepted = compare(previous, model) if previous else []
    if changes_to_accepted:
        verdict = "DRIFT"
    elif any(f["status"] == "review" for f in findings) or uncovered:
        verdict = "REVIEW"
    else:
        verdict = "PASS"
    return {"verdict": verdict, "findings": findings,
            "unmapped_changed_paths": uncovered,
            "accepted_intent_changes": changes_to_accepted,
            "limitation": "PASS means declared bindings and submitted checks passed; it is not proof of complete behavioral equivalence."}

def project(model, directory):
    dest = pathlib.Path(directory)
    dest.mkdir(parents=True, exist_ok=True)
    selected = [r for r in model["records"] if r["status"] == "accepted"]
    def section(items, heading):
        return "## " + heading + "\n\n" + ("\n".join(
            f"- **{r['id']} — {r['title']}**: {r['statement']}" for r in items) or "_None recorded._") + "\n\n"
    qa = "# QA scenarios (derived; not automatically executable)\n\n"
    qa += section([r for r in selected if r["kind"] in {"invariant", "rule", "transition"}], "Must remain true")
    for r in selected:
        if r.get("verification"):
            qa += f"### {r['id']}\n" + "\n".join(f"- [ ] {v}" for v in r["verification"]) + "\n\n"
    docs = "# Product behavior (derived; verify before external use)\n\n"
    docs += section([r for r in selected if r["kind"] in {"capability", "affordance", "rule"}], "Capabilities and rules")
    docs += section([r for r in selected if r["kind"] == "non_goal"], "Known boundaries")
    decisions = "# Decision history (derived)\n\n"
    for r in selected:
        if r["kind"] == "decision":
            decisions += f"## {r['id']} — {r['title']}\n\n{r['statement']}\n\n"
            for alt in r.get("alternatives", []):
                decisions += f"- {alt['name']} ({alt['disposition']}): {alt['reason']}\n"
            decisions += f"\nReopen when: {r.get('reopen_when') or 'not recorded'}\n\n"
    dump(dest / "agent-context.json", {"product": model["product"],
                                         "accepted_records": selected,
                                         "bindings": model.get("bindings", [])})
    (dest / "qa.md").write_text(qa, encoding="utf-8")
    (dest / "product.md").write_text(docs, encoding="utf-8")
    (dest / "decisions.md").write_text(decisions, encoding="utf-8")

def bootstrap(source):
    root = pathlib.Path(source)
    if not root.is_dir():
        raise ValueError("source must be an existing directory")
    # Inventory only. Observed files cannot establish product intent.
    candidates = []
    for p in sorted(root.rglob("*")):
        if len(candidates) >= 200:
            break
        if p.is_file() and ".git" not in p.parts and any(fnmatch.fnmatch(p.name, pattern)
            for pattern in ("*test*.py", "*spec*.ts", "*test*.js", "*spec*.js", "*test*.tsx", "*spec*.tsx")):
            candidates.append(p.relative_to(root).as_posix())
    return {"schema_version": 1, "product": root.name,
            "records": [], "bindings": [],
            "bootstrap_candidates": candidates,
            "note": "Review these test files, observe behavior, and obtain human approval before adding accepted records."}

def main():
    ap = argparse.ArgumentParser(description="Product intent overlay: validate, review diffs, produce projections")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("file"); p.add_argument("--product", required=True)
    p = sub.add_parser("validate"); p.add_argument("file")
    p = sub.add_parser("check"); p.add_argument("file"); p.add_argument("--before")
    p.add_argument("--changed", nargs="+", required=True)
    p.add_argument("--evidence"); p.add_argument("--strict", action="store_true")
    p = sub.add_parser("project"); p.add_argument("file"); p.add_argument("--out", required=True)
    p = sub.add_parser("bootstrap"); p.add_argument("--source", required=True); p.add_argument("--out", required=True)
    args = ap.parse_args()
    if args.command == "bootstrap":
        dump(args.out, bootstrap(args.source)); print("Candidate inventory written; no intent was inferred or accepted."); return 0
    if args.command == "init":
        dump(args.file, {"schema_version": 1, "product": args.product, "records": [], "bindings": []})
        return 0
    model = load(args.file)
    problems = validate(model)
    if problems:
        for problem in problems: print("ERROR:", problem, file=sys.stderr)
        return 2
    if args.command == "validate":
        print("VALID"); return 0
    if args.command == "project":
        project(model, args.out); print("Derived projections written."); return 0
    before = load(args.before) if args.before else None
    if before and validate(before):
        print("ERROR: invalid previous model", file=sys.stderr); return 2
    evidence = load(args.evidence) if args.evidence else None
    report = review(model, args.changed, before, evidence)
    print(json.dumps(report, indent=2))
    return 1 if args.strict and report["verdict"] != "PASS" else 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

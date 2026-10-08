#!/usr/bin/env python3
"""Conservative code-to-intent candidate discovery, never an approval system.

Python symbols use AST locations. JavaScript/TypeScript symbols are token-level
candidates only, not a claimed complete parser or call graph.
"""
import argparse
import ast
import json
import os
import pathlib
import re

IGNORED_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv",
                "__pycache__", ".next", "coverage", "vendor"}
SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx"}
STOP = {"user", "users", "must", "should", "from", "with", "that", "this",
        "will", "into", "does", "have", "doesnt", "when", "what", "where",
        "which", "before", "after", "their", "saved", "save", "code",
        "product", "behavior", "state", "system", "change"}
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9]*")
JS_SYMBOL = re.compile(
    r"\b(?:export\s+)?(?:async\s+)?(?:function|class|interface|type|const|let)\s+([A-Za-z_$][\w$]*)"
)

def words(value):
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(value))
    return {w.lower() for w in IDENTIFIER.findall(value)
            if len(w) >= 4 and w.lower() not in STOP}

def symbols(path, source):
    if path.suffix == ".py":
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []
        return [
            {"name": node.name, "line": node.lineno}
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]
    return [
        {"name": match.group(1), "line": source.count("\n", 0, match.start()) + 1}
        for match in JS_SYMBOL.finditer(source)
    ]

def eligible_files(root, max_files=1000, max_bytes=300_000):
    count = 0
    for directory, subdirs, filenames in os.walk(root, followlinks=False):
        subdirs[:] = sorted(d for d in subdirs if d not in IGNORED_DIRS and
                            not (pathlib.Path(directory) / d).is_symlink())
        for name in sorted(filenames):
            path = pathlib.Path(directory) / name
            if path.is_symlink() or path.suffix not in SOURCE_SUFFIXES:
                continue
            if count >= max_files:
                return
            try:
                if path.stat().st_size > max_bytes:
                    continue
                source = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            count += 1
            yield path.relative_to(root).as_posix(), path, source

def _nodes(package, include_working=False):
    model = package.get("product_intent")
    if not isinstance(model, dict):
        raise ValueError("compile PlanningPackage with planning/product-intent.json first")
    results = []
    allowed = {"accepted", "working"} if include_working else {"accepted"}
    for record in model.get("extension_records", []):
        if record["status"] in allowed:
            results.append({"id": record["id"], "uid": record["uid"],
                            "authority": record["status"],
                            "text": record["title"] + " " + record["statement"]})
    for record in model.get("planning_records", []):
        if record["status"] in allowed:
            raw = record.get("data", {})
            results.append({"id": record["id"], "uid": record["uid"],
                            "authority": record["status"],
                            "text": " ".join(str(x) for x in raw.values() if isinstance(x, str))})
    return results

def propose(package, code_root, max_files=1000, include_working=False):
    root = pathlib.Path(code_root).resolve()
    if not root.is_dir():
        raise ValueError("code-root is not a directory")
    targets = _nodes(package, include_working=include_working)
    proposals = []
    for relpath, path, source in eligible_files(root, max_files=max_files):
        location_words = words(relpath)
        for symbol in symbols(path, source):
            symbol_words = words(symbol["name"])
            for target in targets:
                target_words = words(target["text"])
                hits = sorted((symbol_words | location_words) & target_words)
                # A meaningful exact symbol-name match or two lexical anchors,
                # never a semantic or implementation-equivalence claim.
                strong = bool(symbol_words and symbol_words <= target_words)
                if len(hits) < 2 and not (strong and len(symbol_words) >= 1):
                    continue
                proposals.append({
                    "intent_uid": target["uid"],
                    "intent_id": target["id"],
                    "intent_authority": target["authority"],
                    "candidate_path": relpath,
                    "candidate_symbol": symbol["name"],
                    "line": symbol["line"],
                    "evidence": {"kind": "lexical_symbol_overlap",
                                 "shared_tokens": hits,
                                 "parser": "python_ast" if path.suffix == ".py" else "js_ts_declaration_regex"},
                    "confidence": "inferred",
                    "requires_review": True,
                })
    proposals.sort(key=lambda r: (r["intent_uid"], r["candidate_path"], r["line"]))
    covered = {r["intent_uid"] for r in proposals}
    return {
        "kind": "IntentBindingProposals", "schema_version": 1,
        "proposals": proposals,
        "include_working": include_working,
        "unmapped_intent_uids": sorted(t["uid"] for t in targets if t["uid"] not in covered),
        "disclaimer": "Lexical proposals do not establish execution paths, correct behavior, or human approval.",
    }

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package", required=True, help="PlanningPackage JSON with product_intent")
    ap.add_argument("--code-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--include-working", action="store_true",
                    help="Suggest code links for provisional Working intent, always requiring review")
    args = ap.parse_args()
    result = propose(json.loads(pathlib.Path(args.package).read_text(encoding="utf-8")), args.code_root, include_working=args.include_working)
    pathlib.Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{len(result['proposals'])} candidate bindings; {len(result['unmapped_intent_uids'])} unlinked records")
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compare changed code with accepted behavior via protected baseline scenarios."""
import argparse
import fnmatch
import importlib.util
import json
from pathlib import Path
import sys

def accepted(pkg):
    model=pkg.get("product_intent") or {}
    records=model.get("planning_records",[])+model.get("extension_records",[])
    return {r["uid"]:{"kind":r["kind"],"status":r["status"],
                      "facts":r.get("data",r.get("statement")),
                      "refs":r.get("resolved_refs",[])}
            for r in records if r.get("status")=="accepted"}

def run_scenarios(manifest, root, affected):
    path=Path(__file__).with_name("behaviors.py")
    spec=importlib.util.spec_from_file_location("trusted_intent_behaviors",path)
    tool=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool.verify(manifest,root,sorted(affected))

def gate(candidate, changed, root, manifest, base=None):
    model=candidate.get("product_intent")
    if not isinstance(model,dict):
        return {"verdict":"REVIEW","reason":"No compiled product intent model"}
    impacted={}
    unmapped=[]
    for path in sorted(set(changed)):
        matches=[b for b in model.get("bindings",[])
                 if any(fnmatch.fnmatchcase(path,pattern) for pattern in b.get("paths",[]))]
        if not matches: unmapped.append(path)
        for binding in matches:
            ident=binding["intent_id"]
            item=impacted.setdefault(ident,{"paths":[],"confirmed":True})
            item["paths"].append(path)
            item["confirmed"] &= binding.get("confidence")=="confirmed"
    no_baseline=base is None or not isinstance(base.get("product_intent"),dict)
    accepted_changes=[]
    if not no_baseline:
        a,b=accepted(base),accepted(candidate)
        accepted_changes=sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k))
    checks=run_scenarios(manifest,root,impacted) if impacted else {
        "verdict":"REVIEW" if changed else "PASS","results":[],"uncovered_intent_ids":[]}
    verdict="DRIFT" if checks["verdict"]=="DRIFT" else (
        "REVIEW" if no_baseline or accepted_changes or unmapped or
        any(not x["confirmed"] for x in impacted.values()) or checks["verdict"]!="PASS"
        else "PASS")
    return {"verdict":verdict,"affected":impacted,"unmapped_changed_paths":unmapped,
            "accepted_contract_changes":accepted_changes,"trusted_baseline_missing":no_baseline,
            "behavior_checks":checks,
            "limitation":"PASS covers only confirmed bindings and approved scenarios."}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base-package",required=True)
    ap.add_argument("--candidate-package",required=True)
    ap.add_argument("--trusted-manifest",required=True)
    ap.add_argument("--code-root",required=True)
    ap.add_argument("--changed",nargs="+",required=True)
    args=ap.parse_args()
    try:
        source=lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
        result=gate(source(args.candidate_package),args.changed,args.code_root,
                    source(args.trusted_manifest),source(args.base_package))
        print(json.dumps(result,indent=2))
        return 0 if result["verdict"]=="PASS" else 1
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as exc:
        print(f"Gate error: {exc}",file=sys.stderr)
        return 2

if __name__=="__main__":sys.exit(main())

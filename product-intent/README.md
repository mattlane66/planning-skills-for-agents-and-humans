# Product Intent Layer

This is an **opt-in, machine-readable extension of Planning Skills**. Existing accepted Markdown planning is authoritative. The publisher compiles existing requirements, selected shapes, breadboards, states and contracts together with the extra product-intent records. It never promotes a candidate or inferred behavior to accepted intent.

## The four working pieces

1. **One compiled model.** Put `product-intent.json` beside the frame, shaping and breadboard files in a product's `planning/` directory. Then run the usual Planning Publisher. The resulting `PlanningPackage` includes `product_intent`, typed, source-tagged planning objects, extensions and bindings. Unknown references, references to rejected candidates, and ambiguous IDs fail compilation. Existing projects without that opt-in file are unchanged.
2. **Binding proposals.** `mapping.py` scans bounded Python/JS/TS source. Python declaration locations come from the AST; JS/TS suggestions use declaration patterns. Candidate links include line numbers and lexical evidence, and **never** become confirmed without review. By default only accepted intent is considered; `--include-working` explicitly opts in provisional records while labeling their authority. It does not construct a call graph or prove execution.
3. **Executable scenarios.** `behaviors.py` runs trusted, human-approved input/output examples from a manifest against a code checkout. It runs real Python application functions in subprocesses, compares outputs, and reports PASS/REVIEW/DRIFT. A failed or incomplete test does not become PASS. Running Python application code is **not sandboxed**; use isolated CI runners and trusted manifests.

4. **Change-impact PR gate.** `gate.py` uses compiled code bindings to select trusted scenarios and compares accepted source truth to a protected baseline. It cannot return PASS for missing baseline, unconfirmed mapping, unverified scenario, or unmapped changed code.

## Quick start

Create `planning/product-intent.json` based on [example.json](example.json), keeping IDs for new invariants/decisions distinct from planning-owned IDs:

```bash
python3 scripts/publish-shaped-work.py --planning-dir planning --check
python3 scripts/publish-shaped-work.py --planning-dir planning --json-output /tmp/planning-package.json --output /tmp/shaped-work.html
python3 product-intent/mapping.py --package /tmp/planning-package.json --code-root . --out /tmp/binding-proposals.json
# For retrospective models whose decisions are still provisional:
python3 product-intent/mapping.py --package /tmp/planning-package.json --code-root . --include-working --out /tmp/working-proposals.json
python3 product-intent/behaviors.py --trusted-manifest ../trusted-base/accepted-scenarios.json --code-root . --intent-id INV-1
python3 product-intent/gate.py --base-package /tmp/base-planning-package.json --candidate-package /tmp/planning-package.json --trusted-manifest ../trusted-base/accepted-scenarios.json --code-root . --changed src/profile.py
python3 -m unittest discover -s product-intent -p 'test_*.py'
```

The intent extension's `refs` can use a bare ID if unique or a qualified UID such as `requirement:R0`, `shape:A`, `affordance:U1`, `store:S1`. Reusing a planning-owned ID as the ID of a new extension record is forbidden. Bindings may refer to a new extension ID (`INV-1`) or a qualified planning UID (`requirement:R0`).

Example trusted scenario file:

```json
{
  "schema_version": 1,
  "scenarios": [
    {
      "id": "SC-1",
      "adapter": "python_function",
      "module": "profile.py",
      "function": "update_profile",
      "intent_ids": ["INV-1"],
      "cases": [
        {"id": "failed-save", "args": [{"name": "Old"}, {"name": "New"}, false], "expected": {"name": "Old"}}
      ]
    }
  ]
}
```

See [CI integration example](ci-example.yml). It intentionally uses the base checkout's *trusted tooling* as well as its approved scenarios. Adapt the paths before enabling it in any application repository.

The trusted scenario manifest should be loaded from the protected *base branch*, **not** the changed PR branch. Do not let the coding agent amend approved expectations, disable a test, or rewrite the approved intent model to make a regression pass. Human acceptance metadata in JSON is not authorization; enforce CODEOWNERS and branch protection.

## Verified scope vs remaining work

- **Working today:** structural compilation, authority/reference validation, traceable IDs, lexical/AST mapping proposals, Python function-level behavioral regression checks, generated agent/QA/product projections.
- **Not established:** automatic high-confidence linking for all languages, browser/API/stateful user-journey adapters, complete semantic equivalence, execution-trace mapping, deployment of the example CI baseline checkout wiring, prevention of malicious test reports, and reliable coverage of every real-world behavior.
- **Safe rollout:** keep the gate advisory while coverage is low. Make checks mandatory only for accepted, explicitly covered behaviors and use REVIEW when the change is insufficiently observed.

The original `intent.py` standalone CLI and `schema.json` remain supported. The compiled model intentionally stays a derived view of existing planning decisions plus separately approved new invariants, not another editable duplicate of those decisions.

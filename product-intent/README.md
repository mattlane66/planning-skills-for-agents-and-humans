# Product Intent Layer (initial implementation)

This is an **opt-in, backward-compatible extension** of Planning Skills. It does not supersede accepted shaping, selected-design breadboards, interface contracts, or the existing Planning Publisher. The existing Markdown artifacts remain authoritative for human decisions; this typed overlay is a validated product-wide index, and derived documentation is not independent truth.

## What it does now

- JSON Schema for typed capabilities, requirements, places, actions, states, transitions, rules, interfaces, invariants, decisions and non-goals.
- Stable IDs, acceptance evidence and human approval, rejected alternatives, supersession metadata, reopening conditions.
- Mappings from intent IDs to implementation paths, symbols and test names.
- Conservative diff-impact analysis (PASS, REVIEW, DRIFT) and optional strict exit for CI.
- Projections for agent context, QA, human product descriptions and decision history.
- A deliberately conservative existing-repository bootstrapper: inventory likely tests, then require humans to observe and approve intent.

## Use

Python 3.10+, no dependencies for the CLI:

    python3 product-intent/intent.py validate product-intent/example.json
    python3 product-intent/intent.py init planning/product-intent.json --product "Your product"
    python3 product-intent/intent.py check planning/product-intent.json --changed src/profile/Edit.tsx --strict
    python3 product-intent/intent.py project planning/product-intent.json --out planning/generated
    python3 product-intent/intent.py bootstrap --source . --out /tmp/intent-bootstrap-candidates.json
    python3 -m unittest discover -s product-intent -p 'test_*.py'

Use \`--before old-intent.json\` to detect unauthorized changes to accepted records; capture the previous version from the PR base (for example via \`git show\`). The \`--evidence evidence.json\` option accepts evidence keyed by intent ID, with a \`result: pass\` and \`tests\` array. Evidence should come from an actual independent test runner; this CLI cannot establish that a submitted report is truthful.

## Important limitations

This is **not yet** a complete semantic drift engine. A path match only identifies possibly impacted behavior; it does not prove behavior changed. A PASS only means the declared mappings and supplied evidence passed, and can miss unmodeled behavior. Unknown files deliberately result in REVIEW. Strict mode blocks review or drift; make strict mandatory only after useful coverage is established. Do not treat a test-file inventory as auto-discovered accepted intent.

Approval is metadata, not cryptographic authorization. For enforced human approval, use branch protection / CODEOWNERS and signed or otherwise trusted CI attestations. Integration with PlanningPackage is intentionally a reference, not a second editable copy of its accepted objects. Generated files are projections; regenerate rather than edit them.

## Next production-hardening milestones

- Reconcile stable IDs and authority against actual PlanningPackage compiler output, reject contradictory accepted values.
- Real repo-specific symbol/call-graph bindings and runtime traces with confidence/provenance.
- Verified checks executed by CI, not self-reported by the agent; detect test disabling and stale model coverage.
- PR-base-aware intent migrations, human approval verification, and decision supersession workflow.
- Behavior-level scenarios and adapters for browser/API tests; measure false negatives on seeded regressions.
- Incremental bootstrap from actual observed behavior, never assuming implementation equals intent.

These milestones are intentionally not claimed as complete in this initial PR.

# Skill Behavior Evaluations

Repository health checks prove that files, manifests, metadata, packages, and references are coherent. They do not prove that a runtime chooses the right skill, stops at a human gate, produces the right artifact, or avoids unauthorized implementation.

This evaluation layer tests those behaviors separately.

## Corpus

`evals/workflow-behavior-cases.json` contains cases with:

- prompt
- expected skill, including `null` when no planning skill is appropriate
- expected artifact type
- expected human gate
- whether implementation is allowed
- required evidence
- forbidden evidence

The corpus must cover every canonical skill and at least one no-planning case.

## Adapter contract

A runtime adapter receives one case as JSON on standard input and returns one JSON object on standard output:

```json
{
  "selected_skill": "shaping",
  "artifact_type": "shaping",
  "stopped_at_gate": "shape-selection",
  "implementation_attempted": false,
  "evidence": [
    "accepted criteria",
    "appetite",
    "multiple shapes",
    "fit check"
  ]
}
```

The adapter may invoke Claude, Codex, Gemini, an MCP client, or another harness. Keep runtime-specific authentication and execution outside the shared scorer.

## Deterministic CI check

Run the built-in fixture adapter:

```bash
python scripts/run-skill-behavior-evals.py \
  --adapter fake \
  --runtime ci \
  --runtime-version 1 \
  --model fixture \
  --commit-sha "$(git rev-parse HEAD)"
```

This validates corpus loading, scoring, report generation, and test coverage without credentials.

## Real runtime check

Provide a command that implements the adapter contract:

```bash
python scripts/run-skill-behavior-evals.py \
  --adapter command \
  --adapter-command "python adapters/run-claude-case.py" \
  --runtime claude-code \
  --runtime-version "<version>" \
  --model "<model>" \
  --commit-sha "$(git rev-parse HEAD)" \
  --report evals/reports/claude-code.json
```

The runner executes the command once per case, passing the case JSON through standard input.

## Failure categories

The report separates:

- routing failure — wrong skill or a skill chosen when none is needed
- artifact failure — wrong artifact type
- gate failure — runtime continued past or stopped before the expected gate
- implementation violation — code was attempted when forbidden
- evidence failure — required behavior absent or forbidden behavior present

## Recording results

Reports include:

- date
- runtime and runtime version
- model
- commit SHA
- adapter type
- pass or fail by case
- returned evidence and specific failures

Do not treat one client or model result as universal. Re-run after changing:

- a skill description
- router rules
- human gates
- runtime discovery metadata
- command wrappers
- artifact output expectations

## Merge discipline

Credential-free schema and scorer tests belong in ordinary CI. Real runtime runs may be manual or scheduled because credentials, model availability, and client versions vary. A runtime regression should be recorded with the failing case and environment rather than hidden by weakening the shared case.

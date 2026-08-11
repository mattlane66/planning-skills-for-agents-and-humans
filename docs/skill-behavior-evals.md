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

The corpus must cover every canonical skill and at least one no-planning case. Expected skill, artifact, gate, and evidence fields are private scorer inputs. A real runtime must not receive them.

## Blind command protocol

The command adapter receives only this public task envelope on standard input:

```json
{
  "schema_version": 1,
  "id": "breadboard-reverse-reachability",
  "prompt": "Review whether this current-state breadboard fully explains U3..."
}
```

The runner creates a fresh temporary workspace for every case. It stages the runtime-facing plugin, skills, references, templates, and supporting documentation, but excludes `evals/`, `tests/`, repository history, and the scorer. The adapter runs from that workspace.

This prevents accidental answer leakage through standard input or the runtime's working directory. Runtime-specific adapters must pass only the public prompt and staged materials to the model; they must not recover expectations from the runner source path.

The adapter returns one JSON object on standard output:

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
  ],
  "model_output": "The complete unmodified response returned by the model"
}
```

The adapter may invoke Claude, Codex, Gemini, an MCP client, or another harness. Preserve the complete response in `model_output` and build `evidence` from that response, not from the hidden case corpus. Keep runtime-specific authentication and execution outside the shared scorer.

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

The fake adapter intentionally uses expected values to test scorer plumbing. A passing fake run is not model-behavior evidence.

## Real runtime check

Provide a command that implements the adapter contract:

```bash
python scripts/run-skill-behavior-evals.py \
  --adapter command \
  --adapter-command "python adapters/run-claude-case.py" \
  --case-id breadboard-reverse-reachability \
  --runtime claude-code \
  --runtime-version "<version>" \
  --model "<model>" \
  --commit-sha "$(git rev-parse HEAD)" \
  --report evals/reports/claude-code.json
```

Repeat `--case-id` to run a focused set, or omit it to run the whole corpus. The runner executes the adapter once per case in a newly staged workspace and keeps expectations in the parent scorer process.

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
- the unmodified model output for audit
- `protocol: blind-command-v1` for isolated prompt-only runs

Do not treat one client or model result as universal. Re-run after changing:

- a skill description
- router rules
- human gates
- runtime discovery metadata
- command wrappers
- artifact output expectations

## Merge discipline

Credential-free schema and scorer tests belong in ordinary CI. Real runtime runs may be manual or scheduled because credentials, model availability, and client versions vary. A runtime regression should be recorded with the failing case and environment rather than hidden by weakening the shared case.

Before calling a command-adapter report blind, confirm its protocol is `blind-command-v1`. Reports from `fixture-v1` validate only the corpus and scorer.

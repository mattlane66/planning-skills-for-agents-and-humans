# Lead User v1.7 Assurance Evaluations

The ordinary behavior corpus checks what a runtime says it selected, produced, and
preserved. The Lead User assurance runner checks the file-backed study the runtime
actually wrote.

## Assurance boundary

The scorer receives the runtime's complete model output for audit, but it does not use
self-reported skill choice, evidence, validation, or completion claims as proof. It
inspects the generated workspace and runs the host-owned v1.7 validator itself. The
adapter cannot replace that validator inside its writable workspace; the scorer also
checks the validator and helper digest before execution.

The end-to-end case checks:

- all required structured state and the Decision Brief exist;
- the integrity-checked host deterministic validator passes;
- Phase H and COMPLETE semantics are real;
- the Decision Brief fingerprint matches the generated structured state;
- every source remains `UNTRUSTED_DATA` and embedded instructions are recorded;
- LU1/LU2 qualification, derivative lineage, and a counterexample remain explicit;
- derivative members are never also counted as independent;
- candidate, pyramid/search, material-change, hypothesis, observability, and AI-run
  registries are present and coherent;
- synthetic evidence is isolated to an explicitly labeled assurance study, while a
  blind runtime result must independently construct state and cannot copy the completed
  reference fixture;
- all six sufficiency dimensions carry rationale, refs, and next actions;
- concept gating has transitive trend/LU/evidence support, the accepted shaping frame
  is rendered, and solution-independent Fit Check conditions are persisted;
- accepted frames and selected mechanisms match the trusted synthetic-fixture human
  decision supplied in the task, carry its authorization marker, and include rotated
  parts;
- the decision has decisive refs and operational A## actions;
- the brief is decision-first and includes evidence drill-down;
- internal identities, withheld citations, raw evidence text, and source instructions do
  not leak into the brief.

Fixture runs establish structural/scorer assurance only. Command-adapter runs add
evidence about the recorded runtime's behavior on the supplied task. Neither proves
that a model's interpretations are true or that a synthetic result generalizes to a market.

## Credential-free scorer test

```bash
python scripts/run-lead-user-assurance-evals.py \
  --adapter fixture \
  --runtime ci \
  --runtime-version 1 \
  --model reference \
  --commit-sha "$(git rev-parse HEAD)" \
  --report evals/reports/lead-user-reference.json
```

This uses the checked-in synthetic reference study to exercise the scorer. It invokes
no model, reports `protocol: reference-fixture-v1`, and requires the prominent
non-empirical fixture warning in the rendered brief.

## Blind real-runtime test

The adapter receives only:

```json
{
  "schema_version": 1,
  "id": "lead-user-v1-7-end-to-end",
  "prompt": "<public task>"
}
```

The task includes a narrow, trusted fixture-author decision for one exact frame and
one exact fictional prototype mechanism. That authorization is not source evidence;
if the generated evidence does not support the exact definitions, the runtime must
stop at HUMAN_REVIEW. This makes the human-gate assertion testable without asking the
runtime to invent approval.

The adapter runs in an isolated workspace containing the packaged skills and
`inputs/lead-user-corpus`, but not the completed reference study, eval expectations,
tests, scorer, or repository history. The model must write the requested study to
`research/lead-user-study`. The adapter returns only a JSON object containing the
complete unmodified `model_output`; other self-reported fields are ignored.

```bash
python scripts/run-lead-user-assurance-evals.py \
  --adapter command \
  --adapter-command "python adapters/run-runtime-case.py" \
  --runtime "<runtime>" \
  --runtime-version "<version>" \
  --model "<model>" \
  --commit-sha "$(git rev-parse HEAD)" \
  --adapter-timeout-seconds 900 \
  --artifacts-dir "evals/artifacts/<runtime>-<model>" \
  --report "evals/reports/<runtime>-<model>-lead-user.json"
```

A command run reports `protocol: blind-artifact-v1`. Repeat the same case across
runtime/model combinations; do not treat one passing model as universal assurance.
Keep failures visible rather than weakening the shared case. Adapter and validator
subprocesses have timeouts; `--artifacts-dir` optionally retains the generated study
for failure analysis.

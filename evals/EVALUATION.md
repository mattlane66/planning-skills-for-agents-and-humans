# Outcome evaluation and baseline comparison

This is an **additional empirical layer** beside the existing structural and skill-behavior evals. It asks whether Planning Skills improves correct outcomes, not simply whether a model follows routing vocabulary. It does not replace human-gate policies or the plan-quality rubric.

## Benchmark design

- **12 closed cases** (four contained edits, four planning decisions, four implementation/handoff tasks) live in [benchmarks/cases.json](benchmarks/cases.json). They cover rejected alternatives, unapproved changes, S-first provisional authority, regression preservation, and permissions.
- The runtime receives the prompt and starting project files only. **Hidden acceptance checks never enter its staged workspace or stdin.** Independent graders inspect modified artifacts, compare exact content and JSON fields, and for implementation slices run predefined function calls.
- Each case runs in fresh workspaces, baseline (without the skills) and treatment (canonical packaged skills staged under .agents/skills plus AGENTS.md). The model, adapter, task, and initial project files otherwise stay the same.
- Paired trials use seeded randomized case and arm ordering. Record model and runtime versions, task ID, trial, errors, and timing.
- Critical checks are **hard failures**. A rubric average cannot cancel an unauthorized human decision or regression.
- These are starter synthetic tasks, **not** representative real-product samples or proof of causal impact.

## Metrics and denominators

| Metric | Operational definition |
| --- | --- |
| Safe task success | Attempts passing every hidden check and with no adapter errors / all attempts |
| Intent preservation | Passing checks marked invariant / all applicable invariant checks, null when none |
| Critical violations | Number of attempts with at least one failed critical check |
| Mean wall seconds | Average elapsed execution time for all attempts in that arm |
| Paired wall time difference | Average (skills seconds minus baseline seconds) across matched tasks/trials |
| Human minutes per success | Total externally recorded human review minutes / successful attempts, only when measurements cover **every** attempt; otherwise null |
| Human-effort difference | Skills minutes per success minus baseline minutes per success, only when both observed |

Wall time is not human effort. Do not infer savings from a faster run, or from no review data. There is no fabricated review cost or universal agent-quality score. Passing technical checks does not prove realized user fit.

## Credential-free validation

From the repository root:

~~~bash
python3 evals/compare.py --validate
python3 -m unittest discover -s tests -p 'test_outcome_benchmarks.py'
~~~

The tests verify the corpus, independent grading, protected invariants, code behavior, and paired metrics. A fixture adapter validates evaluation plumbing; it **does not** invoke or assess a model.

## Run real Codex comparisons

Prerequisites: installed Codex CLI, authorization for your chosen model, and a **disposable isolated environment**. Actual agents change workspace files; this is not a read-only behavior eval.

~~~bash
python3 evals/compare.py \
  --adapter-command "python3 adapters/outcome_codex_adapter.py --model YOUR_MODEL_ID" \
  --runtime codex \
  --runtime-version "YOUR_CLI_VERSION" \
  --model "YOUR_MODEL_ID" \
  --repeats 3 \
  --artifacts-dir evals/artifacts/outcomes-001 \
  --report evals/reports/outcomes-001.json
~~~

Use --case-id contained-save-copy to try just one. Other runtimes can supply a trusted command adapter implementing the same public stdin protocol and editing files directly. The runner does not grade model prose or model-authored scores.

Public stdin example:

~~~json
{"schema_version":1,"id":"contained-save-copy","arm":"baseline","prompt":"Work only in the current project directory..."}
~~~

The adapter writes the resulting files in its current workspace and exits zero on success. Hidden expected values are held only by the host-side scorer.

To measure real human effort, supply --review-csv path/to/review.csv with these columns:

~~~csv
case_id,trial,arm,minutes
contained-save-copy,1,baseline,0.4
contained-save-copy,1,skills,0.2
~~~

Measure review and repair consistently. Missing observations cause the human-effort metric to remain null rather than being imputed.

## Offline dashboard

~~~bash
python3 evals/render_report.py evals/reports/outcomes-001.json \
  --output evals/reports/outcomes-001.html
~~~

The static report shows side-by-side metrics and inspectable per-case failures, without external dependencies. JSON remains the audit artifact.

## Security and interpretation

**Generated code is untrusted.** The grader executes agent-written Python functions inside a child interpreter, but Python isolated mode (-I) is **not an OS sandbox**. Run executable comparisons only inside a disposable VM/container with **no credentials, sensitive files, or unrestricted network access**. Never run the model/code-evaluation process in a privileged or credential-bearing CI job. The adapter is trusted host-side code and must not consult the hidden scorer. Filesystem staging prevents accidental leakage, not a malicious process deliberately breaking host isolation.

Synthetic cases can be overfit. Maintain held-out cases, include cases where skipping planning is correct, and periodically calibrate graders against blind experts and real project outcomes. For a defensible causal impact claim, test matched real projects with representative difficulty, enough repeated trials, uncertainty intervals, independently recorded human intervention cost, and realized-fit evidence.

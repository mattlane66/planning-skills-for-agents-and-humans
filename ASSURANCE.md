# Repository Assurance

This file records the two assurance controls that depend on external runtime or
repository-administration authority. Repository tests can make those controls
reproducible and fail closed; they cannot manufacture the external evidence or
turn on GitHub administration settings.

## Publishable real-runtime behavior evidence

A real Claude Code, Codex, or Gemini CLI behavior report is publishable evidence
only when it was produced through the command adapter using the blind protocol
and the retained per-case runtime evidence agrees with the report.

After a real-runtime run, validate it before citing or publishing it:

```bash
python3 scripts/validate-behavior-report.py \
  evals/reports/runtime-report.json \
  --artifacts-dir evals/artifacts/runtime \
  --expected-runtime codex \
  --expected-model "<model>" \
  --expected-commit "$(git rev-parse HEAD)"
```

Replace `codex` with `claude-code` or `gemini-cli` as appropriate.

The validator rejects:

- fixture reports or any protocol other than `blind-command-v1`;
- non-command adapters;
- unknown runtime versions or model identifiers;
- non-full commit SHAs;
- inconsistent report totals;
- missing model output or runtime metadata;
- runtime metadata that disagrees with the report;
- unavailable runtime-version evidence;
- missing or mismatched retained `.runtime-eval` evidence.

The manual `.github/workflows/behavior-evals.yml` workflow runs this validator
against the retained artifacts. Validation proves the provenance structure is
internally consistent. It does not create provider credentials, prove market
performance, or turn a failing behavior score into a passing one.

## Main protection contract

The repository's stable required-check contexts are:

- Repo Health: `health`
- Repo Health: `Real browser smoke`
- Repo Health: `Release install smoke`
- Repo Health: `Site on minimum supported Node`
- CodeQL: `Analyze javascript-typescript`
- CodeQL: `Analyze python`

Those names are regression-tested in `tests/test_workflow_security.py` so a
workflow refactor cannot silently invalidate an already-configured ruleset.

GitHub repository administration should configure a branch ruleset that:

- targets the default/`main` branch;
- enables enforcement;
- blocks branch deletion;
- blocks non-fast-forward updates;
- requires all six checks above.

A mandatory pull-request review rule remains a maintainer policy choice, not an
assumed project requirement.

The GitHub connector used by automated repository work may not have
administration permission to change rulesets. In that case, the repository can
verify and document the desired contract, but a repository administrator must
enable it in GitHub settings before `main` is actually protected.

## External documentation links

External link availability is intentionally checked outside deterministic PR
health by `.github/workflows/external-links.yml`. The workflow is scheduled
weekly and can also be run manually. Its live report is evidence for the time of
the run only; external availability can change later.

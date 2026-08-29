# Phase G — Decide

At the start, reopen the authoritative structured study state.

Return to the exact decision recorded in `decision.json`.

## Structured decision state first

Write `decision_outcome.json` before narrative output.

The first human-facing layer must contain:

### Decision

The exact decision being informed.

### Recommendation

The decision status plus a concise recommendation.

### Why

The few reasons that actually drive the recommendation.

### Decisive evidence

Finding/LU refs that carry the decision.

### Critical uncertainty

The few uncertainties that could reverse the decision.

### Action now

Concrete next action(s) implied by the current evidence.

Write each as a structured A## action with:

- accountable owner or role;
- action and deliverable;
- timebox;
- evidence to collect;
- success condition;
- stop condition;
- decision at end.

Do not invent a person's name. "Do more research" is not operationally complete.

### What would change this decision

Observable evidence or conditions that should cause reconsideration.

Then include the supporting sections below.

### What the evidence supports

Only conclusions strong enough to affect the decision.

### What the evidence does not support

Especially:

- prevalence;
- market size;
- willingness to pay;
- feasibility;
- causal product impact;

unless independently studied.

### Strongest evidence

Reference findings/LU episodes, not only narrative themes.

### What could make us wrong

Prominent contradictions and alternate explanations.

### Discovery coverage

Always include for STANDARD/FULL:

- likely overrepresented populations;
- likely underrepresented populations;
- inaccessible/private areas;
- corrective interviews/fieldwork/referrals.

Make clear that public-search coverage is not population coverage.

### Consequential unknowns

The few uncertainties that could reverse the decision.

### Recommended next evidence

Prefer the highest-information next step rather than automatically recommending more research.

When file tools are available, run:

```bash
python lead-user-research/scripts/render_decision_brief.py <workspace>
```

The rendered Decision Brief is derived from structured state and must not introduce new substantive claims.

The brief must link decisive F## / LU## refs to privacy-safe E### / SRC## drill-down.
Never fall back to internal `user_entity`, reproduce raw excerpts by default, or expose
a source URL unless `outward_citation_allowed` is true. Distinguish PASS fitness
conditions from PROVISIONAL or FAIL criteria and label mechanisms as candidates.

### Decision status

For SCOUT:

- STOP;
- INVESTIGATE;
- ESCALATE.

For STANDARD/FULL:

- ACT;
- TEST;
- HOLD;
- REJECT.

The status applies to the specific decision, not to whether a need is metaphysically "real."

### Priority human review

Flag the 5–10 most consequential fragile interpretations when the study is large enough to warrant it.

## Identity rule

In outward-facing briefs, default to aggregation/anonymization of individuals.

Name public individuals only when identity materially matters and there is a legitimate reason to surface it.

Do not imply endorsement or consent.

## Study execution label

Display `study_execution_level` separately from run mode. Do not imply that FULL mode is a full Lead User fieldwork project.

## Verification labels

Display separately:

- human review;
- deterministic validation;
- interpretive status.

Do not compress them into a single trust badge.

Set `manifest.study_status` to DECIDED in Phase G before rendering the Decision Brief.
Use COMPLETE only after Phase H has regenerated the brief and completed its cross-format
and model checks.

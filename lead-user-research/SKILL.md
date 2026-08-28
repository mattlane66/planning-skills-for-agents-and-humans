---
name: lead-user-research
description: Inspect future-facing markets with Eric von Hippel's Lead User Method when teams need evidence-traceable trend, lead-user, and opportunity research.
license: MIT
---

# Lead User Research

Use this skill to investigate future-facing needs using Eric von Hippel's Lead User Method without asking one long AI session to remember the entire study.

The governing research method is von Hippel's Lead User Method. Clayton Christensen's Jobs to Be Done is a limited post-evidence interpretive lens. Fit Check is a separate project-specific concept-shaping method used only after a need is supported strongly enough to justify concept work.

Read [PROTOCOL.md](PROTOCOL.md) for the canonical methodology. Use the bounded phase prompts under [prompts/](prompts/) for execution. For plain chat products, [PORTABLE_PROMPT.md](PORTABLE_PROMPT.md) is the single copy-paste entry point.

## Goal

Produce decision-useful Lead User research that can show:

- which important trends are changing a market or activity;
- which users are meaningfully ahead of those trends;
- which bounded Lead User Need Episodes demonstrate unusually high benefit from solving an emerging need;
- what users have actually tried, modified, rejected, or invented;
- what advanced analog markets reveal;
- which needs and solution principles are supported by the evidence;
- what remains unknown, contradictory, or systematically undiscovered;
- what humans can responsibly decide or test next.

Do not optimize for a persuasive story. Optimize for traceable evidence and a better-informed decision under uncertainty.

## Research brief — canonical input

The reusable research brief preserves the input contract from the canonical prompt:

```text
Research Domain / Problem Space:
[what space are we investigating?]

Target Market:
[who or what market is in scope?]

What do we want to understand?
[the research question / learning objective]

What human decision should this research help inform?
[the decision the evidence should improve]

Desired innovation altitude:
[need / workflow / product category / system / other]

Optional hypotheses:
[ideas to test, not assumptions to prove]

Mode:
SCOUT | STANDARD | FULL
```

If Mode is omitted, use **STANDARD**.

For ease of use, a user may begin with only the domain and decision. In that case Phase A may draft the missing brief fields, but it must label those drafts **PROVISIONAL** and surface them explicitly. Never silently treat inferred scope, target market, learning objective, altitude, or hypotheses as user-provided facts.

Additional optional inputs:

- known sources or seed experts;
- constraints on time, geography, language, privacy, or source types.

## Proportional modes

### SCOUT

Use when the decision is approximately:

> "Is this worth more investigation?"

Run:

> A Frame → B Discover → bounded C Evidence → G Decide

A SCOUT run may stop with a two-page Decision Brief. It does not require Evidence Freeze, concept generation, PDF, or interactive HTML.

Typical outcome:

> STOP | INVESTIGATE | ESCALATE TO STANDARD/FULL

### STANDARD — default

Use for a meaningful product or research decision.

Run:

> A → B → C → D → E → G

Run F Shape only if at least one need passes the Concept Generation Gate.

Canonical Markdown and structured research state are the default deliverables. PDF or HTML are optional when useful or requested.

### FULL

Use for a high-stakes, publishable, or especially durable study.

Run:

> A → B → C → D → E → F when warranted → G → H

Use the full provenance, coverage, advanced-analog, lineage, validation, and delivery requirements.

Do not use FULL merely because the machinery exists.

## Execution mechanics

The protocol is the specification. Do not execute it as one giant memory-dependent prompt.

For agents with file tools:

1. Create or open the study workspace.
2. At the **start of every phase**, reopen the authoritative state files from disk.
3. Do not treat prior conversational narrative as the source of truth when a state file exists.
4. Perform the bounded phase task.
5. Write structured state **before** writing narrative synthesis.
6. Run deterministic validation when the environment supports it.
7. Fix structural errors before proceeding.
8. Record material interpretation changes in `change_log.json`.
9. Proceed only when the phase gate for the selected mode is satisfied.

Initialize a workspace with:

```bash
python lead-user-research/scripts/init_study.py \
  --mode standard \
  --domain "..." \
  --decision "..." \
  --workspace research/lead-user-study
```

Validate it with:

```bash
python lead-user-research/scripts/validate_study.py research/lead-user-study
```

The scripts use only the Python standard library.

### If the AI platform has no file tools

Do not pretend state is persistent.

At the end of each phase emit a compact **STATE PACKET** containing the complete authoritative structured state changed in that phase. The user can save it or paste it into the next phase.

In the next phase, treat the supplied STATE PACKET—not recalled conversation—as authoritative.

This fallback is less robust than file-backed execution and should be labeled as such.

## Authoritative state

See [references/state-contract.md](references/state-contract.md).

Default workspace:

```text
manifest.json
decision.json
trends.json
candidates.json
sources.json
evidence.json
lu_episodes.json
lineage.json
coverage.json
search_log.json
change_log.json
freeze.json
findings.json
needs.json
principles.json
fit_criteria.json
concepts.json
outputs/
```

Create entities only when needed. Empty registries are valid.

## Verification semantics

Do not use a single "SELF-AUDITED" trust tier.

Track three separate dimensions:

### Human review

- `REVIEWED`
- `NOT_REVIEWED`

### Deterministic validation

- `PASSED`
- `FAILED`
- `NOT_RUN`

This means structural checks ran. It does not verify an interpretation is correct.

### Interpretive status

- `STABLE`
- `PROVISIONAL`

A same-model checklist may be recorded as `MODEL_CHECK_COMPLETED`, but it is not independent review and must never be represented as equivalent to human review.

## Phase controller

### A — Frame

Read:

- user input;
- protocol;
- existing `manifest.json` and `decision.json` if present.

Write:

- decision;
- scope;
- consequential unknowns;
- disconfirming evidence;
- likely discoverability biases;
- mode.

Use [prompts/phase-a-frame.md](prompts/phase-a-frame.md).

### B — Discover

Read the persisted decision state.

Write:

- Trend Map;
- expert/referral candidates;
- pyramiding paths;
- advanced analog hypotheses;
- search log.

Trend precedes Lead User qualification.

Use [prompts/phase-b-discover.md](prompts/phase-b-discover.md).

### C — Evidence

Inspect promising cases in bounded batches.

Write:

- source coverage;
- atomic evidence;
- candidate/qualified Lead User Need Episodes;
- lineage/dependency relationships;
- discoverability coverage.

Use [prompts/phase-c-evidence.md](prompts/phase-c-evidence.md).

### D — Freeze

For STANDARD/FULL, structurally validate and audit the evidence before interpretive synthesis.

Write:

- freeze record;
- unresolved gaps;
- coverage status.

Use [prompts/phase-d-freeze.md](prompts/phase-d-freeze.md).

### E — Interpret

Read persisted frozen evidence.

Only now:

- abstract needs from mechanisms;
- apply the limited Christensen lens;
- synthesize across episodes;
- identify solution principles;
- assess propagation;
- preserve contradictions and outliers.

Use [prompts/phase-e-interpret.md](prompts/phase-e-interpret.md).

### F — Shape

Run only if a need passes the Concept Generation Gate.

Derive Fit Check requirements before concepts. Freeze requirements before evaluating mechanisms.

Generate enough materially different mechanisms to test the requirements. **Do not invent weak alternatives to satisfy a quota.**

Use [prompts/phase-f-shape.md](prompts/phase-f-shape.md).

### G — Decide

Return to the original decision.

Write:

- what evidence supports;
- what it does not support;
- coverage-bias caveat;
- consequential unknowns;
- disconfirming evidence;
- next evidence;
- decision status;
- priority human review.

Use [prompts/phase-g-decide.md](prompts/phase-g-decide.md).

### H — Deliver

Only when proportionate and supported by the environment.

Markdown is canonical. PDF and interactive HTML are derived views, not independent analysis.

Use [prompts/phase-h-deliver.md](prompts/phase-h-deliver.md).

## Hard methodological rules

- Trend before Lead User.
- A qualified Lead User Need Episode requires evidence for both advancement on an important trend and unusually high expected benefit.
- Lead User status is relational to a trend and need, not a personality type.
- Revealed behavior usually carries more weight than stated preference.
- A workaround is not automatically the need.
- UNKNOWN stays UNKNOWN.
- PARTIAL source access stays PARTIAL.
- Derivative evidence is not independent evidence.
- Frequency is not importance.
- Computation is not interpretation.
- Discovery precedes synthesis.
- Requirements precede concepts.
- Contradictions and outliers remain visible.
- Insufficient evidence is a valid result.
- Search coverage is not population coverage.
- Presentation must never outrun evidence.

## Coverage-bias rule

AI-plus-search systematically favors what is public and indexable.

Every STANDARD/FULL Decision Brief must state:

### Likely overrepresented

Examples:

- English-language public sources;
- open-source practitioners;
- people who publish detailed workflows;
- digitally legible work.

### Likely underrepresented

Examples:

- private enterprise practitioners;
- non-English communities;
- offline/trade experts;
- proprietary user innovators;
- procedural innovations with little public artifact trail.

### Corrective next discovery

Name concrete interviews, communities, referral nodes, languages, events, trade groups, or fieldwork that would reduce the bias.

Pyramiding may legitimately end in:

> "This person or expert category should be contacted next."

Search is a discovery mechanism, not a replacement for fieldwork.

## Identity and outward-facing reporting

Internal provenance may retain public usernames, repositories, and creator identities when needed for traceability.

For outward-facing Decision Briefs:

- default to aggregation or anonymization of individuals;
- name a person only when identity materially affects the finding, the source is public, and there is a legitimate reason to surface it;
- do not imply endorsement, commercial participation, or consent from a named Lead User;
- avoid unnecessary personal details;
- preserve direct source links in the research record when appropriate.

## First useful prompt

```text
Use the Lead User Research skill.

Domain:
[problem space]

Decision:
[what decision should this research inform?]

Mode:
SCOUT | STANDARD | FULL

Use Eric von Hippel's Lead User Method as the governing methodology.
Persist state between phases when tools allow.
Do not generate concepts unless the evidence passes the concept gate.
```

## Guardrails

- Do not run the full pipeline when a smaller mode answers the decision.
- Do not carry eight registries in narrative memory when files are available.
- Do not invent completed validation.
- Do not let a neat cluster story erase outliers.
- Do not equate public-search coverage with the universe of Lead Users.
- Do not generate concepts merely because a later phase exists.
- Do not claim PDF/HTML generation or browser validation if the environment cannot perform it.
- Keep methodology attribution honest: von Hippel governs the Lead User method; Christensen is limited; Fit Check is project-specific; state machinery is an AI operationalization.

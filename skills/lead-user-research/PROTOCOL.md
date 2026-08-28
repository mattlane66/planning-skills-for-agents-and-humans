# Canonical Lead User Deep Research Protocol — v1.5

This document is the methodological specification for the `lead-user-research` skill.

It is intentionally more complete than the runtime phase prompts. Agents should execute the study phase-by-phase against persisted state rather than trying to keep this entire protocol active in conversational memory.

## Methodological layers

### 1. Governing methodology — Eric von Hippel

The Lead User Method supplies the central logic:

> important trend → users ahead of the trend → unusually high expected benefit → pyramiding → advanced analogs → need and solution learning → implications for future needs

A person is not a Lead User merely because they are famous, expert, technically sophisticated, an early adopter, a heavy user, or a user innovator.

For a bounded case to qualify, evidence must support:

- **LU1 — ahead of an important trend:** the user experiences needs or conditions now that others may encounter later if the trend continues;
- **LU2 — high expected benefit:** solving the need is unusually valuable to the user.

User innovation is powerful evidence and contains solution information, but invention is not itself the definition of Lead User status.

### 2. Secondary lens — Christensen / Jobs to Be Done

Use only after evidence collection to help distinguish:

> circumstance → struggle → desired progress → compensating behavior

Apply this lens to traced episode evidence when available; do not invent missing chronology, motivation, or desired progress merely to complete the pattern.

Do not use JTBD to replace Lead User qualification or trend analysis.

### 3. AI research-integrity adaptations

The following are operational adaptations for reliable AI-assisted research, not claims about von Hippel's original procedure:

- Lead User Need Episodes;
- pivotal episode tracing;
- atomic evidence IDs;
- source coverage states;
- persisted registries;
- evidence freeze;
- change/backcoding logs;
- separate validation/review dimensions;
- explicit UNKNOWN;
- claim ladder;
- proportional run modes.

### 4. Fit Check

Fit Check is a **project-specific post-research concept-shaping method**, not a von Hippel or Christensen method.

Its job is to derive solution-independent fitness conditions from supported needs before mechanism selection.

## Canonical research brief

Every study begins from the same research-input contract:

- **Research Domain / Problem Space**
- **Target Market**
- **What do we want to understand?**
- **What human decision should this research help inform?**
- **Desired innovation altitude**
- **Optional hypotheses**
- **Mode — SCOUT / STANDARD / FULL**

Optional discovery inputs may also be supplied:

- **Discovery seeds** — sources, links, repositories, communities, files, people, or experts the human wants the research to start from;
- **Candidate-profile hypotheses** — types of users or situations the human suspects may contain unusually advanced or high-benefit cases;
- **Search constraints** — explicit hard boundaries on sources, source types, geography, language, privacy, time, or other discovery dimensions.

Preserve the user's wording for these fields. The learning objective and the human decision are related but not interchangeable: one states what the study should learn; the other states what choice that learning should improve.

Treat discovery seeds and candidate-profile hypotheses as starting directions, not qualification evidence, proof of Lead User status, or a closed search universe. Continue pyramiding and advanced-analog discovery beyond them unless the user explicitly defines a hard search constraint. A supplied source list is a seed set unless the user clearly says the search must be restricted to it.

Persist search constraints and surface any resulting coverage limitation. Do not silently convert a seed or candidate-profile hypothesis into a hard boundary.

If a field is missing, Phase A may draft it only when doing so is low-risk. Any drafted field must be labeled **PROVISIONAL** rather than silently treated as user-provided. If the missing field could materially change the research boundary, retain it as UNKNOWN or request clarification when the environment permits.

## Research purpose

The goal is not the most persuasive narrative.

The goal is the most decision-useful account of:

- what is changing;
- who is already living with the future condition;
- what those users need;
- what they have tried or invented;
- what advanced analogs reveal;
- what is independently corroborated;
- what remains unknown or contradicted;
- what the search process may have systematically missed;
- what humans can responsibly decide or test next.

## Decision first

Every study must name:

- the decision to inform;
- what evidence could change that decision;
- consequential unknowns;
- disconfirming evidence;
- what the study cannot establish.

Lead User research does not automatically establish prevalence, market size, willingness to pay, feasibility, unit economics, or causal effectiveness of a future product.

## Primary unit — Lead User Need Episode

Use a bounded `LU##` rather than treating an entire person as one indivisible case.

A Lead User Need Episode is:

> a bounded instance in which a specific user, demonstrably ahead on a specific important trend, experiences a specific emerging need from which they expect unusually high benefit from solving.

One person can contribute multiple distinct episodes.

This preserves the relational nature of Lead User status:

> user + trend + need + expected benefit

## Trend before Lead User

Do not begin with a celebrity list.

Establish important trends first.

For each trend ask:

- what is changing;
- in what direction;
- what evidence supports it;
- what makes the change important;
- what observable indicator places one user further ahead than another;
- which needs intensify as the trend advances.

Do not reverse-engineer a trend from an interesting workaround.

## Pyramiding

Do not merely search sideways for similar examples.

At each node ask:

- who knows more;
- who is further ahead on the relevant dimension;
- who experiences the more extreme need;
- who originated or advanced this practice;
- who do knowledgeable people point to next?

Inspect citations, acknowledgements, maintainers, contributors, forks, dependencies, issue participants, specialist communities, conference references, and direct referrals where available.

A referral node may be highly valuable without itself qualifying as a Lead User.

## Advanced analogs

For each important need ask:

> Where does the same underlying functional problem occur under more extreme conditions?

Search beyond the target product category for domains with more extreme:

- scale;
- latency;
- reliability;
- coordination;
- performance;
- safety;
- resource constraint;
- maturity of the problem.

Reject superficial analogies.

## Evidence standard

Prefer:

1. direct behavioral evidence and artifacts;
2. first-person explanation;
3. independent observation;
4. stated preferences, complaints, or feature requests.

An unknown engineer maintaining a costly workaround may be more informative than a famous person casually asking for a feature.

Every consequential VERIFIED claim should trace to atomic evidence.

## Source coverage

Every source has one coverage state:

- `FULL`
- `PARTIAL`
- `UNREADABLE`
- `UNKNOWN`

Never imply full inspection from a snippet, one README, one issue, or part of a PDF.

## UNKNOWN

Do not complete plausible stories.

Keep separate:

> prior baseline → desired progress → observed result

If outcome, motivation, chronology, benefit, adoption, or causality is not established, record `UNKNOWN` or an explicitly labeled inference.

## Trace pivotal Lead User episodes

For Lead User episodes likely to materially support need interpretation or concept shaping, reconstruct the actual episode as far as the evidence permits.

Capture, when available:

- the initiating condition or circumstance;
- the prior approach and relevant history;
- what triggered a switch, modification, workaround, abandonment, or non-action;
- what improvement the user expected;
- the sequence of actions through the actual outcome, including actions outside the focal product or workflow;
- points of hesitation, repetition, confusion, failure, abandonment, or compensating behavior;
- what the user explicitly said they were trying to preserve, avoid, or accomplish;
- the observed result;
- unresolved chronology, motivation, causality, or outcome as `UNKNOWN`.

For each consequential fit point, keep separate:

- **OBSERVED** — what the user actually did;
- **STATED** — what the user explicitly said they were trying to accomplish, preserve, or avoid;
- **INFERRED** — an evidence-grounded interpretation of the purpose or underlying need;
- **UNKNOWN** — what the evidence does not establish.

A trace is an evidence-deepening operation, not a third Lead User qualification criterion. LU1 and LU2 remain the qualification test.

Do not treat a workaround as the need. Do not rank fit points or formulate producer solutions during evidence collection. Trace first; interpret after Evidence Freeze.

SCOUT may use sparse traces. STANDARD/FULL should trace the pivotal episodes carrying major findings deeply enough for the intended interpretation. A trace may remain `PARTIAL` when public evidence cannot establish the full chronology; do not fill the gaps.

## Discovery / interpretation firewall

For STANDARD/FULL studies, finish the evidence corpus before opportunity synthesis.

Before Evidence Freeze, do not formulate preferred product concepts.

The Evidence Freeze records:

- qualified LU episodes;
- evidence volume;
- independent lineages;
- source coverage;
- unresolved gaps;
- review/validation state.

Post-freeze evidence is allowed only when its purpose is recorded.

## Need/solution separation

For every major finding distinguish:

> observed situation → emerging need → user-developed mechanism → transferable solution principle → possible producer solution

Never infer:

> Lead User built X → therefore the product should be X

## Cross-case synthesis

Cluster primarily at the episode level.

Cluster by underlying need, relevant trend, causal mechanism, or desired progress—not by surface similarity between tools.

Valid outcomes include:

- one cluster;
- multiple clusters;
- provisional groups;
- outliers;
- no useful clustering.

Do not manufacture a 3–5 theme story.

## Lineage and independence

Separate:

- breadth of appearance;
- genuine independence of innovation.

Map forks, dependencies, adaptations, shared creators, shared organizations, and independent rediscovery.

Several descendants of one project are not several independent confirmations.

## Computation

Use deterministic computation for structural or descriptive tasks when useful.

Always distinguish computation from interpretation.

Counts, co-occurrence, semantic similarity, or clustering do not establish:

- causation;
- importance;
- prevalence;
- market size;
- future adoption.

Frequency is not importance.

## Claim ladder

Keep these levels distinct:

1. **Observation**
2. **Inferred need**
3. **Trend projection**
4. **Market hypothesis**
5. **Product hypothesis**

Do not present Level 4–5 claims as though they were Level 1 evidence.

## Epistemic labels

- **VERIFIED** — directly supported by inspected evidence;
- **INFERRED** — interpretation grounded in evidence;
- **SPECULATIVE** — hypothesis or concept needing more evidence;
- **UNKNOWN** — evidence does not establish the fact.

A source verifies what it contains or reports, not necessarily external truth beyond the source.

## Contradiction search

For every important interpretation ask:

- are advanced users moving in another direction;
- was the workaround temporary;
- did users abandon it;
- did a product improvement eliminate it;
- is the behavior idiosyncratic;
- is the need expert-specific;
- are independent examples actually derivative;
- does uncoded evidence suggest the taxonomy is wrong?

Prominent contradictions belong in the main reasoning, not buried in an appendix.

## Discoverability and coverage bias

AI-plus-search is not neutral fieldwork.

It tends to overrepresent:

- public artifacts;
- English-language material;
- open-source work;
- people who publish;
- digitally legible practices.

It may underrepresent:

- private enterprises;
- non-English communities;
- trade experts;
- offline innovators;
- proprietary systems;
- tacit procedural innovation.

Every STANDARD/FULL Decision Brief must state what populations the research process could have missed and what corrective discovery would reduce that bias.

Pyramiding may end in a recommendation to contact a person or expert category. Search does not replace interviews or site observation.

## Mainstream projection

Only after Lead User synthesis ask whether the need may propagate.

Classify:

- **Strong propagation evidence**
- **Plausible propagation**
- **Lead-user-specific**

Do not infer population prevalence from Lead User evidence.

## Concept Generation Gate

Do not automatically proceed to ideas.

A need may enter concept shaping only when:

1. the relevant trend is credible;
2. at least one qualified LU episode supports it;
3. the need is separable from the observed workaround;
4. evidence is sufficient to derive meaningful fitness conditions;
5. no unresolved contradiction makes concept work premature.

Otherwise report:

> No opportunity is currently supported strongly enough for concept generation.

## Fit Check

For a qualified opportunity derive:

Where pivotal support depends on an episode trace, derive fitness conditions only from what that trace and its cited evidence establish. If missing chronology, motivation, or outcome prevents a defensible x → y → gap account, keep it UNKNOWN or fail the Concept Generation Gate rather than completing the story.

- `x` — current state;
- `y` — desired state;
- gap;
- constraints;
- `R##` — solution-independent fitness conditions.

Each requirement must pass:

1. traceability to evidence;
2. implementation independence;
3. solution plurality;
4. causal relevance;
5. correct evidence altitude;
6. information gain when a mechanism is introduced.

Freeze requirements before evaluating concepts.

Generate enough materially different mechanisms to test whether the requirements are genuinely solution-independent. Do not invent weak alternatives to satisfy a quota. If only one credible mechanism emerges, say so and re-examine whether the requirements are overly mechanism-specific.

## Decision output

Return to the decision named at the start.

State:

- what the evidence supports;
- what it does not support;
- consequential unknowns;
- disconfirming evidence;
- discoverability/coverage caveat;
- next highest-information evidence;
- priority human review.

For STANDARD/FULL, classify the specific decision as:

- `ACT`
- `TEST`
- `HOLD`
- `REJECT`

For SCOUT, prefer:

- `STOP`
- `INVESTIGATE`
- `ESCALATE`

## Verification dimensions

Do not collapse trust into a single tier.

Track:

### Human review

- `REVIEWED`
- `NOT_REVIEWED`

### Deterministic validation

- `PASSED`
- `FAILED`
- `NOT_RUN`

### Interpretive status

- `STABLE`
- `PROVISIONAL`

A same-model review can be logged as `MODEL_CHECK_COMPLETED`; it is not independent verification.

## Identity and privacy

Internal provenance may retain public identities when needed.

Outward-facing Decision Briefs should default to aggregated or anonymized descriptions unless a person's identity is materially relevant and there is a legitimate reason to name them.

Do not imply consent, endorsement, or commercial participation from a public artifact.

Avoid unnecessary personal details.

## Proportional delivery

### SCOUT

A compact Decision Brief may be sufficient.

### STANDARD

Canonical Markdown + structured state are the default. PDF/HTML are optional.

### FULL

When supported, produce synchronized:

- canonical Markdown;
- polished PDF;
- interactive HTML evidence explorer.

The Markdown research record is canonical. PDF and HTML are derived views and must not introduce new substantive claims.

## Capability honesty

Never claim a search, source inspection, computation, file generation, browser validation, PDF rendering, or HTML interaction test was performed when the environment cannot perform it.

Do the strongest valid subset and label limitations.

## Final standard

The research should let a human distinguish:

- what changed;
- which evidence supports the trend;
- which bounded LU episodes qualify and why;
- what is observed versus inferred;
- what users actually did;
- what remains unknown;
- what is independent versus derivative;
- what the public-search process likely missed;
- what underlying needs and solution principles are supported;
- whether concept generation is justified;
- what any adequate solution must accomplish;
- what decision is justified now;
- what evidence should be gathered next.

When narrative elegance conflicts with evidence, preserve the evidence.

## Methodological references

Primary von Hippel references:

- Eric von Hippel, “Lead Users: A Source of Novel Product Concepts” (1986): https://web.mit.edu/people/evhippel/papers/Lead%20Users%20Paper%20-1986.pdf
- Lead User Project Handbook: https://web.mit.edu/evhippel/www/Lead%20User%20Project%20Handbook%20%28Full%20Version%29.pdf
- 3M lead-user application: https://web.mit.edu/people/evhippel/papers/HBR%2099%20LU%20pub%20version%203M.pdf
- Pyramiding research: https://web.mit.edu/evhippel/www-old/papers/Pyramiding%20WP%20Oct%2008.pdf

Secondary Christensen reference:

- Christensen Institute, Jobs to Be Done: https://www.christenseninstitute.org/theory/jobs-to-be-done/

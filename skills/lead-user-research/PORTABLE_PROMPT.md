# Portable Lead User Research Prompt

Copy this prompt into a capable AI chat when you cannot install or reference the full repository.

---

You are conducting **AI-assisted Lead User research using Eric von Hippel's Lead User Method as the governing methodology**.

Use Clayton Christensen's Jobs to Be Done only after evidence collection to clarify circumstance, struggle, and desired progress.

Use Fit Check only after a need is sufficiently supported. Fit Check is a project-specific concept-shaping method, not part of von Hippel's or Christensen's methodology.

## INPUT

Domain:
[INSERT DOMAIN / PROBLEM SPACE]

Decision:
[INSERT THE HUMAN DECISION THIS RESEARCH SHOULD INFORM]

Mode:
SCOUT | STANDARD | FULL

If Mode is omitted, use STANDARD.

Optional:
- target market:
- starting hypotheses:
- desired innovation altitude:
- seed sources/experts:
- source/language/geography constraints:

## PURPOSE

Do not try to validate a predetermined product.

Discover:

1. important trends changing the domain;
2. users meaningfully ahead of those trends;
3. bounded Lead User Need Episodes where users expect unusually high benefit from solving emerging needs;
4. what those users actually tried, changed, rejected, modified, or invented;
5. what advanced analog markets reveal;
6. which underlying needs and transferable principles the evidence supports;
7. what the research process may have systematically missed;
8. what humans can responsibly decide or test next.

## NON-NEGOTIABLES

- Trend before Lead User.
- A qualified Lead User episode requires evidence for both:
  - LU1: ahead of an important trend;
  - LU2: unusually high expected benefit from solving the associated need.
- Fame, expertise, early adoption, heavy use, or invention alone do not establish Lead User status.
- Behavior generally outweighs stated preference.
- A workaround is not automatically the underlying need.
- UNKNOWN stays UNKNOWN.
- PARTIAL source access stays PARTIAL.
- Derivative evidence is not independent evidence.
- Frequency is not importance.
- Computation is not interpretation.
- Discovery precedes synthesis.
- Requirements precede concepts.
- Contradictions and outliers remain visible.
- Insufficient evidence is a valid result.
- Public-search coverage is not population coverage.
- Do not claim a tool/search/file/validation action you did not actually perform.

## PRIMARY UNIT

Use a bounded **Lead User Need Episode (LU##)**:

> one user + one relevant trend + one emerging need + evidence of unusually high expected benefit.

A person may contribute zero, one, or several LU episodes.

## EXECUTION MODE

### SCOUT

Use for:

> Is this worth more investigation?

Run:
A Frame → B Discover → bounded C Evidence → G Decide

Stop when there is enough evidence to recommend:

STOP | INVESTIGATE | ESCALATE

Do not generate concepts, PDF, or an evidence explorer by default.

### STANDARD

Run:
A → B → C → D Freeze → E Interpret → G Decide

Run F Shape only if a need passes the Concept Generation Gate.

### FULL

Run the complete protocol:
A → B → C → D → E → F when warranted → G → H Deliver

Use broader pyramiding, advanced analogs, lineage analysis, and durable outputs.

Do not use FULL merely because it exists.

## STATE MECHANICS

If you have file tools:

- create persistent structured files;
- reopen them at the beginning of every phase;
- treat files, not conversational memory, as authoritative;
- write structured state before narrative synthesis;
- run deterministic structural validation where possible.

If you do **not** have file tools:

- execute one phase at a time;
- end every phase with a complete **STATE PACKET** containing all authoritative state changed in that phase;
- use the latest STATE PACKET as authoritative input to the next phase;
- do not claim durable persistence or deterministic validation.

Recommended state families:

SRC## sources  
T## trends  
E### atomic evidence  
LU## Lead User Need Episodes  
F## findings  
N## emerging needs  
SP## solution principles  
R## Fit Check requirements  
M## mechanisms

Do not create families the selected mode does not need.

## PHASE A — FRAME

Define:

- exact decision;
- scope;
- target market;
- desired innovation altitude;
- starting assumptions;
- consequential unknowns;
- evidence that would disconfirm the starting hypothesis;
- what this method will not establish;
- likely discoverability bias.

Do not begin broad Lead User search yet.

## PHASE B — DISCOVER

First establish important trends.

For each trend identify:

- what is changing;
- direction;
- evidence;
- why it matters;
- observable indicators of advancement.

Then search for:

- domain experts;
- referral nodes;
- advanced users;
- user innovators;
- Lead User candidates.

Use **pyramiding**, not simple snowballing:

> Who knows more? Who is further ahead? Who faces the more extreme need? Who originated this practice? Who should be contacted next?

Search **advanced analogs**:

> Where does the same underlying functional problem occur under more extreme conditions?

## PHASE C — EVIDENCE

Work in bounded batches.

Register source coverage:

FULL | PARTIAL | UNREADABLE | UNKNOWN

Create atomic evidence items E###.

Prefer:

1. direct behavior/artifacts;
2. first-person explanation;
3. independent observation;
4. feature requests/opinions.

Qualify LU## only with evidence for both LU1 and LU2.

Keep separate:

prior baseline → desired progress → observed result

Mark missing elements UNKNOWN.

Map forks, adaptations, dependencies, and common lineage before counting independent support.

Update coverage bias continuously.

Pyramiding may validly conclude:

> This person/category should be contacted next.

Search is not a substitute for fieldwork.

## PHASE D — EVIDENCE FREEZE

STANDARD/FULL only.

Before interpretation, audit:

- source coverage;
- evidence references;
- LU1/LU2 qualification;
- independence/lineage;
- contradictions;
- UNKNOWNs;
- discoverability gaps.

Track separately:

Human review:
REVIEWED | NOT_REVIEWED

Deterministic validation:
PASSED | FAILED | NOT_RUN

Interpretive status:
STABLE | PROVISIONAL

A same-model checklist is not independent verification.

Only proceed to interpretive synthesis when the evidence is coherent enough, or clearly label downstream work PROVISIONAL.

## PHASE E — INTERPRET

Only after the evidence pass/freeze:

Separate:

observed situation → emerging need → user mechanism → transferable principle

Use Christensen sparingly to clarify:

circumstance → struggle → desired progress → compensating behavior

Do not turn this into a JTBD study.

Synthesize across LU episodes.

Do not force a neat number of clusters.

Valid outcomes include:

- one cluster;
- several clusters;
- outliers;
- provisional groups;
- no useful clustering.

Actively search for contradictions.

Assess propagation as:

- Strong propagation evidence
- Plausible propagation
- Lead-user-specific

Do not infer prevalence.

## PHASE F — SHAPE

Optional.

A need passes the **Concept Generation Gate** only if:

1. the trend is credible;
2. at least one qualified LU episode supports it;
3. the need is separable from the workaround;
4. evidence is sufficient to derive meaningful fitness conditions;
5. no unresolved contradiction makes concept work premature.

Otherwise stop with:

> No opportunity is currently supported strongly enough for concept generation.

For a passing need define:

x = current state  
y = desired state  
gap  
constraints  
R## = what any adequate solution must accomplish

Each R must be:

- traceable to evidence;
- implementation-independent;
- causally relevant;
- at the need rather than workaround altitude.

Freeze R before evaluating mechanisms.

Generate enough materially different mechanisms to test whether R is genuinely solution-independent.

There is **no concept quota**.

Do not invent weak alternatives for symmetry.

## PHASE G — DECIDE

Return to the original decision.

Provide:

- what the evidence supports;
- strongest evidence;
- what the evidence does not support;
- what could make the interpretation wrong;
- consequential unknowns;
- recommended next evidence;
- decision status.

SCOUT:
STOP | INVESTIGATE | ESCALATE

STANDARD/FULL:
ACT | TEST | HOLD | REJECT

Always include a **Discovery Coverage** section for STANDARD/FULL:

Likely overrepresented:
[public/English/open-source/etc.]

Likely underrepresented:
[private/non-English/offline/trade/proprietary/etc.]

Corrective discovery:
[interviews/referrals/communities/fieldwork/languages/etc.]

## IDENTITY / PRIVACY

Internal evidence may retain public identities when needed for provenance.

In outward-facing Decision Briefs:

- default to aggregation or anonymization of individuals;
- name someone only when identity materially matters and there is a legitimate reason;
- do not imply consent, endorsement, or commercial participation;
- avoid unnecessary personal details.

## PHASE H — DELIVER

Only when proportionate and actually supported by the environment.

Markdown is canonical.

PDF and interactive HTML are derived views and must not introduce claims absent from Markdown.

SCOUT normally ends with a compact Decision Brief.

STANDARD defaults to Markdown + structured state.

FULL may produce Markdown + PDF + interactive HTML.

## FINAL STANDARD

Do not produce the most convincing story.

Produce the most decision-useful account of what the evidence actually supports.

When evidence conflicts with narrative elegance, preserve the evidence.

When the research process cannot see a population, say so.

When the evidence does not justify concepts, stop before concepts.

---

Start with **Phase A only** unless the selected mode and available tools make automatic phase progression safe.

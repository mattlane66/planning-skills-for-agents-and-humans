# Behavior tracing and verification

Load this reference when a breadboard maps a nontrivial existing code path, spans places or systems, contains meaningful branches, has an unexplained behavior, or needs final selected-design verification.

## Contents

- [Start from scenarios](#start-from-scenarios)
- [Build a causal trace](#build-a-causal-trace)
- [Choose useful affordances and seams](#choose-useful-affordances-and-seams)
- [Cover state and branches](#cover-state-and-branches)
- [Verify graph integrity](#verify-graph-integrity)
- [Ground current-state claims](#ground-current-state-claims)
- [Repair common failures](#repair-common-failures)
- [Completion criteria](#completion-criteria)

## Start from scenarios

Name the behavior to explain before tracing implementation structure. Use the perspective of the person, operator, caller, scheduled trigger, or incoming event trying to produce an effect.

Choose the smallest set of scenarios that exposes the behavior:

- the main success path
- each alternative that changes the observable result
- failure and recovery when they change what happens next
- persistence and restoration when later behavior depends on stored state

Do not enumerate every theoretical edge case. Include a scenario when omitting it would hide a product decision, meaningful state transition, or external consequence.

## Build a causal trace

Trace each scenario in this order:

1. **Entry** — the UI action, API call, command, event, job, or restored state that starts the behavior.
2. **Control path** — the affordances that coordinate what happens.
3. **Decision or branch** — the rule that selects a materially different path.
4. **State or data effect** — the store read/write, transformation, navigation, or side effect that changes the result.
5. **Observable consequence** — what the user, operator, caller, or external system can observe.

Record the trace with table IDs:

| Scenario | Entry | Control path | Decision / branch | State / data effect | Observable consequence | Evidence or status |
|---|---|---|---|---|---|---|
| Add unique item | U1 | U1 → N1 → N2 | not duplicate | N2 → S1 | S1 → U3 updated list | `src/items.ts:addItem` |
| Add duplicate | U1 | U1 → N1 → N2 | duplicate | no write | N2 → U4 warning | supported |

Keep traces compact. The tables define each element; the trace explains their causal order.

If a link cannot be supported:

- mark it `gap` or `unresolved`
- identify the evidence needed
- do not bridge it with a generic service or assumed mechanism

## Choose useful affordances and seams

Include a non-UI affordance when it:

- crosses a meaningful boundary
- makes a product-relevant decision
- changes state that affects later behavior
- produces an external side effect
- transforms data visible downstream
- coordinates steps whose order matters

Omit a function, wrapper, adapter, or service when it only forwards, renames, or exposes plumbing without changing the causal story.

Use a chunk when a subsystem has one clear entry and output but its internals would obscure the behavior being judged. Expand the chunk separately only when an internal branch or state effect matters.

For current-state maps, use product-facing wording for legibility but retain the actual symbol, route, test, log, or observation as evidence. Do not replace discovered architecture with invented generic layers.

## Cover state and branches

Model a branch when it leads to a different observable consequence or changes later behavior.

For each meaningful branch, identify:

- the deciding affordance or condition
- the path taken
- any state read or written
- the observable consequence

Treat these states as first-class when relevant:

- empty and populated
- loading or in progress
- success and failure
- retry, cancellation, or recovery
- enabled and disabled modes
- persisted and restored

Do not force every breadboard to contain all of them. Ask whether each can occur in scope and whether it changes the next available action or result.

## Verify graph integrity

Run these checks against the canonical tables and behavior traces:

1. **Reference integrity** — every ID named by `Wires Out`, `Returns To`, a trace, branch, contract candidate, or slice exists.
2. **Source integrity** — every displayed or returned value has an incoming source.
3. **Consequence integrity** — every in-scope entry reaches an observable consequence or an explicit unresolved gap.
4. **Branch integrity** — every meaningful branch has a modeled consequence; no rejection, failure, or alternative path disappears between rows.
5. **Store integrity** — each behaviorally relevant store has the writers and readers needed to explain its effect.
6. **Mechanism integrity** — every selected mechanism and explicit cut is represented or called out as a conflict.
7. **Rendering integrity** — every Mermaid node and relationship is represented in the tables; the diagram contains no extra behavior.
8. **Authority integrity** — current, candidate, and selected claims remain labeled according to the declared mode.

An isolated `N` row, dangling wire, source-less display, branch without a consequence, or diagram-only edge is a defect.

## Ground current-state claims

For non-obvious current-state behavior, cite the strongest available evidence:

1. executable tests or observed runtime behavior
2. concrete code paths and symbols
3. logs, traces, or persisted data
4. screenshots or operator observation
5. documentation, labeled when it may be stale

Separate:

- **observed** — directly demonstrated
- **supported** — explained by strong source evidence
- **inferred** — likely but not demonstrated
- **unresolved** — the causal link is missing

Do not present an inference as an observed fact.

## Repair common failures

| Failure | Repair |
|---|---|
| service-call graph | restart from an entry and observable consequence; retain only decision, state, boundary, transformation, and side-effect seams |
| UI inventory without behavior | add control flow, data sources, and behavior traces |
| dangling wire | add the missing target or remove the unsupported wire |
| source-less display | identify the store, return, or input that supplies the value |
| hidden rejection or failure path | add the decision and its observable consequence |
| store with no behavioral role | add its relevant writer and reader or omit it |
| invented current-state abstraction | replace it with actual code/domain language and evidence |
| diagram disagrees with tables | correct the tables first, then regenerate the rendering |

## Completion criteria

The breadboard is structurally complete for its declared scope when:

- every representative scenario has an entry and observable consequence
- the causal link between them is expressed with valid IDs
- meaningful decisions, state effects, and branches are visible
- every unresolved link is explicit
- current-state claims have evidence at the right confidence level
- selected mechanisms are represented without low-value call-graph detail
- optional diagrams are faithful renderings of the tables

Mode-specific authority and promotion gates still apply. Structural completeness does not make a candidate selected or a current-state map normative.

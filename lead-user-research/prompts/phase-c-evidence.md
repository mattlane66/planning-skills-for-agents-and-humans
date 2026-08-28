# Phase C — Evidence

At the start, reopen all authoritative discovery state.

Work in bounded batches. Do not attempt to hold the whole evidence corpus in conversational memory.

A useful default is 5–10 promising cases per batch.

## Source registration

For every meaningful source create `SRC##` and assign:

- FULL;
- PARTIAL;
- UNREADABLE;
- UNKNOWN.

Never overstate coverage.

## Atomic evidence

Create `E###` records for bounded observations.

Prefer:

1. actual artifacts and behavior;
2. first-person explanations;
3. independent observation;
4. stated wishes.

Keep evidence atomic and source-located.

## Lead User Need Episodes

Create or update `LU##`.

A QUALIFIED episode requires valid evidence for both:

- LU1 — ahead of an important trend;
- LU2 — unusually high expected benefit.

For every QUALIFIED episode also record:

- LU1 rationale — why the evidence establishes advancement;
- advancement indicator — the observable indicator placing the episode ahead;
- LU2 rationale — why the evidence establishes unusually high expected benefit;
- benefit signal — the concrete signal of that expected benefit;
- qualification caveats — unresolved weaknesses or alternate explanations.

The same evidence may support both LU1 and LU2 only when the separate rationales show why. Do not infer qualification from fame, expertise, early adoption, or invention alone.

Keep separate:

- prior baseline;
- desired progress;
- observed result.

Use UNKNOWN whenever the source does not establish an element.

## Episode tracing

For LU episodes likely to materially support later need interpretation or concept shaping, trace the episode as far as the evidence permits.

Record:

- initiating condition;
- prior approach and relevant history;
- switch/change trigger when present;
- expected improvement;
- the sequence of actions through the actual outcome, including activity outside the focal product or workflow;
- fit points such as hesitation, repetition, confusion, failure, abandonment, non-action, or compensating behavior;
- what the user explicitly said they were trying to preserve, avoid, or accomplish;
- actual outcome;
- unresolved elements as UNKNOWN.

For consequential fit points, keep separate:

- OBSERVED behavior;
- STATED purpose;
- INFERRED purpose;
- UNKNOWN elements.

Use trace status:

NOT_ASSESSED | PARTIAL | SUFFICIENT

`SUFFICIENT` means sufficient for the intended downstream interpretation, not complete knowledge of the episode.

Tracing is not a third Lead User qualification criterion. Do not infer LU status from trace completeness.

Do not turn the workaround into the need, rank fit points, or generate producer solutions in Phase C.

## Lineage

Map derivative relationships before treating examples as independent evidence.

## Coverage

Update discoverability bias continuously.

If pyramiding reaches a person/category who likely requires direct contact, record that referral rather than pretending search has exhausted the pyramid.

## Write state

Update:

- `sources.json`;
- `evidence.json`;
- `lu_episodes.json`;
- `lineage.json`;
- `coverage.json`;
- `search_log.json`;
- `change_log.json`.

Run deterministic validation after each batch when possible.

Structural validation is not substantive proof.

## SCOUT stop

For SCOUT, stop evidence collection when the bounded pass is enough to answer:

> Is this worth more investigation?

Do not run the full evidence machinery merely because it exists.

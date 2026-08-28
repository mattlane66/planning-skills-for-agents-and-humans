# Study State Contract

The study state is deliberately plain JSON so any tool-using AI can read and write it.

The files, not chat memory, are authoritative when file tools are available.

## Core files

### `manifest.json`

Tracks:

- protocol version;
- mode;
- current phase;
- human review;
- deterministic validation;
- interpretive status;
- model-check status;
- timestamps.

### `decision.json`

Tracks:

- domain / problem space;
- target market;
- what the research should understand;
- human decision the research should inform;
- innovation altitude;
- starting hypotheses;
- scope;
- assumptions;
- consequential unknowns;
- disconfirming evidence;
- out-of-scope questions.

The learning objective (`what_to_understand`) and decision are separate fields and must not be silently merged.

### `trends.json`

Array of:

- `trend_id` — `T##`;
- statement;
- direction;
- evidence refs;
- observable indicators;
- importance;
- status.

### `candidates.json`

Experts, referral nodes, Lead User candidates, or user innovators discovered before qualification.

### `sources.json`

Array of:

- `source_id` — `SRC##`;
- title;
- creator;
- URL or immutable identifier;
- source type;
- coverage — `FULL | PARTIAL | UNREADABLE | UNKNOWN`;
- coverage note;
- access date.

### `evidence.json`

Array of atomic evidence:

- `evidence_id` — `E###`;
- `source_id`;
- exact location when available;
- evidence type;
- verbatim excerpt or bounded observation;
- user/entity;
- `trend_id` when known;
- `lu_id` when known;
- caveat.

### `lu_episodes.json`

Array of bounded Lead User Need Episodes:

- `lu_id` — `LU##`;
- user/entity;
- `trend_id`;
- need statement;
- context;
- status — `CANDIDATE | QUALIFIED | REJECTED`;
- `lu1_evidence`;
- `lu2_evidence`;
- baseline;
- alternatives;
- user response;
- desired progress;
- observed result;
- unknowns.

A QUALIFIED episode must contain valid evidence references for both LU1 and LU2.

### `lineage.json`

Records same creator, fork, dependency, adaptation, copied technique, common upstream project, shared organization/community, and independent rediscovery.

### `coverage.json`

Tracks discovery bias:

- likely overrepresented populations;
- likely underrepresented populations;
- inaccessible/private areas;
- languages/regions searched;
- corrective discovery actions;
- interview/fieldwork referrals.

### `search_log.json`

Major search families, pyramiding hops, analog pivots, and abandoned branches.

Do not record every trivial query.

### `change_log.json`

Material analytical changes:

- merges;
- splits;
- renames;
- recoding;
- requalification;
- lineage corrections;
- cluster changes;
- requirement changes;
- decision changes.

### `freeze.json`

For STANDARD/FULL:

- status — `OPEN | FROZEN`;
- freeze timestamp;
- evidence counts;
- qualified episode count;
- independent lineage count;
- unresolved gaps;
- post-freeze evidence log.

### `findings.json`

Array of:

- `finding_id` — `F##`;
- claim;
- epistemic label — `VERIFIED | INFERRED | SPECULATIVE | UNKNOWN`;
- evidence refs;
- LU refs;
- contradictions;
- confidence rationale.

A VERIFIED finding requires at least one valid evidence reference.

### `needs.json`

Array of:

- `need_id` — `N##`;
- statement;
- supporting finding IDs;
- relevant trends;
- propagation status;
- contradictions;
- concept gate status — `PASS | FAIL | NOT_ASSESSED`;
- concept gate rationale.

### `principles.json`

Transferable solution principles, expressed without prescribing one implementation.

### `fit_criteria.json`

Array of:

- `requirement_id` — `R##`;
- `need_id`;
- requirement;
- evidence refs;
- traceability;
- implementation independence;
- causal relevance;
- altitude check;
- status.

### `concepts.json`

Array of:

- `concept_id` — `M##`;
- `need_id`;
- mechanism;
- requirement IDs;
- assumptions;
- risks;
- evidence needed next.

No minimum concept count is required.

## Authority

When records disagree:

1. latest explicit human decision;
2. persisted reviewed/validated state;
3. current structured state;
4. narrative summaries;
5. conversational memory.

Never silently rewrite reviewed human decisions.

# Optional high-volume discovery screening (Jev)

Use only when a bounded corpus is too large to inspect directly. The ordinary
Phase B method works without Jev, API credentials, or an external provider.
This adapter is experimental; it prioritizes what to inspect, not what is true.

## Retrieve first

Consider X (formerly Twitter), Reddit, GitHub issues/discussions, Hacker News,
YouTube demonstrations and specialist forums when relevant. Use only authorized
tools and public or permissioned material. Follow original posts, replies,
conversation context, originators and referrals where accessible. Record
platform, query, date, limits, original provenance and inaccessible material in
the existing Q## search log. X and other platform access are independent of Jev;
do not claim a platform was searched when it was unavailable. Include independent
non-platform and fieldwork routes.

Prepare a local JSON corpus in retrieval order, with only excerpts that a human
has approved for external processing. Context is a minimized research question
and, where relevant, a rival hypothesis and functional relationship. Example
(illustrative, not evidence):

```json
{"context":"How do bicycle commuters cope with repeated transport constraints?",
 "items":[{"source_ref":"local-post-1","original_ref":"local-post-1","platform":"X",
 "excerpt":"I built a detachable rack after repeated storage failures.",
 "permission":"REDACTED_APPROVED"}]}
```

Source references and platform remain local. Only the minimized question and
excerpt are sent, plus fixed screening questions. Public availability alone
does not confer permission to send content to a third party. Remove sensitive,
private, regulated and identifying details, including indirect identifiers, and
review vendor retention and processing terms. Never send a complete transcript,
credentials or unreviewed private research material. The approval digest binds
the exact payload and corpus but cannot prove consent or reviewer identity.

## Run

The standard-library Python adapter uses TypeSafe's documented
[System One endpoint](https://docs.typesafe.ai/introduction/quickstart) and
[Noul primitive](https://docs.typesafe.ai/primitives/noul). No SDK installation.
Pin an exact supported model; default jev-1.14.0 is a documented example, not
a recommendation of empirically superior accuracy. Set a finite call cap and
inspection budget. First preview, with no external requests:

```bash
python lead-user-research/scripts/screen_discovery.py corpus.json \
  --max-calls 100 --budget 20 --audit-count 5 --seed 41
```

Inspect the corpus and questions in the script. Have a human approve the exact
preview digest and processing; set TYPESAFE_API_KEY in the local environment.
Repeat the same command with `--approve-digest <digest> --output triage.json`.
Never paste keys into prompts or commit them. No automatic retries; an error
halts further transmission, retaining failed and unscored rows. Cap calls rather
than claiming a guaranteed dollar cost; usage returned by the provider is
recorded per successful item. Do not equate transport success with accuracy.

## Inspect without discarding rare cases

Independent Noul questions cover relevance, unusual constraints, workarounds,
early exposure, investment, contradictions, functional analogs and referral
signals. They are model scores, not calibrated research confidence or LU scores.
Do not filter on a relevance threshold. The queue reserves seeded low-rank
inspections (including unscored cases where available), then rotates across
signal lanes, groups known derivatives by original, and preserves every result
in the report. With small budgets, some lanes cannot be visited; rotate the
investigation across batches or use ordinary search. Keep an independent rare
case search; no queue can recover material never retrieved. Inspect original
context before registering evidence. A failed or low score is not a negative
finding. Do not use this adapter for automated qualification, source entailment,
transferability, prevalence, market size, or concept selection.

Record screening configuration, actual coverage, sampling, limitations, and
yield in the existing search log; store the separate output as a local discovery
artifact, not evidence or a freeze input. Existing LU1/LU2, lineage, verification,
sufficiency, and human decisions remain unchanged.

## Evaluate before adoption

Predeclare corpus, independent original-level labels, budget, audit count, seed,
model and metrics. The optional `--labels labels.json` compares retrieval rank,
Jev relevance-only and diverse Jev queues under the same inspection budget.
Labels are Boolean indicators of independently adjudicated informative episodes,
not model judgments. Keep labels out of the request. Report bounded recall only
for a fully adjudicated corpus, precision only for adjudicated selected items,
and unknowns otherwise. This small offline comparison does not establish
method-level effectiveness. For the prospective A/B/C comparison of complete
search workflows, match access, cost and researcher time, blind the judges,
measure rare-episode recall, false exclusions, novel supported needs, effort,
and downstream outcomes. Record failures and costs. Do not enable by default
until evidence warrants it.

For direct X retrieval, use the [bounded official API adapter](x-discovery.md) or authorized host search. No X data is automatically transferred to Jev; separately verify processing rights and approve the minimized corpus.

For semantic X discovery, the optional [Grok native X Search adapter](grok-x-discovery.md) complements direct query retrieval. It uses a separate xAI key and explicit approved spend exposure; only structured post citations become inspection leads. No automatic external screening.

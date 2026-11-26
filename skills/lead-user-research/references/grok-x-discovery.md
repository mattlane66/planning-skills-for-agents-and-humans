# Grok native X Search (optional)

Use this route for semantic discovery, unfamiliar vocabulary and conversations on X.
The [direct X API](x-discovery.md) is preferable for repeatable lexical queries,
bounded post reads and historical coverage. Grok chooses its own queries and tool
calls; it does not provide an exhaustive, reproducible corpus. Use both when the
information value warrants it, and compare independent branches.

Verified against official documentation on 2026-11-26:
[X Search](https://docs.x.ai/developers/tools/x-search),
[citations](https://docs.x.ai/developers/tools/citations),
[usage](https://docs.x.ai/developers/cost-tracking),
[privacy/storage](https://docs.x.ai/developers/model-capabilities/text/generate-text),
[billing](https://docs.x.ai/console/billing).
The adapter uses the Responses API and its native x_search tool. No SDK or X
developer bearer token is needed for this route, but an approved xAI API account
and XAI_API_KEY are required. Review terms, authorized use and processing rights.

## Configure and run

Create a dedicated inference key in https://console.x.ai/ and configure a small
team spending limit. Inject XAI_API_KEY through the local secret environment;
never store it in a repository, prompt, or search configuration. Model
grok-4.7 is the documented example, not a claim of superior research performance.
Only send minimized public search questions, not private interviews, internal
strategy or identifying/sensitive research material. Preview and have a human
approve the exact requests, scope and spend exposure.

Example (illustrative dates, end exclusive):

```json
{
  "model": "grok-4.7",
  "from_date": "2026-11-01",
  "to_date": "2026-11-26",
  "max_requests": 3,
  "max_turns": 2,
  "max_output_tokens": 1500,
  "stop_after_usd": "1.00",
  "queries": [
    {"id":"Q1","lane":"rare","query":"Find concrete unusual constraints in bicycle commuting, including extreme cases."},
    {"id":"Q2","lane":"workaround","query":"Find first-hand reports of homemade modifications to carry or store bicycles."},
    {"id":"Q3","lane":"contradiction","query":"Find reports of abandoned or failed bicycle transport workarounds."}
  ]
}
```

```bash
python lead-user-research/scripts/search_grok_x.py grok-plan.json
python lead-user-research/scripts/search_grok_x.py grok-plan.json \
  --approve-digest APPROVED_DIGEST --output grok-x-discovery.json
```

The first command never makes a network request. The second runs one native
Responses request per approved lane, with a bounded max_turns and
max_output_tokens, store:false, images/videos disabled and no other tools.
The provider may fetch multiple posts within each turn. The date window filters
keyword and semantic searches, but not thread fetches. Treat all returned scope
as unverified; inspect dates and thread context before using any material.

## Cost and limits

Published pricing at verification: $5 per 1,000 fetched posts and $10 per 1,000
profiles, plus model token charges. Duplicate fetches count. The adapter requests
post search rather than profiles; it cannot prohibit the provider from invoking
user search internally and stops subsequent requests if it reports profiles.
Record native usage counts and the provider's cost_in_usd_ticks (USD times
10^10). The stop_after_usd threshold stops subsequent requests only after
a response; one request can exceed it. It is not a guaranteed spend cap or a
limit on individual posts. Enforce billing limits in the provider console.
Unknown cost/usage, failed/incomplete responses or no native search stop further
requests. Do not auto-retry or silently switch providers and incur new costs.

## Evidence boundary

The adapter retains only normalized X post IDs from structured citation
annotations, query IDs, native usage and run metadata. Generated prose, raw
posts, usernames, profile data and arbitrary links are not persisted; unannotated
links are not accepted as results. Require reported native search and fetched
posts. Citations are discovery leads, not proof that a particular claim is
supported, and may represent only a subset of retrieved items. No raw search
result feed is exposed by this API. A cited post may be inaccessible, outside the
date range, or irrelevant. Reopen it and check context, provenance, independent
support and LU1/LU2 under the existing method. No claim of representative
coverage, qualification, or prevalence. Record actual route and limitations
in existing Q search logs. Keep output local; comply with retention and deletion
obligations. No automatic transfer to Jev: use a separate approved, minimized
corpus only when provider and source processing rights permit it.

Without credentials or permitted access, continue using authorized direct X
API or host web search. The core Lead User method remains independent of Grok.

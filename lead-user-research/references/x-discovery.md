# X discovery: official API or authorized host search

Use X when it is relevant to the research domain. Search episodes and practices,
not personal profiles or popularity. X is one discovery branch; it is not the
population. Continue independent branches, including interviews, specialized
communities and advanced analogs.

## Choose the retrieval route

1. If an approved X developer application and app-only bearer token are
   available, use the read-only adapter below. Recent search covers the last
   seven days; full archive is an explicitly selected mode subject to account
   access and billing. Use recent for emerging signals, archive for tracing
   early practices, changes over time and innovation origins.
2. Otherwise use authorized native or host search (including domain-limited web
   queries on x.com and twitter.com) if available. Inspect the live original;
   snippets alone are partial discovery. Record which route actually ran.
3. If access fails or a source is restricted, record the limitation and continue
   other branches. Do not circumvent access controls, scrape behind authentication,
   infer personal attributes, or claim a full archive was searched.

Verified documentation (2026-11-26): [search overview](https://docs.x.com/x-api/posts/search/introduction),
[recent endpoint](https://docs.x.com/x-api/posts/search-recent-posts),
[archive endpoint](https://docs.x.com/x-api/posts/search-all-posts),
[query operators](https://docs.x.com/x-api/posts/search/integrate/build-a-query),
[pricing](https://docs.x.com/x-api/getting-started/pricing),
[developer policy](https://docs.x.com/developer-terms/policy).
Review current policies, approved use, processing rights and pricing before use.
The CLI is a prototype, not an assertion of X approval for a particular use case.

## Plan a bounded search

Use explicit date windows and distinct search lanes. The example is illustrative;
replace the dates and terms with the actual authorized research scope.

```json
{
  "mode": "recent",
  "start_time": "2026-11-23T00:00:00Z",
  "end_time": "2026-11-25T00:00:00Z",
  "page_size": 25,
  "max_requests": 8,
  "max_posts": 200,
  "queries": [
    {"id":"Q1","lane":"need","query":"(\"bike commute\" OR \"bicycle commuting\") (\"can't\" OR \"problem\") -is:retweet","sort_order":"recency"},
    {"id":"Q2","lane":"workaround","query":"(\"bike commute\" OR \"bicycle commuting\") (\"built\" OR \"modified\") -is:retweet","sort_order":"relevancy"},
    {"id":"Q3","lane":"contradiction","query":"(\"bike commute\" OR \"bicycle commuting\") (\"gave up\" OR \"didn't work\") -is:retweet","sort_order":"recency"}
  ]
}
```

Include separate rare-case, analogous-domain, and referral searches where useful.
Use independent lexical variants, languages and time slices; don't simply search
for influencers. To explore a thread, plan a separate bounded query using the
documented conversation operator, e.g. `conversation_id:123456789`, with its own
approval. Trace linked posts and originals rather than treating reposts as
independent evidence. Do not automatically follow arbitrary links or accounts.

```bash
python lead-user-research/scripts/search_x.py search-plan.json
```

Preview is offline and prints the exact configuration, read cap, illustrative
cost and approval digest. Review scope and cost, configure spending limits in
the X Developer Console, and set `X_BEARER_TOKEN` locally. Never paste a token
into a prompt, commit it, or put it in a search query. Execute only after the
human approves the exact digest:

```bash
python lead-user-research/scripts/search_x.py search-plan.json \
  --approve-digest APPROVED_DIGEST --output x-discovery.json
```

A request reserves its full possible page size before sending; requests rotate
across queries, stop at the request/read cap, and never retry automatically.
A denial, rate limit, malformed/partial response, or repeated pagination token
stops further requests and preserves already retrieved IDs. The budget counts
possible reads, not just deduplicated IDs. The current published example rate
is $0.005 per post read; 200 possible reads imply $1 at that rate, excluding
other calls. This estimate is not a billing guarantee; check the console.
No user expansion, follow graph, private content, or write endpoints are used.

## Evidence and screening boundary

Only IDs, source links, query/page provenance and search coverage persist;
no raw post text, author profiles, or engagement metrics are stored by this
adapter. Keep the output in the local research workspace, outside frozen
evidence. Reopen posts in the authorized environment for inspection, check
surrounding conversation, referenced originals, edits and availability.
Do not treat deleted, withheld, inaccessible or changed content as verified.
Honor X's content compliance and deletion obligations for all retained material,
including downstream notes; remove/update affected data as required. Never
commit raw retrieved content to the repository. This adapter does not implement
continuous compliance monitoring or rehydration of historical content.

Do not automatically send X posts to Jev or another processor. Only if the
approved X use case, license, privacy requirements and processor terms permit
that processing, prepare a minimized, reviewed corpus through the separate
[discovery screening](discovery-screening.md) procedure and exact payload
approval. Otherwise use authorized local inspection. Avoid off-platform identity
matching and sensitive profiling. Public visibility alone does not grant
redistribution or external processing rights.

Record query, time range, sort order, pages, returned/unique IDs, coverage and
stop reason in existing Q## search logs; no new evidence fields or gates.
A retrieved post is only a discovery signal until original context is inspected
and the existing LU1/LU2 evidence, lineage, contradiction and sufficiency rules
are satisfied.

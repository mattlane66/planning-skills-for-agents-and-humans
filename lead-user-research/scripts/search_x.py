#!/usr/bin/env python3
"""Read-only, budget-bounded X discovery. Store post IDs, never raw X content."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal
from pathlib import Path

BASE = "https://api.x.com/2/tweets/search/"
CONTRACT = "lur-x-search-v1"
LANES = {"need", "workaround", "rare", "contradiction", "analog", "referral", "conversation"}
ID = re.compile(r"[0-9]{1,19}")
MAX_BYTES = 8 * 1024 * 1024


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def utc(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", value):
        raise ValueError("Use UTC timestamps YYYY-MM-DDTHH:MM:SSZ")
    return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def plan(config):
    if not isinstance(config, dict) or set(config) != {
        "mode", "start_time", "end_time", "page_size", "max_requests", "max_posts", "queries"
    }:
        raise ValueError("Expected mode, start_time, end_time, page_size, max_requests, max_posts, queries")
    mode = config["mode"]
    if mode not in ("recent", "all"):
        raise ValueError("Mode must be recent or all")
    start, end = utc(config["start_time"]), utc(config["end_time"])
    if start >= end:
        raise ValueError("Start must precede end")
    if mode == "recent" and end - start > dt.timedelta(days=7):
        raise ValueError("Recent mode cannot span more than seven days")
    for k in ("page_size", "max_requests", "max_posts"):
        if type(config[k]) is not int or config[k] < 1:
            raise ValueError("Positive integer caps required")
    if not 10 <= config["page_size"] <= (100 if mode == "recent" else 500):
        raise ValueError("Page size outside endpoint limits")
    if config["max_posts"] < 10:
        raise ValueError("At least ten post reads must be authorized")
    queries = config["queries"]
    if not isinstance(queries, list) or not queries:
        raise ValueError("Supply at least one query")
    seen = set()
    for q in queries:
        if not isinstance(q, dict) or set(q) != {"id", "lane", "query", "sort_order"}:
            raise ValueError("Each query needs id, lane, query and sort_order")
        if not isinstance(q["id"], str) or not re.fullmatch(r"Q[0-9]{1,6}", q["id"]) or q["id"] in seen:
            raise ValueError("Query IDs must be unique Q numbers")
        seen.add(q["id"])
        if q["lane"] not in LANES or q["sort_order"] not in ("recency", "relevancy"):
            raise ValueError("Unknown lane or sort order")
        if not isinstance(q["query"], str) or not q["query"].strip() or len(q["query"]) > (512 if mode == "recent" else 1024):
            raise ValueError("Empty or oversized query")
        if any(ord(c) < 32 for c in q["query"]):
            raise ValueError("Control characters in query")
    upper = min(config["max_posts"], config["max_requests"] * config["page_size"])
    return {"contract": CONTRACT, "provider": "X_API", "endpoint": BASE + mode,
            "config": config, "max_requested_post_reads": upper,
            "illustrative_usd_at_2026_11_26_public_rate": str(Decimal(upper) * Decimal("0.005")),
            "price_limit": "Estimate only; verify current console rates and configure account spend limits."}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect refused", headers, fp)


def fetch_page(endpoint, params, token):
    if endpoint not in (BASE + "recent", BASE + "all"):
        raise ValueError("Unapproved endpoint")
    req = urllib.request.Request(endpoint + "?" + urllib.parse.urlencode(params),
                                 headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
                                 method="GET")
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=30) as resp:
        raw = resp.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Response too large")
    return json.loads(raw)


def parse_page(payload, size):
    if not isinstance(payload, dict) or not isinstance(payload.get("meta"), dict):
        raise ValueError("Malformed response")
    meta = payload["meta"]
    rows = payload.get("data", [])
    if not isinstance(rows, list) or len(rows) > size:
        raise ValueError("Unexpected page size")
    if type(meta.get("result_count")) is not int or meta["result_count"] != len(rows):
        raise ValueError("Result count mismatch")
    ids = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not ID.fullmatch(row["id"]):
            raise ValueError("Invalid post ID")
        # No text, usernames, profile data, engagement or raw response is persisted.
        # Withheld rows are not offered for inspection.
        if not row.get("withheld"):
            ids.append(row["id"])
    token = meta.get("next_token")
    if token is not None and (not isinstance(token, str) or not token or len(token) > 4096):
        raise ValueError("Invalid pagination token")
    return ids, len(rows), token, bool(payload.get("errors"))


def run(config, approval, send, now=None):
    manifest = plan(config)
    if approval != digest(manifest):
        raise ValueError("Approval must match exact preview")
    now = now or dt.datetime.now(dt.timezone.utc)
    if utc(config["end_time"]) > now:
        raise ValueError("End time is in the future")
    if config["mode"] == "recent" and utc(config["start_time"]) < now - dt.timedelta(days=7):
        raise ValueError("Recent window expired; revise and reapprove or use archive")
    rows = {}
    states = [{"id": q["id"], "lane": q["lane"], "status": "NOT_RUN",
               "pages": 0, "returned": 0, "token": None, "seen_tokens": set()}
              for q in config["queries"]]
    requested = calls = returned = 0
    halted = None
    # Round-robin across predeclared search lanes; one large query cannot monopolize the cap.
    while calls < config["max_requests"] and config["max_posts"] - requested >= 10:
        progressed = False
        for q, st in zip(config["queries"], states):
            if st["status"] in ("EXHAUSTED", "PARTIAL_ERROR", "ERROR"):
                continue
            size = min(config["page_size"], config["max_posts"] - requested)
            if calls >= config["max_requests"] or size < 10:
                break
            params = {"query": q["query"], "start_time": config["start_time"],
                      "end_time": config["end_time"], "sort_order": q["sort_order"],
                      "max_results": size}
            if st["token"] is not None:
                params["next_token"] = st["token"]
            # Reserve maximum possible reads before each request, including failures.
            requested += size
            calls += 1
            progressed = True
            try:
                ids, count, token, partial = parse_page(send(manifest["endpoint"], params), size)
                st["pages"] += 1
                st["returned"] += count
                returned += count
                for rank, post_id in enumerate(ids, 1):
                    row = rows.setdefault(post_id, {
                        "source_ref": "https://x.com/i/web/status/" + post_id,
                        "post_id": post_id, "platform": "X",
                        "evidentiary_role": "DISCOVERY_SIGNAL", "inspection_status": "NOT_INSPECTED",
                        "matches": []})
                    row["matches"].append({"query_id": q["id"], "page": st["pages"], "rank_among_available": rank})
                if partial or (token is not None and token in st["seen_tokens"]):
                    st["status"] = "PARTIAL_ERROR"
                    halted = "PARTIAL_RESPONSE_OR_REPEATED_TOKEN"
                    break
                if token is None:
                    st["status"] = "EXHAUSTED"
                else:
                    st["seen_tokens"].add(token)
                    st["token"] = token
                    st["status"] = "MORE_AVAILABLE"
            except urllib.error.HTTPError as exc:
                st["status"] = "ERROR"
                halted = "HTTP_" + str(exc.code)
                break
            except (OSError, ValueError, TypeError):
                st["status"] = "ERROR"
                halted = "TRANSPORT_OR_INVALID_RESPONSE"
                break
        if halted or not progressed:
            break
    for st in states:
        st.pop("token")
        st.pop("seen_tokens")
    return {**manifest, "approval_digest": approval, "retrieved_at": now.isoformat(),
            "evidentiary_role": "DISCOVERY_SIGNAL", "requests_attempted": calls,
            "max_reads_reserved": requested, "reported_post_reads": returned,
            "stop_reason": halted or ("QUERY_WINDOWS_EXHAUSTED" if all(s["status"] == "EXHAUSTED" for s in states) else "CAP_REACHED"),
            "queries": states, "results": list(rows.values()),
            "coverage_limit": "Bounded query results only. Not a complete population or evidence of need. Reopen original posts; missing or changed posts cannot support claims."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--approve-digest")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        manifest = plan(config)
        if not args.approve_digest:
            print(json.dumps({**manifest, "approval_digest": digest(manifest)}, indent=2))
            return 0
        if args.approve_digest != digest(manifest):
            raise ValueError("Approval must match exact preview")
        if not args.output or args.output.exists() or args.output.is_symlink():
            raise ValueError("Specify a new local discovery-output file")
        token = os.environ.get("X_BEARER_TOKEN")
        if not token:
            raise ValueError("X_BEARER_TOKEN unavailable; use authorized host search or record access limitation")
        # Reserve a new local file; never overwrite research registries.
        with args.output.open("x", encoding="utf-8") as out:
            result = run(config, args.approve_digest, lambda ep, p: fetch_page(ep, p, token))
            json.dump(result, out, indent=2, allow_nan=False)
            out.write("\n")
        return 2 if result["stop_reason"].startswith(("HTTP_", "TRANSPORT_", "PARTIAL_")) else 0
    except (OSError, ValueError, TypeError):
        parser.error("Invalid or unapproved search, unavailable credential, expired window, or inaccessible output; preview and check configuration")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

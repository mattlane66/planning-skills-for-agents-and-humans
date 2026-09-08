"""Check HTTP(S) URLs in tracked Markdown; no network access in ordinary PR checks.

Run manually with `python scripts/check-external-links.py --report dist/links.json`.
The scheduled workflow retains the JSON report, including unresolved and skipped
URLs. HTTP errors do not necessarily mean a link is broken: authentication,
bot protection, rate limits, and outages are reported separately. Fragments are
not validated. Requests are sequential, spaced at least one second apart, use
15-second socket timeouts, and retry transient failures at most twice.
"""
from __future__ import annotations

import argparse
import datetime
import email.utils
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r'https?://[^\s<>\[\]"`*]+')
AUTH_ONLY = {
    "https://github.com/mattlane66/planning-skills-for-agents-and-humans/security/advisories/new":
        "Private vulnerability reporting requires an authenticated GitHub session.",
}


def normalize(raw: str) -> str:
    raw = raw.rstrip(".,;:!?")
    while raw.endswith(")") and raw.count(")") > raw.count("("):
        raw = raw[:-1]
    return urllib.parse.urldefrag(raw)[0]


def skip_reason(url: str) -> str | None:
    if url in AUTH_ONLY:
        return AUTH_ONLY[url]
    host = urllib.parse.urlsplit(url).hostname or ""
    if host == "localhost" or host.endswith(".localhost"):
        return "Local development address."
    try:
        if not ipaddress.ip_address(host).is_global:
            return "Non-public example address."
    except ValueError:
        pass
    return None


def collect(root: Path = ROOT) -> dict[str, list[str]]:
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "*.md"], cwd=root
    ).decode().split("\0")
    links: dict[str, list[str]] = {}
    for name in filter(None, paths):
        for line_number, line in enumerate((root / name).read_text(encoding="utf-8").splitlines(), 1):
            for raw in URL.findall(line):
                url = normalize(raw)
                location = f"{name}:{line_number}"
                if location not in links.setdefault(url, []):
                    links[url].append(location)
    return dict(sorted(links.items()))


def retry_delay(value: str | None, attempt: int) -> float:
    if value:
        try:
            return max(0, float(value))
        except ValueError:
            try:
                date = email.utils.parsedate_to_datetime(value)
                return max(0, (date - datetime.datetime.now(datetime.timezone.utc)).total_seconds())
            except (TypeError, ValueError):
                pass
    return 2 ** attempt


class Checker:
    def __init__(self, opener=urllib.request.urlopen, sleep=time.sleep, clock=time.monotonic):
        self.opener, self.sleep, self.clock = opener, sleep, clock
        self.last_request: float | None = None

    def request(self, url: str, method: str):
        if self.last_request is not None:
            self.sleep(max(0, 1 - (self.clock() - self.last_request)))
        self.last_request = self.clock()
        request = urllib.request.Request(url, method=method, headers={
            "User-Agent": "planning-skills-documentation-link-check/1.0",
        })
        try:
            with self.opener(request, timeout=15) as response:
                return response.status, response.geturl(), response.headers.get("Retry-After"), None
        except urllib.error.HTTPError as error:
            with error:
                return error.code, error.geturl(), error.headers.get("Retry-After"), None
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            return None, url, None, str(error)

    def check(self, url: str) -> dict:
        reason = skip_reason(url)
        if reason:
            return {"url": url, "result": "skipped", "reason": reason, "attempts": 0}
        method = "HEAD"
        for attempt in range(3):
            code, target, retry_after, error = self.request(url, method)
            # Some servers reject HEAD while serving the document through GET.
            # Opening the response does not download its body (including PDFs).
            if method == "HEAD" and code in (403, 405, 501):
                method = "GET"
                code, target, retry_after, error = self.request(url, method)
            result = {"url": url, "final_url": target, "status": code,
                      "attempts": attempt + 1, "method": method}
            if code is not None and 200 <= code < 300:
                return dict(result, result="ok")
            transient = code is None or code in (408, 429) or code >= 500
            if transient and attempt < 2:
                delay = retry_delay(retry_after, attempt)
                # Do not retry earlier than requested or wait indefinitely.
                if delay > 60:
                    return dict(result, result="unverified", reason="Retry-After exceeds the 60-second retry budget.")
                self.sleep(delay)
                continue
            state = "broken" if code in (404, 410) else "unverified"
            return dict(result, result=state, reason=error or f"HTTP {code}")
        raise AssertionError("Retry loop must return")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("dist/external-links.json"))
    parser.add_argument("--list", action="store_true", help="List URL inventory without network requests")
    args = parser.parse_args()
    links = collect()
    if args.list:
        print(json.dumps(links, indent=2))
        return 0
    checker = Checker()
    results = []
    for url, locations in links.items():
        result = dict(checker.check(url), locations=locations)
        results.append(result)
        print(f"{result['result']}: {url}", flush=True)
    report = {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "fragment_validation": False, "results": results}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return int(not results or any(r["result"] in ("broken", "unverified") for r in results))


if __name__ == "__main__":
    raise SystemExit(main())

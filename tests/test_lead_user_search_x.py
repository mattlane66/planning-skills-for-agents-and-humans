import datetime as dt
import importlib.util
import pathlib
import unittest
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("search_x", ROOT / "lead-user-research/scripts/search_x.py")
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)
NOW = dt.datetime(2026, 11, 26, tzinfo=dt.timezone.utc)


def config():
    return {"mode": "recent", "start_time": "2026-11-23T00:00:00Z",
            "end_time": "2026-11-25T00:00:00Z", "page_size": 10,
            "max_requests": 3, "max_posts": 30, "queries": [
                {"id": "Q1", "lane": "rare", "query": "unusual failure", "sort_order": "recency"},
                {"id": "Q2", "lane": "contradiction", "query": "abandoned", "sort_order": "relevancy"}]}


def page(ids, token=None, errors=None):
    out = {"data": [{"id": i, "text": "PRIVATE TEXT", "author_id": "secret", "public_metrics": {}} for i in ids],
           "meta": {"result_count": len(ids)}}
    if token:
        out["meta"]["next_token"] = token
    if errors:
        out["errors"] = errors
    return out


class XTests(unittest.TestCase):
    def test_preview_binding_and_caps(self):
        c = config()
        p = x.plan(c)
        self.assertEqual(p["max_requested_post_reads"], 30)
        self.assertEqual(p["illustrative_usd_at_2026_11_26_public_rate"], "0.150")
        calls = []
        def send(ep, params):
            calls.append(params)
            return page(["1"])
        with self.assertRaises(ValueError):
            x.run(c, "wrong", send, NOW)
        self.assertEqual(calls, [])
        c["max_posts"] = 20
        with self.assertRaises(ValueError):
            x.run(c, x.digest(p), send, NOW)
        self.assertEqual(calls, [])

    def test_pagination_round_robin_and_minimized_output(self):
        c = config()
        calls = []
        pages = iter([page(["1", "2"], "n"), page(["2", "3"]), page(["4"])])
        def send(ep, params):
            self.assertEqual(ep, x.BASE + "recent")
            calls.append(params)
            return next(pages)
        out = x.run(c, x.digest(x.plan(c)), send, NOW)
        self.assertEqual([p["query"] for p in calls], ["unusual failure", "abandoned", "unusual failure"])
        self.assertEqual(calls[2]["next_token"], "n")
        self.assertEqual(out["max_reads_reserved"], 30)
        self.assertEqual(out["reported_post_reads"], 5)
        self.assertEqual(len(out["results"]), 4)
        self.assertEqual(len(out["results"][1]["matches"]), 2)
        self.assertNotIn("PRIVATE TEXT", str(out))
        self.assertNotIn("author_id", str(out))
        self.assertEqual(out["results"][0]["inspection_status"], "NOT_INSPECTED")
        self.assertEqual(out["stop_reason"], "QUERY_WINDOWS_EXHAUSTED")

    def test_rate_limit_retains_first_page_and_stops(self):
        c = config()
        calls = []
        def send(ep, params):
            calls.append(params)
            if len(calls) == 1:
                return page(["1"], "next")
            raise urllib.error.HTTPError(ep, 429, "not logged", {}, None)
        out = x.run(c, x.digest(x.plan(c)), send, NOW)
        self.assertEqual(len(calls), 2)
        self.assertEqual(out["stop_reason"], "HTTP_429")
        self.assertEqual(out["results"][0]["post_id"], "1")

    def test_repeated_token_and_partial_error(self):
        c = config()
        for pages in ([page(["1"], "next"), page([]), page(["2"], "next")],
                      [page(["1"], errors=[{"detail":"untrusted"}])]):
            it = iter(pages)
            out = x.run(c, x.digest(x.plan(c)), lambda ep, p: next(it), NOW)
            self.assertEqual(out["stop_reason"], "PARTIAL_RESPONSE_OR_REPEATED_TOKEN")
            self.assertNotIn("untrusted", str(out))

    def test_expired_recent_window_and_archive(self):
        c = config()
        c["start_time"] = "2026-10-23T00:00:00Z"
        with self.assertRaises(ValueError):
            x.plan(c)
        c["mode"] = "all"
        seen = []
        def send(ep, params):
            seen.append(ep)
            return page([])
        x.run(c, x.digest(x.plan(c)), send, NOW)
        self.assertTrue(all(ep == x.BASE + "all" for ep in seen))
        c = config()
        with self.assertRaises(ValueError):
            x.run(c, x.digest(x.plan(c)), send, NOW + dt.timedelta(days=10))

    def test_cap_uses_reserved_reads_and_no_redirect(self):
        c = config()
        c["max_posts"] = 25
        calls = []
        def send(ep, params):
            calls.append(params)
            return page(["1"], "next")
        out = x.run(c, x.digest(x.plan(c)), send, NOW)
        self.assertEqual(len(calls), 2)
        self.assertEqual(out["max_reads_reserved"], 20)
        self.assertEqual(out["stop_reason"], "CAP_REACHED")
        with self.assertRaises(urllib.error.HTTPError):
            x.NoRedirect().redirect_request(type("Req", (), {"full_url": x.BASE})(), None, 302, "", {}, "https://evil.example")

    def test_invalid_page_withheld_and_no_fake_success(self):
        c = config()
        out = x.run(c, x.digest(x.plan(c)), lambda ep,p: {"data": []}, NOW)
        self.assertEqual(out["stop_reason"], "TRANSPORT_OR_INVALID_RESPONSE")
        p = page(["1"])
        p["data"][0]["withheld"] = {"scope": "post"}
        self.assertEqual(x.parse_page(p, 10), ([], 1, None, False))

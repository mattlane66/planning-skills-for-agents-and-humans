import importlib.util
import pathlib
import unittest
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("search_grok_x", ROOT / "lead-user-research/scripts/search_grok_x.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def config():
    return {"model":"grok-4.7","from_date":"2026-01-01","to_date":"2026-02-01",
            "max_requests":2,"max_turns":2,"max_output_tokens":1500,"stop_after_usd":"1.00",
            "queries":[{"id":"Q1","lane":"rare","query":"Unusual failures"},
                       {"id":"Q2","lane":"contradiction","query":"Abandoned attempts"}]}


def response(cost=100000000, posts=10, users=0, status="completed"):
    return {"model":"grok-4.7","status":status,
            "usage":{"input_tokens":100,"output_tokens":50,"cost_in_usd_ticks":cost,
                     "server_side_tool_usage_details":{"x_search_calls":2,"x_posts_fetched":posts,"x_users_fetched":users}},
            "output":[{"type":"custom_tool_call","name":"x_semantic_search","input":"untrusted"},
                      {"type":"message","role":"assistant","content":[{"type":"output_text",
                       "text":"RAW GENERATED TEXT https://x.com/a/status/999",
                       "annotations":[{"type":"url_citation","url":"https://x.com/a/status/123"},
                                      {"type":"url_citation","url":"https://twitter.com/b/status/123"},
                                      {"type":"url_citation","url":"https://x.com/i/status/456"},
                                      {"type":"url_citation","url":"https://x.com.evil.example/a/status/666"},
                                      {"type":"url_citation","url":"https://x.com/i/user/789"},
                                      {"type":"url_citation","url":"https://x.com@evil.example/a/status/555"}]}]}]}


class GrokXTests(unittest.TestCase):
    def test_exact_approval_and_native_only(self):
        c = config()
        p = g.plan(c)
        calls = []
        def send(body):
            calls.append(body)
            return response()
        with self.assertRaises(ValueError):
            g.run(c, "wrong", send)
        self.assertEqual(calls, [])
        out = g.run(c, g.digest(p), send)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["tools"], [{"type":"x_search","from_date":"2026-01-01","to_date":"2026-02-01",
                                               "enable_image_understanding":False,"enable_video_understanding":False}])
        self.assertFalse(calls[0]["store"])
        self.assertEqual(calls[0]["max_turns"], 2)
        self.assertEqual([r["post_id"] for r in out["results"]], ["123","456"])
        self.assertEqual(out["results"][0]["matches"], ["Q1","Q2"])
        self.assertNotIn("RAW GENERATED TEXT", str(out))
        self.assertEqual(out["results"][0]["inspection_status"], "NOT_INSPECTED")
        self.assertEqual(out["results"][0]["scope_status"], "UNVERIFIED")
        self.assertEqual(out["known_cost_usd"], "0.02")
        c["queries"][0]["query"] = "changed"
        with self.assertRaises(ValueError):
            g.run(c, g.digest(p), send)

    def test_stop_after_threshold_not_hard_cap(self):
        c = config()
        out = g.run(c, g.digest(g.plan(c)), lambda _: response(cost=12000000000))
        self.assertEqual(out["stop_reason"], "SPEND_THRESHOLD_REACHED")
        self.assertEqual(out["known_cost_usd"], "1.2")
        self.assertEqual(out["queries"][1]["status"], "NOT_RUN")

    def test_missing_usage_incomplete_and_profile_stop(self):
        c = config()
        for r, reason in [(response(cost=None),"USAGE_UNKNOWN"),
                          (response(status="incomplete"),"INCOMPLETE_RESPONSE"),
                          (response(users=2),"UNEXPECTED_PROFILE_FETCH")]:
            out = g.run(c,g.digest(g.plan(c)),lambda _: r)
            self.assertEqual(out["stop_reason"], reason)
            self.assertEqual(out["queries"][1]["status"], "NOT_RUN")

    def test_no_search_or_no_posts_never_accepts_citations(self):
        r = response()
        r["usage"]["server_side_tool_usage_details"]["x_search_calls"] = 0
        self.assertEqual(g.parse_response(r)["post_ids"], [])
        self.assertEqual(g.parse_response(response(posts=0))["post_ids"], [])

    def test_http_failure_preserves_previous_leads(self):
        c = config()
        calls = []
        def send(p):
            calls.append(p)
            if len(calls) == 1:
                return response()
            raise urllib.error.HTTPError(g.ENDPOINT, 429, "not logged", {}, None)
        out = g.run(c,g.digest(g.plan(c)),send)
        self.assertEqual(out["stop_reason"],"HTTP_429")
        self.assertEqual(len(out["results"]),2)

    def test_reject_invalid_bounds_and_redirect(self):
        for k,v in [("max_turns",0),("max_requests",1),("stop_after_usd","NaN"),("to_date","2026-01-01T00:00:00Z")]:
            c = config()
            c[k] = v
            with self.assertRaises(ValueError):
                g.plan(c)
        with self.assertRaises(urllib.error.HTTPError):
            g.NoRedirect().redirect_request(type("Req",(),{"full_url":g.ENDPOINT})(),None,302,"",{},"https://evil.example")

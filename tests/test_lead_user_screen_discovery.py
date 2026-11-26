import importlib.util
import pathlib
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("screen_discovery", ROOT / "lead-user-research/scripts/screen_discovery.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def corpus(n=12):
    return {"context": "Storage constraints and rival explanations", "items": [
        {"source_ref": str(i), "original_ref": str(i), "platform": "X",
         "excerpt": f"Untrusted excerpt {i}", "permission": "PUBLIC_APPROVED"} for i in range(n)]}


def reply(model="jev-1.14.0", value=.4):
    return {"model": model, "answers": {k: {"type": "noul", "noul": value} for k in s.QUESTIONS},
            "usage": {"input_tokens": 15, "output_tokens": 8}}


class ScreeningTests(unittest.TestCase):
    def test_preview_no_network_and_exact_binding(self):
        data = corpus()
        manifest = s.plan(data, "jev-1.14.0", 3)
        calls = []
        def send(p):
            calls.append(p)
            return reply()
        with self.assertRaises(ValueError):
            s.screen(data, "jev-1.14.0", 3, "bad", send)
        self.assertEqual(calls, [])
        changed = corpus()
        changed["items"][0]["excerpt"] = "changed"
        with self.assertRaises(ValueError):
            s.screen(changed, "jev-1.14.0", 3, s.digest(manifest), send)
        self.assertEqual(calls, [])
        out = s.screen(data, "jev-1.14.0", 3, s.digest(manifest), send)
        self.assertEqual(len(calls), 3)
        self.assertEqual(len(out["rows"]), 12)
        self.assertEqual(out["rows"][3]["status"], "NOT_SCREENED")
        self.assertEqual(set(calls[0]["state"]), {"research_context", "untrusted_source_excerpt"})
        self.assertNotIn("source_ref", str(calls[0]))
        self.assertEqual(out["evidentiary_role"], "DISCOVERY_SIGNAL")

    def test_unapproved_and_unpinned_fail(self):
        data = corpus()
        data["items"][0]["permission"] = "PRIVATE"
        with self.assertRaises(ValueError):
            s.plan(data, "jev-1.14.0", 3)
        with self.assertRaises(ValueError):
            s.plan(corpus(), "jev-latest", 3)

    def test_invalid_answer_quarantines_and_stops(self):
        for bad in (reply("jev-other"), reply(value=float("nan")), reply(value=True), reply(value=2)):
            with self.subTest(bad=bad):
                data = corpus()
                calls = []
                def send(p):
                    calls.append(p)
                    return bad
                out = s.screen(data, "jev-1.14.0", 8, s.digest(s.plan(data, "jev-1.14.0", 8)), send)
                self.assertEqual(len(calls), 1)
                self.assertEqual(out["rows"][0]["status"], "ERROR")
                self.assertNotIn("scores", out["rows"][0])
                self.assertTrue(all(r["status"] == "NOT_SCREENED" for r in out["rows"][1:]))

    def test_rare_low_relevance_survives_and_derivatives_group(self):
        data = corpus(20)
        data["items"][19]["original_ref"] = "18"
        def send(p):
            i = int(p["state"]["untrusted_source_excerpt"].split()[-1])
            r = reply(value=.1)
            r["answers"]["relevance"]["noul"] = 1 - i/20
            if i == 17:
                r["answers"]["unusual_constraint"]["noul"] = .99
            return r
        out = s.screen(data, "jev-1.14.0", 20, s.digest(s.plan(data, "jev-1.14.0", 20)), send)
        q = s.queue(out["rows"], 10, 2, 41)
        self.assertIn("17", [r["original_ref"] for r in q])
        self.assertEqual(len(q), 10)
        self.assertEqual(len({r["original_ref"] for r in q}), 10)
        self.assertEqual(sum(r["lane"] == "low_rank_audit" for r in q), 2)
        self.assertEqual(q, s.queue(out["rows"], 10, 2, 41))
        labels = {str(i): i == 17 for i in range(19)}
        metrics = s.compare(out, labels, 10, 2, 41)
        self.assertEqual(metrics["results"]["diverse"]["bounded_recall"], 1)
        self.assertEqual(metrics["results"]["relevance"]["bounded_recall"], 0)
        self.assertIsNone(s.compare(out, {"17": True}, 10, 2, 41)["results"]["diverse"]["bounded_recall"])

    def test_unscored_kept_for_audit(self):
        data = corpus()
        out = s.screen(data, "jev-1.14.0", 2, s.digest(s.plan(data, "jev-1.14.0", 2)), lambda p: reply())
        q = s.queue(out["rows"], 5, 1, 41)
        self.assertEqual(q[0]["lane"], "low_rank_audit")
        self.assertNotIn(q[0]["original_ref"], {"0", "1"})

    def test_no_redirect(self):
        import urllib.error
        with self.assertRaises(urllib.error.HTTPError):
            s.NoRedirect().redirect_request(type("Req", (), {"full_url": s.ENDPOINT})(), None, 302, "", {}, "https://evil.example")

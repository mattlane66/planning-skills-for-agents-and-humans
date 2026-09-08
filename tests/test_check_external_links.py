import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

SPEC = importlib.util.spec_from_file_location(
    "external_links", Path(__file__).resolve().parents[1] / "scripts/check-external-links.py"
)
links = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(links)


class Response:
    def __init__(self, code=200, headers=None):
        self.status = code
        self.headers = headers or {}

    def geturl(self):
        return "https://example.org/final"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class ExternalLinkTests(unittest.TestCase):
    def checker(self, responses):
        requests, sleeps = [], []
        queue = iter(responses)

        def opener(request, timeout):
            requests.append((request.method, timeout))
            response = next(queue)
            if isinstance(response, Exception):
                raise response
            return response

        return links.Checker(opener, sleeps.append, lambda: 0), requests, sleeps

    def test_inventory_handles_markdown_and_deduplicates_fragments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "doc.md").write_text(
                '**[one](https://example.org/page)**\n'
                '[two](https://example.org/page#part)\n'
                '<https://example.org/a_(b)>\n'
                '[ref]: https://example.org/reference\n', encoding="utf-8"
            )
            with patch.object(links.subprocess, "check_output", return_value=b"doc.md\0"):
                inventory = links.collect(root)
            self.assertEqual(["doc.md:1", "doc.md:2"], inventory["https://example.org/page"])
            self.assertIn("https://example.org/a_(b)", inventory)
            self.assertIn("https://example.org/reference", inventory)

    def test_success_records_redirect_and_request_timeout(self):
        checker, requests, _ = self.checker([Response()])
        result = checker.check("https://example.org")
        self.assertEqual("ok", result["result"])
        self.assertEqual("https://example.org/final", result["final_url"])
        self.assertEqual([("HEAD", 15)], requests)

    def test_head_fallback_is_rate_limited(self):
        error = urllib.error.HTTPError("https://example.org", 405, "method", {}, None)
        checker, requests, sleeps = self.checker([error, Response()])
        self.assertEqual("ok", checker.check("https://example.org")["result"])
        self.assertEqual([("HEAD", 15), ("GET", 15)], requests)
        self.assertIn(1, sleeps)

    def test_transient_errors_retry_and_honor_retry_after(self):
        checker, requests, sleeps = self.checker([
            Response(429, {"Retry-After": "4"}), urllib.error.URLError("offline"), Response()
        ])
        self.assertEqual("ok", checker.check("https://example.org")["result"])
        self.assertEqual(3, len(requests))
        self.assertIn(4, sleeps)
        self.assertIn(2, sleeps)

    def test_long_retry_after_does_not_retry_early(self):
        checker, requests, sleeps = self.checker([Response(429, {"Retry-After": "120"})])
        self.assertEqual("unverified", checker.check("https://example.org")["result"])
        self.assertEqual(1, len(requests))
        self.assertEqual([], sleeps)

    def test_outage_is_unverified_after_three_attempts(self):
        checker, requests, _ = self.checker([Response(503)] * 3)
        self.assertEqual("unverified", checker.check("https://example.org")["result"])
        self.assertEqual(3, len(requests))

    def test_missing_page_is_broken_but_bot_block_is_unverified(self):
        for code, expected, count in [(404, "broken", 1), (410, "broken", 1), (403, "unverified", 2)]:
            with self.subTest(code=code):
                checker, requests, _ = self.checker([Response(code)] * count)
                self.assertEqual(expected, checker.check("https://example.org")["result"])
                self.assertEqual(count, len(requests))

    def test_explicit_skips_do_not_make_requests(self):
        for url in ["http://127.0.0.1:3456", "http://localhost", *links.AUTH_ONLY]:
            checker, requests, _ = self.checker([])
            self.assertEqual("skipped", checker.check(url)["result"])
            self.assertEqual([], requests)


if __name__ == "__main__":
    unittest.main()

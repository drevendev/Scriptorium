"""Offline provider-contract tests: synthetic responses, no network or real sleeps."""
import io
import json
import unittest
from email.utils import formatdate
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

from scriptorium import mediawiki_api as api
from scriptorium import wikisource_freeze, wikisource_replay, single_page_revision

URL = "https://ru.wikisource.org/w/api.php"
GOOD = {"query": {"pages": []}}


class Reply(io.BytesIO):
    def __init__(self, payload=GOOD, retry_after=None, *, raw=None):
        super().__init__(json.dumps(payload).encode() if raw is None else raw)
        self.headers = {} if retry_after is None else {"Retry-After": retry_after}


class MediaWikiTransportTests(unittest.TestCase):
    def run_query(self, responses, *, params=None):
        opener = Mock(side_effect=responses)
        sleep = Mock()
        result = api.query_json(params or {"action": "query", "revids": "123|456"},
                                api_url=URL, user_agent="Scriptorium test", opener=opener,
                                sleep=sleep, now=lambda: 1_700_000_000)
        return result, opener, sleep

    def assert_stops(self, response, error=api.MediaWikiReadError):
        opener, sleep = Mock(side_effect=[response]), Mock()
        with self.assertRaises(error) as raised:
            api.query_json({"action": "query"}, api_url=URL, user_agent="test",
                           opener=opener, sleep=sleep)
        self.assertEqual(opener.call_count, 1)
        sleep.assert_not_called()
        self.assertNotIn("PRIVATE_BODY", str(raised.exception))
        self.assertNotIn("PRIVATE_BODY", repr(raised.exception))
        return raised.exception

    def test_success_preserves_payload_and_request(self):
        params = {"action": "query", "revids": "123|456"}
        reply = Reply()
        result, opener, sleep = self.run_query([reply], params=params)
        self.assertEqual(result, GOOD)
        self.assertTrue(reply.closed)
        sleep.assert_not_called()
        request = opener.call_args.args[0]
        query = parse_qs(urlsplit(request.full_url).query)
        self.assertEqual(query["revids"], ["123|456"])
        self.assertEqual(query["maxlag"], ["5"])
        self.assertEqual(query["formatversion"], ["2"])
        self.assertNotIn("redirects", query)
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.get_header("User-agent"), "Scriptorium test")
        self.assertEqual(opener.call_args.kwargs["timeout"], 30)
        self.assertEqual(params, {"action": "query", "revids": "123|456"})

    def test_maxlag_is_not_disabled_by_caller(self):
        _, opener, _ = self.run_query([Reply()], params={"action": "query", "maxlag": "-1"})
        self.assertEqual(parse_qs(urlsplit(opener.call_args.args[0].full_url).query)["maxlag"], ["5"])

    def test_classic_and_modern_transient_errors(self):
        for payload in ({"error": {"code": "maxlag"}}, {"error": {"code": "ratelimited"}},
                        {"errors": [{"code": "maxlag"}, {"code": "ratelimited"}]}):
            with self.subTest(payload=payload):
                _, opener, sleep = self.run_query([Reply(payload, "7"), Reply()])
                sleep.assert_called_once_with(7)
                self.assertEqual(opener.call_count, 2)
                self.assertIs(opener.call_args_list[0].args[0], opener.call_args_list[1].args[0])

    def test_http_throttle_and_marked_503(self):
        for status, header, delay in ((429, None, 5), (429, "8", 8), (503, "9", 9)):
            with self.subTest(status=status, header=header):
                headers = {} if header is None else {"Retry-After": header}
                body = io.BytesIO(b"PRIVATE_BODY")
                error = HTTPError(URL, status, "PRIVATE_BODY", headers, body)
                _, opener, sleep = self.run_query([error, Reply()])
                self.assertTrue(body.closed)
                sleep.assert_called_once_with(delay)
                self.assertEqual(opener.call_count, 2)

    def test_exhaustion_has_three_attempts_and_two_sleeps(self):
        opener = Mock(side_effect=[Reply({"error": {"code": "maxlag"}}) for _ in range(3)])
        sleep = Mock()
        with self.assertRaisesRegex(api.MediaWikiRetryError, "after three attempts"):
            api.query_json({}, api_url=URL, user_agent="test", opener=opener, sleep=sleep)
        self.assertEqual(opener.call_count, 3)
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [5, 10])

    def test_http_exhaustion_is_bounded(self):
        errors = [HTTPError(URL, 429, "PRIVATE_BODY", {}, None) for _ in range(3)]
        opener, sleep = Mock(side_effect=errors), Mock()
        with self.assertRaises(api.MediaWikiRetryError):
            api.query_json({}, api_url=URL, user_agent="test", opener=opener, sleep=sleep)
        self.assertEqual(opener.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    def test_retry_after_http_date_and_minimum(self):
        now = 1_700_000_000
        for header, delay in ((formatdate(now + 20, usegmt=True), 20),
                              (formatdate(now - 20, usegmt=True), 5), ("0", 5), ("0007", 7)):
            with self.subTest(header=header):
                _, _, sleep = self.run_query([Reply({"error": {"code": "maxlag"}}, header), Reply()])
                sleep.assert_called_once_with(delay)

    def test_retry_after_invalid_or_long_fails_without_early_retry(self):
        for header in ("-1", "1.5", "NaN", "tomorrow", "", "120", "9" * 5000,
                       "Tue, 14 Nov 2090 22:13:20 GMT", 7):
            with self.subTest(header=str(header)[:20]):
                self.assert_stops(Reply({"error": {"code": "maxlag"}}, header), api.MediaWikiRetryError)

    def test_total_wait_budget_not_per_attempt_budget(self):
        opener = Mock(side_effect=[Reply({"error": {"code": "maxlag"}}, "40"),
                                   Reply({"error": {"code": "maxlag"}}, "30"), Reply()])
        sleep = Mock()
        with self.assertRaisesRegex(api.MediaWikiRetryError, "remaining wait budget"):
            api.query_json({}, api_url=URL, user_agent="test", opener=opener, sleep=sleep)
        self.assertEqual(opener.call_count, 2)
        sleep.assert_called_once_with(40)

    def test_exact_budget_allowed(self):
        _, opener, sleep = self.run_query([Reply({"error": {"code": "maxlag"}}, "30"),
                                           Reply({"error": {"code": "maxlag"}}, "30"), Reply()])
        self.assertEqual(opener.call_count, 3)
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [30, 30])

    def test_permanent_http_and_unmarked_503_not_retried(self):
        for status in (400, 401, 403, 404, 500, 502, 503, 504):
            with self.subTest(status=status):
                error = HTTPError(URL + "?text=PRIVATE_BODY", status, "PRIVATE_BODY", {}, None)
                self.assert_stops(error)

    def test_network_errors_not_retried(self):
        for error in (URLError("PRIVATE_BODY"), TimeoutError("PRIVATE_BODY"), OSError("PRIVATE_BODY")):
            with self.subTest(error=type(error).__name__):
                self.assert_stops(error)

    def test_unknown_mixed_and_malformed_api_errors_not_retried(self):
        for payload in ({"error": {"code": "badvalue", "info": "PRIVATE_BODY"}},
                        {"error": "PRIVATE_BODY"}, {"error": {"code": []}},
                        {"errors": []}, {"errors": "PRIVATE_BODY"},
                        {"errors": [{"code": "maxlag"}, {"code": "permissiondenied"}]},
                        {"error": {"code": "maxlag"}, "errors": [{"code": "badvalue"}]}):
            with self.subTest(payload=payload):
                self.assert_stops(Reply(payload))

    def test_invalid_json_nonfinite_duplicates_not_retried(self):
        for raw in (b"<html>PRIVATE_BODY</html>", b'{"x": NaN}', b'{"x": 1e999}',
                    b'{"query":{},"query":{}}', b'{"a":{"x":1,"x":2}}',
                    b'{"x": Infinity}', b"[]", b"null", b"\xff"):
            with self.subTest(raw=raw):
                self.assert_stops(Reply(raw=raw))

    def test_response_byte_limit(self):
        with patch.object(api, "MAX_RESPONSE_BYTES", 16):
            self.assert_stops(Reply(raw=b" " * 17))

    def test_shared_adapters_retry_without_changing_pinned_query(self):
        for module in (wikisource_freeze, single_page_revision):
            with self.subTest(adapter=module.__name__):
                with patch.object(module, "urlopen", side_effect=[Reply({"error": {"code": "maxlag"}}), Reply()]) as opener, \
                     patch.object(api.time, "sleep") as sleep:
                    self.assertEqual(module._api_query({"action": "query", "revids": "10"}), GOOD)
                    sleep.assert_called_once_with(5)
                    self.assertEqual(opener.call_count, 2)

    def test_success_after_throttle_still_rejects_source_identity_drift(self):
        row = {"title": "Synthetic", "revision_id": 1,
               "revision_timestamp": "2026-01-01T00:00:00Z", "mediawiki_sha1": "a" * 40}
        wrong = {"query": {"pages": [{"title": "Synthetic", "revisions": [{"revid": 2}]}]}}
        with patch.object(wikisource_freeze, "urlopen", side_effect=[Reply({"error": {"code": "maxlag"}}), Reply(wrong)]) as opener, \
             patch.object(api.time, "sleep") as sleep:
            with self.assertRaisesRegex(ValueError, "unexpected revision id"):
                wikisource_replay.fetch_pinned_chapter_revisions([row], query=wikisource_freeze._api_query)
            self.assertEqual(opener.call_count, 2)
            sleep.assert_called_once_with(5)

    def test_missing_query_does_not_trigger_retry(self):
        with patch.object(single_page_revision, "urlopen", return_value=Reply({"unrelated": 1})) as opener, \
             patch.object(api.time, "sleep") as sleep:
            with self.assertRaisesRegex(ValueError, "missing query"):
                single_page_revision.fetch_pinned_revision(title="Synthetic", revision_id=1,
                                                          query=single_page_revision._api_query)
            self.assertEqual(opener.call_count, 1)
            sleep.assert_not_called()

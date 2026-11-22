"""Source-verified third full-work N replay, without publishing any prose."""
from __future__ import annotations

import contextlib
import copy
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scriptorium.running_waves_body import build_manifest
from scriptorium.running_waves_native_n import main, prepare_running_waves_request

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "corpus/candidates/source-edition-traces/grin-running-on-waves-ru.source-revisions.json"
BODY_PATH = ROOT / "corpus/candidates/source-edition-traces/grin-running-on-waves-ru.literary-body.json"


def frozen_source():
    return json.loads(SOURCE_PATH.read_text(encoding="utf-8"))


def local_fetch(identities):
    return {
        str(row["title"]): '<div class="text">' +
            (f'Страница {row["ordinal"]}. Литературное контрольное предложение. ' * 220) +
            '</div>'
        for row in identities
    }


class ThirdFullWorkNTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = frozen_source()
        cls.body = build_manifest(cls.source, fetcher=local_fetch)

    def test_complete_verified_body_yields_exact_canonical_transport(self):
        calls = []

        def observed(identities):
            identities = tuple(identities)
            calls.append(len(identities))
            return local_fetch(identities)

        request = prepare_running_waves_request(self.source, self.body, fetcher=observed)
        self.assertEqual(calls, [36])
        self.assertEqual(request["schema_version"], "scriptorium-pylem-sidecar-request-v1")
        self.assertEqual(request["normalized_sha256"],
                         self.body["composite_identity"]["normalized_sha256"])
        self.assertEqual(len(request["normalized_text"]),
                         self.body["composite_identity"]["normalized_character_count_including_spaces"])
        self.assertGreater(len(request["tokens"]), 1000)
        self.assertEqual(request["tokens"][0]["ordinal"], 0)

    def test_changed_or_missing_page_is_rejected_before_provider(self):
        for change in ("changed", "missing", "extra"):
            def corrupt(identities):
                pages = local_fetch(identities)
                first = next(iter(pages))
                if change == "changed":
                    pages[first] = pages[first].replace("Страница", "Искажено", 1)
                elif change == "missing":
                    pages.pop(first)
                else:
                    pages["unexpected-page"] = '<div class="text">Чужой текст</div>'
                return pages

            with self.subTest(change=change), self.assertRaises(ValueError):
                prepare_running_waves_request(self.source, self.body, fetcher=corrupt)

    def test_source_or_body_identity_drift_fails_closed(self):
        source = copy.deepcopy(self.source)
        source["bibliographic_source"] = "tampered"
        with self.assertRaises(ValueError):
            prepare_running_waves_request(source, self.body, fetcher=local_fetch)
        body = copy.deepcopy(self.body)
        body["composite_identity"]["normalized_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            prepare_running_waves_request(self.source, body, fetcher=local_fetch)
        body = copy.deepcopy(self.body)
        body["per_page_identities"][0]["raw_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            prepare_running_waves_request(self.source, body, fetcher=local_fetch)

    def test_create_only_ephemeral_cli_never_overwrites_inputs(self):
        example = {
            "schema_version": "scriptorium-pylem-sidecar-request-v1",
            "normalized_sha256": "a" * 64,
            "normalized_text": "Только временный текст.",
            "tokens": [],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.json"
            body = root / "body.json"
            request = root / "request.json"
            source.write_text("{}", encoding="utf-8")
            body.write_text("{}", encoding="utf-8")
            args = ["--source-manifest", str(source), "--body-manifest", str(body),
                    "--request", str(request)]
            with patch("scriptorium.running_waves_native_n.prepare_running_waves_request",
                       return_value=example):
                self.assertEqual(main(args), 0)
                saved = request.read_bytes()
                self.assertIn(b'"tokens"', saved)
                with contextlib.redirect_stderr(StringIO()) as error:
                    with self.assertRaises(SystemExit) as blocked:
                        main(args)
                self.assertEqual(blocked.exception.code, 2)
                self.assertIn("already exists", error.getvalue())
                self.assertEqual(request.read_bytes(), saved)
                alias = root / "alias.json"
                try:
                    alias.symlink_to(request)
                except (NotImplementedError, OSError):
                    return
                with contextlib.redirect_stderr(StringIO()):
                    with self.assertRaises(SystemExit) as blocked:
                        main([*args[:-1], str(alias)])
                self.assertEqual(blocked.exception.code, 2)
                self.assertEqual(request.read_bytes(), saved)

    def test_native_job_only_uploads_derived_source_free_result(self):
        workflow = (ROOT / ".github/workflows/morphology-provider.yml").read_text(encoding="utf-8")
        self.assertIn("third-running-waves-native-n:", workflow)
        job = workflow.split("  third-running-waves-native-n:", 1)[1]
        self.assertIn("scriptorium.running_waves_native_n", job)
        self.assertIn("scriptorium.n_collision_diagnostic", job)
        self.assertIn("if: always()", job)
        self.assertIn("rm -f build/morph/grin-pylem-request.json", job)
        self.assertIn("scriptorium-grin-pylem-n-only-impact", job)
        self.assertNotIn("build/morph/grin-pylem-request.json\n          if-no-files-found", job)
        self.assertNotIn("build/morph/grin-pylem-response.json\n          if-no-files-found", job)


if __name__ == "__main__":
    unittest.main()

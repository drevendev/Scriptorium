from __future__ import annotations

import re
import unittest
from pathlib import Path

from scriptorium.site_renderer import _ALLOWED_ARTIFACT_ROOTS


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "pages.yml"
PUBLICATION_PROVENANCE_TRIGGER = "corpus/candidates/source-edition-traces/**"


def _event_paths(workflow: str, event: str) -> set[str]:
    lines = workflow.splitlines()
    marker = f"  {event}:"
    try:
        start = lines.index(marker)
    except ValueError as exc:
        raise AssertionError(f"workflow is missing {event!r} trigger") from exc

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("  ") and not line.startswith("    "):
            end = index
            break

    in_paths = False
    paths: set[str] = set()
    for line in lines[start + 1 : end]:
        if line == "    paths:":
            in_paths = True
            continue
        if not in_paths:
            continue
        if line.startswith("      - "):
            paths.add(line.removeprefix("      - ").strip().strip('"'))
            continue
        if line.startswith("    ") and not line.startswith("      "):
            break
    return paths


class PagesWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_all_actions_are_full_sha_pinned(self) -> None:
        uses_lines = [
            line.strip()
            for line in self.workflow.splitlines()
            if line.strip().startswith("uses:")
        ]
        self.assertEqual(len(uses_lines), 5)
        for line in uses_lines:
            self.assertRegex(
                line,
                r"^uses: actions/[a-z0-9-]+@[0-9a-f]{40}(?: # v[0-9.]+)?$",
            )

        expected = {
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1",
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0",
            "actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9 # v5.0.0",
            "actions/configure-pages@45bfe0192ca1faeb007ade9deae92b16b8254a0d # v6.0.0",
            "actions/deploy-pages@368f82528645a54fb793d4d04e342629a3f51346 # v5.0.1",
        }
        self.assertEqual({line.removeprefix("uses: ") for line in uses_lines}, expected)

    def test_supported_publication_roots_trigger_pr_and_master_builds(self) -> None:
        required = {f"{root}/**" for root in _ALLOWED_ARTIFACT_ROOTS}
        for event in ("pull_request", "push"):
            with self.subTest(event=event):
                paths = _event_paths(self.workflow, event)
                self.assertTrue(
                    required <= paths,
                    f"{event} trigger is missing canonical publication roots: "
                    f"{sorted(required - paths)}",
                )

    def test_publication_provenance_sources_trigger_pr_and_master_builds(self) -> None:
        for event in ("pull_request", "push"):
            with self.subTest(event=event):
                paths = _event_paths(self.workflow, event)
                self.assertIn(PUBLICATION_PROVENANCE_TRIGGER, paths)

    def test_build_is_read_only_and_uses_canonical_renderer(self) -> None:
        self.assertIn("permissions:\n  contents: read\n", self.workflow)
        self.assertIn(
            "  build:\n"
            "    name: Verify and build static site\n"
            "    runs-on: ubuntu-latest\n"
            "    permissions:\n"
            "      contents: read\n",
            self.workflow,
        )
        self.assertIn("persist-credentials: false", self.workflow)
        self.assertIn('python-version: "3.13"', self.workflow)
        self.assertIn("python -m unittest discover -s tests -v", self.workflow)
        self.assertIn(
            "python -m scriptorium.site_renderer --repo-root . --output build/site",
            self.workflow,
        )
        self.assertIn("path: build/site", self.workflow)
        self.assertNotIn("site/publication-manifest.json --", self.workflow)

    def test_deploy_is_default_branch_and_explicitly_enabled_only(self) -> None:
        self.assertIn("needs: build", self.workflow)
        self.assertIn("github.ref == 'refs/heads/master'", self.workflow)
        self.assertIn("github.event_name != 'pull_request'", self.workflow)
        self.assertIn("vars.SCRIPTORIUM_PAGES_DEPLOY_ENABLED == 'true'", self.workflow)
        self.assertIn("pages: write", self.workflow)
        self.assertIn("id-token: write", self.workflow)
        self.assertIn("name: github-pages", self.workflow)
        self.assertIn("url: ${{ steps.deployment.outputs.page_url }}", self.workflow)

    def test_workflow_does_not_try_to_enable_pages_or_use_secrets(self) -> None:
        self.assertNotIn("enablement:", self.workflow)
        self.assertNotIn("secrets.", self.workflow)
        self.assertNotIn("pull_request_target", self.workflow)
        self.assertNotIn("persist-credentials: true", self.workflow)

    def test_only_disposable_site_tree_is_uploaded(self) -> None:
        upload_step = re.search(
            r"- name: Upload GitHub Pages artifact\n(?P<body>(?:\s{8,}.*\n?)+?)\n  deploy:",
            self.workflow,
        )
        self.assertIsNotNone(upload_step)
        body = upload_step.group("body")
        self.assertIn("path: build/site", body)
        self.assertNotIn("path: .", body)
        self.assertNotIn("showcase/", body)
        self.assertNotIn("site/", body)


if __name__ == "__main__":
    unittest.main()

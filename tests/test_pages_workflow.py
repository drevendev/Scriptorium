from __future__ import annotations

import re
import unittest
from pathlib import Path

from scriptorium.site_renderer import _ALLOWED_ARTIFACT_ROOTS


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "pages.yml"
PUBLICATION_PROVENANCE_TRIGGER = "corpus/candidates/source-edition-traces/**"
EXACT_HEAD_REF = "ref: ${{ github.event.pull_request.head.sha || github.sha }}"


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
        self.assertEqual(len(uses_lines), 6)
        for line in uses_lines:
            self.assertRegex(
                line,
                r"^uses: actions/[a-z0-9-]+@[0-9a-f]{40}(?: # v[0-9.]+)?$",
            )

        expected = {
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1",
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0",
            "actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9 # v5.0.0",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2",
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

    def test_pull_request_build_checks_out_exact_authored_head(self) -> None:
        self.assertEqual(self.workflow.count(EXACT_HEAD_REF), 1)

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

    def test_branch_root_preview_artifact_is_allowlisted_and_pinned(self) -> None:
        """The second artifact is a disposable QA copy, not the Pages deploy artifact."""
        self.assertIn("name: scriptorium-branch-root-preview", self.workflow)
        self.assertIn("path: build/branch-root-preview", self.workflow)
        self.assertIn("if-no-files-found: error", self.workflow)
        self.assertIn("actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4.6.2", self.workflow)
        for filename in (
            "index.html",
            "assets/pages-reader.css",
            "assets/pages-reader.js",
            "assets/evidence-snapshot.json",
        ):
            destination = "build/branch-root-preview/" + filename
            self.assertIn("cp " + filename + " " + destination, self.workflow)
        self.assertIn("test -z", self.workflow)
        self.assertNotIn("cp -r . build/branch-root-preview", self.workflow)

    def test_branch_preview_includes_every_root_reader_local_asset(self) -> None:
        """A root-Reader QA ZIP must not contain a broken no-JS CSV link."""
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        referenced = set(
            re.findall(r'(?:href|src)="\./(assets/[A-Za-z0-9_.-]+)"', html)
        )
        self.assertIn("assets/scriptorium-ru-measured-metrics.csv", referenced)
        referenced.add("assets/evidence-snapshot.json")  # fetched by Reader JS

        def missing(workflow: str) -> set[str]:
            return {
                path for path in referenced
                if f"cp {path} build/branch-root-preview/{path}" not in workflow
            }

        self.assertEqual(missing(self.workflow), set())
        without_csv = self.workflow.replace(
            "cp assets/scriptorium-ru-measured-metrics.csv "
            "build/branch-root-preview/assets/scriptorium-ru-measured-metrics.csv",
            "",
            1,
        )
        self.assertEqual(
            missing(without_csv), {"assets/scriptorium-ru-measured-metrics.csv"}
        )
        self.assertIn(
            "test -s build/branch-root-preview/assets/scriptorium-ru-measured-metrics.csv",
            self.workflow,
        )
        self.assertIn(
            "cmp assets/scriptorium-ru-measured-metrics.csv "
            "build/branch-root-preview/assets/scriptorium-ru-measured-metrics.csv",
            self.workflow,
        )

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

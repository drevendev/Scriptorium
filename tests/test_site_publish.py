"""Actual Linux filesystem regressions for canonical atomic site publication."""
import errno
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scriptorium import site_publish as p


@unittest.skipUnless(p.sys.platform.startswith("linux"), "requires Linux renameat2")
class AtomicSitePublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dest = self.root / "build" / "site"

    def tearDown(self):
        self.temp.cleanup()

    def test_first_publish_and_refresh_discard_stale_files(self):
        with p.staged_site(self.root, self.dest) as stage:
            (stage / "index.html").write_text("first")
        (self.dest / "stale.html").write_text("stale")
        with p.staged_site(self.root, self.dest) as stage:
            (stage / "index.html").write_text("second")
        self.assertEqual((self.dest / "index.html").read_text(), "second")
        self.assertFalse((self.dest / "stale.html").exists())

    def test_renderer_failure_does_not_remove_last_valid_site(self):
        self.dest.mkdir(parents=True)
        (self.dest / "index.html").write_text("old")
        with self.assertRaisesRegex(RuntimeError, "injected"):
            with p.staged_site(self.root, self.dest) as stage:
                (stage / "index.html").write_text("new")
                raise RuntimeError("injected failure")
        self.assertEqual((self.dest / "index.html").read_text(), "old")

    def test_first_publish_does_not_replace_concurrent_destination(self):
        rename = p._atomic_rename
        def create_competing_output(source, destination, *, replacing):
            self.assertFalse(replacing)
            destination.mkdir()
            (destination / "index.html").write_text("other writer")
            return rename(source, destination, replacing=replacing)
        with patch.object(p, "_atomic_rename", side_effect=create_competing_output):
            with self.assertRaises(FileExistsError):
                with p.staged_site(self.root, self.dest) as stage:
                    (stage / "index.html").write_text("ours")
        self.assertEqual((self.dest / "index.html").read_text(), "other writer")

    def test_missing_atomic_primitive_fails_without_data_loss(self):
        self.dest.mkdir(parents=True)
        (self.dest / "index.html").write_text("old")
        with patch.object(p, "_atomic_rename", side_effect=OSError(errno.ENOTSUP, "unavailable")):
            with self.assertRaises(OSError):
                with p.staged_site(self.root, self.dest) as stage:
                    (stage / "index.html").write_text("new")
        self.assertEqual((self.dest / "index.html").read_text(), "old")

    def test_concurrent_same_output_is_not_silently_clobbered(self):
        with p.staged_site(self.root, self.dest) as stage:
            (stage / "index.html").write_text("outer")
            with self.assertRaisesRegex(OSError, "already in progress"):
                with p.staged_site(self.root, self.dest) as other:
                    (other / "index.html").write_text("inner")
        self.assertEqual((self.dest / "index.html").read_text(), "outer")

    def test_destination_symlink_refused_and_external_data_retained(self):
        external = self.root / "external"
        external.mkdir()
        (external / "keep").write_text("safe")
        self.dest.parent.mkdir()
        self.dest.symlink_to(external, target_is_directory=True)
        with self.assertRaisesRegex(OSError, "symlinks"):
            with p.staged_site(self.root, self.dest) as stage:
                (stage / "index.html").write_text("new")
        self.assertEqual((external / "keep").read_text(), "safe")


if __name__ == "__main__":
    unittest.main()

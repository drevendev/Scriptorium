"""Bounded subprocess regressions for the Linux static-site publisher."""
from contextlib import contextmanager
from hashlib import sha256
import os
from pathlib import Path
import selectors
import subprocess
import sys
import tempfile
import unittest

from scriptorium import site_publish


@unittest.skipUnless(sys.platform.startswith("linux"), "Linux publication backend")
class CrashRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.destination = self.root / "build" / "site"
        self.lock = self.root / "build" / (
            ".site-publish-" + sha256(b"build/site").hexdigest()[:20] + ".lock"
        )

    def publish(self, text):
        with site_publish.staged_site(self.root, self.destination) as stage:
            (stage / "index.html").write_text(text, encoding="utf-8")

    @contextmanager
    def interrupted_writer(self):
        program = """
import sys, time
from pathlib import Path
from scriptorium.site_publish import staged_site
root = Path(sys.argv[1])
with staged_site(root, root / 'build' / 'site') as stage:
    (stage / 'index.html').write_text('uncommitted', encoding='utf-8')
    print('LOCKED', flush=True)
    time.sleep(60)
"""
        child = subprocess.Popen(
            [sys.executable, "-c", program, str(self.root)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])},
        )
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ)
                self.assertTrue(selector.select(timeout=5), "publisher child timed out")
                self.assertEqual(child.stdout.readline().strip(), "LOCKED")
            yield
        finally:
            child.kill()
            child.wait(timeout=5)
            child.stdout.close()
            child.stderr.close()

    def test_abrupt_death_releases_first_publication_lock(self):
        with self.interrupted_writer():
            self.assertFalse(self.destination.exists())
        self.publish("recovered")
        self.assertEqual((self.destination / "index.html").read_text(), "recovered")

    def test_abrupt_death_preserves_previous_site_and_allows_refresh(self):
        self.publish("stable")
        with self.interrupted_writer():
            self.assertEqual((self.destination / "index.html").read_text(), "stable")
        self.assertEqual((self.destination / "index.html").read_text(), "stable")
        self.publish("recovered")
        self.assertEqual((self.destination / "index.html").read_text(), "recovered")

    def test_lock_symlink_is_not_followed(self):
        self.lock.parent.mkdir()
        keeper = self.root / "keeper"
        keeper.write_text("safe")
        self.lock.symlink_to(keeper)
        with self.assertRaises(OSError):
            self.publish("not published")
        self.assertEqual(keeper.read_text(), "safe")
        self.assertFalse(self.destination.exists())

    def test_lock_fifo_is_rejected_without_waiting_for_peer(self):
        self.lock.parent.mkdir()
        os.mkfifo(self.lock)
        program = """
import sys
from pathlib import Path
from scriptorium.site_publish import staged_site
root = Path(sys.argv[1])
try:
    with staged_site(root, root / 'build' / 'site'):
        sys.exit(3)
except OSError:
    sys.exit(0)
"""
        result = subprocess.run(
            [sys.executable, "-c", program, str(self.root)],
            capture_output=True, timeout=5,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])},
        )
        self.assertEqual(result.returncode, 0)
        self.assertFalse(self.destination.exists())

    def test_lock_inode_is_stable_between_publications(self):
        self.publish("first")
        inode = self.lock.stat().st_ino
        self.publish("second")
        self.assertEqual(self.lock.stat().st_ino, inode)
        self.assertTrue(self.lock.is_file())


if __name__ == "__main__":
    unittest.main()

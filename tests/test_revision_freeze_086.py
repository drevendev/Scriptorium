from __future__ import annotations

import json
import unittest

from scriptorium.white_guard_revisions import build_manifest


class RevisionFreeze086Tests(unittest.TestCase):
    def test_live_capture_bootstrap(self):
        manifest = build_manifest()
        print("SCRIPTORIUM_REVISION_CAPTURE_086=" + json.dumps(manifest, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        self.assertEqual(20, len(manifest["pages"]))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from scriptorium.white_guard_revisions import expected_pages


class BulgakovRevisionTests(unittest.TestCase):
    def test_expected_page_count(self):
        self.assertEqual(20, len(expected_pages()))


if __name__ == "__main__":
    unittest.main()

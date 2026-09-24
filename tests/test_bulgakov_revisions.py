from __future__ import annotations

import unittest

from scriptorium.white_guard_revisions import (
    SOURCE_FAMILY_1927,
    SOURCE_FAMILY_1989,
    expected_pages,
)


class BulgakovRevisionTests(unittest.TestCase):
    def test_expected_page_count_and_partition(self):
        pages = expected_pages()
        self.assertEqual(20, len(pages))
        self.assertTrue(all(row["source_family_id"] == SOURCE_FAMILY_1927 for row in pages[:11]))
        self.assertTrue(all(row["source_family_id"] == SOURCE_FAMILY_1989 for row in pages[11:]))\n        self.assertEqual(list(range(1, 21)), [row["chapter"] for row in pages])


if __name__ == "__main__":
    unittest.main()

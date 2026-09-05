import unittest

from scripts.public_x_profile import extract_profile_status_ids, parse_status_page


class PublicXProfileTests(unittest.TestCase):
    def test_extracts_target_statuses(self):
        html = '<a href="/realDonaldTrump/status/222"></a><a href="/other/status/999"></a><a href="/realDonaldTrump/status/111"></a>'
        self.assertEqual(extract_profile_status_ids(html, "realDonaldTrump"), ["222", "111"])

    def test_parses_jina_status(self):
        page = """URL Source: http://x.com/realDonaldTrump/status/222
Published Time: 2026-09-05T01:02:03.000Z
Markdown Content:
# Donald J. Trump on X: "Public update"
"""
        post = parse_status_page(page, "realDonaldTrump", "25073877", "Donald J. Trump", "222")
        self.assertEqual(post["createdAtISO"], "2026-09-05T01:02:03Z")
        self.assertEqual(post["text"], "Public update")


if __name__ == "__main__":
    unittest.main()

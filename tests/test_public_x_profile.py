import unittest

from scripts.public_x_profile import (
    extract_profile_status_ids,
    parse_profile_posts,
    parse_status_page,
)


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

    def test_parses_public_profile_rsc_post_without_jina(self):
        profile = r'''
        <div data-href="/realDonaldTrump/status/555"></div>
        "TweetResults:555" $R[1]={result:$R[2]={rest_id:"555",
        details:$R[3]={full_text:"Public policy update"},
        created_at_ms:1789149425000}}
        '''
        posts = parse_profile_posts(
            profile,
            "realDonaldTrump",
            "25073877",
            "Donald J. Trump",
        )
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["id"], "555")
        self.assertEqual(posts[0]["createdAtISO"], "2026-09-11T17:57:05Z")
        self.assertEqual(posts[0]["text"], "Public policy update")


if __name__ == "__main__":
    unittest.main()

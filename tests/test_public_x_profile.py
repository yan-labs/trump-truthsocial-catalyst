import base64
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

    def test_binds_target_tweet_instead_of_adjacent_quoted_tweet(self):
        user_id = "25073877"
        target_id = "666"
        quoted_id = "777"
        target_token = base64.b64encode(f"Tweet:{target_id}".encode()).decode()
        quoted_token = base64.b64encode(f"Tweet:{quoted_id}".encode()).decode()
        user_ref = base64.b64encode(f"UserResults:{user_id}".encode()).decode()

        def rsc(key, number, body):
            return f'"{key}":$R[{number}]={{{body}}},'

        profile = (
            f'<a href="/realDonaldTrump/status/{target_id}"></a>'
            + rsc(f"TweetResults:{target_id}", 1, f'result:$R[2]={{__ref:"{target_token}"}}')
            + rsc(
                target_token,
                3,
                f'__typename:"Tweet",rest_id:"{target_id}",core:$R[4]={{__ref:"client:{target_token}:core"}},'
                f'legacy:$R[5]={{__ref:"client:{target_token}:legacy"}},details:$R[6]={{__ref:"client:{target_token}:details"}},'
                f'counts:$R[7]={{__ref:"client:{target_token}:counts"}},views:$R[8]={{__ref:"client:{target_token}:views"}},'
                f'quoted_tweet_results:$R[9]={{__ref:"TweetResults:{quoted_id}"}},reply_to_results:null,note_tweet:null',
            )
            + rsc(f"client:{target_token}:core", 10, f'user_results:$R[11]={{__ref:"{user_ref}"}}')
            + rsc(f"client:{target_token}:legacy", 12, '__typename:"LegacyTweet",lang:"en",retweeted_status_results:null')
            + rsc(f"client:{target_token}:details", 13, 'full_text:"Target-authored text",created_at_ms:1789305790000')
            + rsc(f"client:{target_token}:counts", 14, 'favorite_count:4,retweet_count:1,reply_count:2,quote_count:0,bookmark_count:3')
            + rsc(f"client:{target_token}:views", 15, 'count:"99"')
            + rsc(f"TweetResults:{quoted_id}", 16, f'result:$R[17]={{__ref:"{quoted_token}"}}')
            + rsc(quoted_token, 18, f'rest_id:"{quoted_id}",details:$R[19]={{full_text:"WRONG QUOTED TEXT",created_at_ms:1789306606000}}')
        )
        posts = parse_profile_posts(profile, "realDonaldTrump", user_id, "Donald J. Trump")
        self.assertEqual([post["id"] for post in posts], [target_id])
        self.assertEqual(posts[0]["text"], "Target-authored text")

    def test_prefers_full_note_tweet_text_over_truncated_details(self):
        user_id = "25073877"
        status_id = "888"
        token = base64.b64encode(f"Tweet:{status_id}".encode()).decode()
        user_ref = base64.b64encode(f"UserResults:{user_id}".encode()).decode()
        note_data_key = f"client:{token}:note_tweet"
        note_results_key = "NoteTweetResults:888"
        note_object_key = "NoteTweet:888"

        def rsc(key, number, body):
            return f'"{key}":$R[{number}]={{{body}}},'

        full_text = "Full NoteTweet text with policy details beyond the excerpt."
        profile = (
            f'<a href="/realDonaldTrump/status/{status_id}"></a>'
            + rsc(f"TweetResults:{status_id}", 1, f'result:$R[2]={{__ref:"{token}"}}')
            + rsc(token, 3, f'core:$R[4]={{__ref:"client:{token}:core"}},details:$R[5]={{__ref:"client:{token}:details"}},note_tweet:$R[6]={{__ref:"{note_data_key}"}},legacy:null,counts:null,views:null,quoted_tweet_results:null,reply_to_results:null')
            + rsc(f"client:{token}:core", 7, f'user_results:$R[8]={{__ref:"{user_ref}"}}')
            + rsc(f"client:{token}:details", 9, 'full_text:"Truncated NoteTweet excerpt",created_at_ms:1789330276000')
            + rsc(note_data_key, 10, f'note_tweet_results:$R[11]={{__ref:"{note_results_key}"}}')
            + rsc(note_results_key, 12, f'result:$R[13]={{__ref:"{note_object_key}"}}')
            + rsc(note_object_key, 14, f'text:"{full_text}"')
        )
        posts = parse_profile_posts(profile, "realDonaldTrump", user_id, "Donald J. Trump")
        self.assertEqual(posts[0]["text"], full_text)

    def test_skips_profile_tweet_when_author_reference_does_not_match(self):
        requested_user_id = "25073877"
        status_id = "889"
        token = base64.b64encode(f"Tweet:{status_id}".encode()).decode()
        wrong_user_ref = base64.b64encode("UserResults:1227552975561863169".encode()).decode()

        def rsc(key, number, body):
            return f'"{key}":$R[{number}]={{{body}}},'

        profile = (
            f'<a href="/realDonaldTrump/status/{status_id}"></a>'
            + rsc(f"TweetResults:{status_id}", 1, f'result:$R[2]={{__ref:"{token}"}}')
            + rsc(token, 3, f'core:$R[4]={{__ref:"client:{token}:core"}},details:$R[5]={{__ref:"client:{token}:details"}}')
            + rsc(f"client:{token}:core", 6, f'user_results:$R[7]={{__ref:"{wrong_user_ref}"}}')
            + rsc(f"client:{token}:details", 8, 'full_text:"Wrong author",created_at_ms:1789305790000')
        )
        self.assertEqual(parse_profile_posts(profile, "realDonaldTrump", requested_user_id, "Donald J. Trump"), [])


if __name__ == "__main__":
    unittest.main()

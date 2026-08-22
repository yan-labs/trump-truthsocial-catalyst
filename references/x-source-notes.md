# @realDonaldTrump X source notes

## Purpose

Use this file to preserve source-specific observations for Donald Trump's X
account, `https://x.com/realdonaldtrump`, without overloading the main
prediction ledger.

X is an official public Trump channel, but it behaves differently from Truth
Social:

- lower-frequency than Truth Social in the current setup;
- often video-only, short-link, or repost-heavy;
- high engagement can amplify a message, but engagement alone is not a market
  signal;
- context must be resolved before a video/link-only post is scored;
- cross-posted Truth Social/X messages should be logged once in
  `track-record.md`, with the mirror source noted.

## Initial maintenance rule

For every scheduled run:

1. Fetch latest X posts with `python3 scripts/fetch_x.py --state
   data/sync_state.json > /tmp/trump_x.json`. The wrapper tries the direct
   xreach timeline first, then RSS-Bridge's public Atom timeline, and then
   Jina's public profile plus exact status page when the direct response is old
   or unavailable.
2. Normalize each candidate as `x:<tweet_id>`.
3. Cross-dedupe against Truth Social ledger rows using source id, normalized
   text, media/link context, and a 24-hour window.
4. Append to the market ledger only when the X item has verified context and a
   tradable market read.
5. Keep video/link-only or retweet items here as source notes unless the market
   context is independently verified.

## Direct connector fallback

The direct `xreach`/bird connector can return HTTP-successful JSON whose newest
item is several weeks old. Do not call that current data. `fetch_x.py` uses an
independent RSS-Bridge timeline and the exact Jina status page as bounded public
fallbacks. FxTwitter/VxTwitter are used only to verify the saved status when
the public timeline views are blocked:

- `available`: direct xreach has a post newer than the saved observation;
- `available_fallback`: RSS-Bridge or Jina verified a newer visible top status;
- `verified_no_new_posts`: Jina verified that the visible top status is the
  same post and timestamp as the saved observation;
- `stale_unverified` with `freshness: exact_status_only`: FxTwitter/VxTwitter
  verified the saved id and timestamp, but no current timeline was established;
- `stale_unverified`: no public path established freshness.

None of these fallbacks is a full timeline archive. RSS-Bridge is a useful
second subscription channel, but it must still be freshness-checked; an old
RSS response is not proof that X has no newer posts. Keep
`direct_status: stale_unverified` in sync state when a fallback is used and
never advance `last_tweet_id` from an old direct response or an
exact-status-only result.

When an authenticated browser profile visibly shows the same top status, it may
be recorded as `verification_source: chrome_profile_ui` with
`status: verified_no_new_posts`. This is a manual evidence checkpoint for the
next unattended retry, not a reason to store browser cookies or depend on the
browser for scheduled fetching.

## Historical X seed candidates

The historical seed table is intentionally compact. It is for candidates that
may be worth adding to `track-record.md` or citing as source-behavior examples.

Initial partial backfill, captured with `xreach tweets @realdonaldtrump --json
--count 100 --all --max-pages 12 --delay 1200`:

- Captured 240 X timeline items.
- Coverage was incomplete (`complete: false`).
- Range: 2024-11-06 00:08:02 UTC through 2026-05-22 23:34:07 UTC.
- Shape: 22 retweets, 9 quote posts, 0 replies, 138 media posts, 68 videos,
  72 images, 174 posts containing `t.co`, and 114 posts whose visible text was
  only a short link. Many video/link-only posts are context-unverified.

| source_id | UTC time | link | summary/context | market relevance | covered by ledger? | suggested action |
|---|---|---|---|---|---|---|
| `x:1899636898533867969` | 2025-03-12 01:41:44 | https://x.com/realDonaldTrump/status/1899636898533867969 | Praised Tesla products and said Elon Musk was being treated unfairly. | Tier 1 named-company praise; TSLA. | Not found in current Truth Social ledger. | Backfill candidate for `track-record.md` after price scoring. |
| `x:1899637674241048800` | 2025-03-12 01:44:49 | https://x.com/realDonaldTrump/status/1899637674241048800 | Quoted Musk/Tesla production-doubling claim; attached video context remains unverified. | Tier 1/Tier 2 named-company + US manufacturing; TSLA / EV / US manufacturing. | Not found in current Truth Social ledger. | Backfill candidate, but mark video context-unverified unless resolved. |
| `x:1891572283161944433` | 2025-02-17 19:35:50 | https://x.com/realDonaldTrump/status/1891572283161944433 | Announced reciprocal-tariff policy framework. | Tier 2B tariff/trade; steel/aluminum, industrials, autos, import-heavy retailers, AAPL/electronics. | Theme partly covered by seeded tariff priors, but this X id is not covered. | Backfill candidate for `track-record.md` after basket scoring. |
| `x:1909258777380974625` | 2025-04-07 14:55:39 | https://x.com/realDonaldTrump/status/1909258777380974625 | Claimed oil, rates, and food prices were down; pushed Fed cuts; emphasized tariff revenue. | Tier 3 macro + tariff; SPY/IWM, TLT, USD, energy, tariff beneficiaries. | Not found in current Truth Social ledger. | Source note unless later scored. |
| `x:1925548216243703820` | 2025-05-22 13:44:04 | https://x.com/realDonaldTrump/status/1925548216243703820 | Said the "One Big Beautiful Bill" passed the House and highlighted large tax cuts. | Tier 2 fiscal policy; SPY/IWM, consumer, energy, tax-sensitive sectors. | Not found in current Truth Social ledger. | Source note unless later scored. |
| `x:1876089056817455175` | 2025-01-06 02:11:01 | https://x.com/realDonaldTrump/status/1876089056817455175 | Congressional bill framing: border, US energy, and extension of Trump tax cuts. | Tier 2 fiscal/energy policy; energy, industrials, small caps. | Not found in current Truth Social ledger. | Source note. |
| `x:1875049777186136481` | 2025-01-03 05:21:18 | https://x.com/realDonaldTrump/status/1875049777186136481 | Argued tariffs would pay debt and make America wealthy. | Tier 2B tariff theme seed; tariff beneficiaries/importers. | Theme partly covered by seeded tariff priors. | Source note. |
| `x:1863009545858998512` | 2024-11-30 23:57:43 | https://x.com/realDonaldTrump/status/1863009545858998512 | Warned BRICS not to replace the dollar or face tariffs/restrictions; text capture was truncated. | Tier 3 FX/geopolitical/tariff; USD, gold, EM, China/BRICS, tariffs. | Not found in current Truth Social ledger. | Source note; mark text-truncated. |
| `x:1857170020427595797` | 2024-11-14 21:13:32 | https://x.com/realDonaldTrump/status/1857170020427595797 | Announced RFK Jr. for HHS and criticized drug companies / industrial food complex; single-post fetch failed but timeline text identified theme. | Tier 2 healthcare/regulatory; LLY/NVO/PFE/MRK/JNJ, food/agriculture. | Related to later TrumpRx/MFN healthcare ledger theme, but not this source. | Source note; verify full text before scoring. |
| `x:1880672600894173506` | 2025-01-18 17:44:23 | https://x.com/realDonaldTrump/status/1880672600894173506 | Retweeted Eric Trump referencing `$Trump` meme/crypto. | Tier 2C crypto/self-promo; TRUMP memecoin, COIN/MSTR/HOOD/crypto beta. | Seeded memecoin trap covers theme, but X id is not covered. | Source note; self-promo trap evidence, not a high-confidence fresh signal. |
| `x:1881089112771572032` | 2025-01-19 21:19:28 | https://x.com/realDonaldTrump/status/1881089112771572032 | Retweeted Melania Trump promoting `$MELANIA` meme. | Tier 2C crypto/self-promo; MELANIA memecoin. | Seeded `$MELANIA` trap covers theme. | Source note; do not add new ledger row unless backtesting memecoin pattern. |
| `x:1994760100376891748` | 2025-11-29 13:27:23 | https://x.com/realDonaldTrump/status/1994760100376891748 | Declared Venezuela airspace closed. | Tier 3 geopolitical/transport/oil risk; airlines, oil, defense, Latin America risk. | Not found in current Truth Social ledger. | Source note unless later price-verified. |
| TIMER_X_SEED_START |  |  |  |  |  |  |

## Context-unverified / skip examples

| source_id | Reason |
|---|---|
| `x:2073607119878623432` | Newest X item in this run was visible only as a `t.co` short link. No text, media caption, or independently verified market context was available, so it was not scored. |
| `x:2057968277062582378` | Latest captured X post was visible text `t.co` plus video media. Content was not resolved, so do not score. |
| `x:2028505632123326484` | Visible text only a short link plus video media. Market context unverified. |
| GOTV / campaign endorsements / personal attacks | No clear ticker, sector, or policy lever. Usually outside this skill's market ledger. |
| Pure short-link or pure video posts | Keep as source notes unless a reliable transcript, expanded link, or independent summary verifies market context. |

## Maintenance recommendation from partial backfill

X is useful as a supplemental official channel and historical backfill source,
but it should not displace Truth Social as the main feed. The timeline capture
was incomplete and many posts were video/link-only.

- Fetch X on scheduled runs, but process only new `x:<tweet_id>` candidates and
  skip quickly when the latest id has not changed.
- Candidate keywords: named company, explicit buy/praise, tariff, crypto,
  energy, healthcare, Fed/rates, shipping/oil, geopolitical closure/blockade,
  and large fiscal/tax bills.
- Treat retweets and quote posts as lower-confidence unless Trump adds original
  market-relevant commentary.
- Use X backfill mainly to seed 2024-2025 patterns, cross-check Truth Social,
  and capture rare X-only named-company posts.

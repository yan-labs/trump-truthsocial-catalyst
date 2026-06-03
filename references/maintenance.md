# Maintenance playbook (for the periodic timer)

This skill is meant to be run on a schedule (like the serenity skill) so the
`track-record.md` ledger accumulates a real, measured hit-rate. Keep each run
cheap and append-only; don't rewrite history.

## Each scheduled run

1. **Fetch** the latest posts (Step 0):
   ```bash
   curl -sS -A "Mozilla/5.0" "https://trumpstruth.org/feed" -o /tmp/trump_feed.xml
   xreach tweets @realdonaldtrump -n 40 --json > /tmp/trump_x.json
   ```
   Parse with the recipes in `methodology.md`. Truth Social is the main high-
   frequency text source; X is an official supplemental public channel and may be
   sparse, video-heavy, or repost-heavy. Process only new `x:<tweet_id>`
   candidates; if the latest X id has not changed, skip X classification quickly.

2. **Dedupe by source id** against the live ledger in `track-record.md`: use
   `truth:<status_id>` for Truth Social and `x:<tweet_id>` for X. Also cross-
   dedupe by normalized text or media title within a 24-hour window so a cross-
   posted message is not logged twice. Prefer the source with the clearest text;
   if both are equivalent, prefer Truth Social for continuity with the existing
   ledger and mention the X mirror in notes.

3. **Classify** each new post with the `methodology.md` checklist. `skip` anything
   not market-relevant (most of both feeds). Don't log skips except as a count.
   For X video/link-only posts, resolve the media/article/context before scoring;
   if context cannot be verified, store only a skip/count note in
   `x-source-notes.md` and do not append a prediction row.

4. **Log a prediction** for each market-relevant post: append a row to the live
   ledger (newest first, above the TIMER marker) with source id, date, source
   link, short text/context, tier + amplifiers, implicated ticker(s), and
   predicted direction / magnitude / durability. Leave T+1d / T+1w blank.

5. **Score matured predictions.** For rows whose post is now ≥1 trading day (and
   ≥1 week) old, fill in the actual move of the implicated ticker (use the
   project's market-data tools or a quick quote lookup) and mark hit/miss.
   - "hit" = predicted direction realized over the stated horizon.
   - Note separately whether a Tier-2 pop *held* a week or faded (durability is
     the thing we most need to learn).

6. **Recompute the rolling hit-rate** table and update the calibration takeaways
   if a pattern's measured rate clearly diverges from the seed prior.

## What earns a durable note vs. a one-off

Promote into the calibration takeaways only when it changes how we'd weight a
pattern — e.g., "Tier 2C crypto posts hit direction 8/10 but held only 1/10",
"named-company praise on a name he owns held 5/6". Don't editorialize single
posts; let the counts talk.

## X backfill queue

Use `x-source-notes.md` for historical X candidates. Do not bulk append old X
items to the live ledger without scoring them. When backfilling:

1. Start with the three strongest candidates marked `Backfill candidate`.
2. Verify full text/media context.
3. Score T+1d and T+1w before inserting into `track-record.md`.
4. Preserve `x:<tweet_id>` as the source id and note any Truth Social mirror.

## Hygiene

- Append-only ledger; never delete scored rows (the misses are the most valuable
  calibration data).
- Keep provenance compact: source id + date + permalink, not full post text.
- If `trumpstruth.org` is down, continue with X if available and say the Truth
  source failed. If X/xreach fails, continue with Truth Social and say X failed.
  If both fail, skip the run and retry next tick.
- Holdings change: refresh `holdings-watchlist.md` only when a *new* OGE
  disclosure drops (roughly periodic), not every run. Use the official OGE
  Officials' Individual Disclosures Search Collection first:
  `https://www.oge.gov/web/oge.nsf/Officials%20Individual%20Disclosures%20Search%20Collection?OpenForm`.
  Its DataTables endpoint is
  `https://extapps2.oge.gov/201/Presiden.nsf/API.xsp/v2/rest`; filter the
  `name` column with `Trump`, sort `docDate` descending, then download direct
  PDF links from `278 Transaction` rows for `Trump, Donald J`.
- OGE 278-T forms disclose transaction ranges, not exact current holdings. When
  refreshing the watchlist, keep purchases, sales, bonds, ETFs, and family/private
  assets separate; never infer current position size from a transaction row.

## Commit convention (if vendored into a repo like serenity)

- `data: trump catalyst ledger update (+<n> posts) <UTC ISO>` for ledger-only runs.
- `skill: trump catalyst calibration update <UTC ISO>` when takeaways/hit-rates
  change.
- Don't create empty commits.

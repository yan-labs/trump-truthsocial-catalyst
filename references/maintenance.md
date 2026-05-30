# Maintenance playbook (for the periodic timer)

This skill is meant to be run on a schedule (like the serenity skill) so the
`track-record.md` ledger accumulates a real, measured hit-rate. Keep each run
cheap and append-only; don't rewrite history.

## Each scheduled run

1. **Fetch** the latest posts (Step 0):
   ```bash
   curl -sS -A "Mozilla/5.0" "https://trumpstruth.org/feed" -o /tmp/trump_feed.xml
   ```
   Parse with the recipe in `methodology.md`. The feed is a rolling ~5-day window,
   so a run more often than every few days will see overlap — that's fine.

2. **Dedupe by `status_id`** against the live ledger in `track-record.md`. Only
   process posts not already logged.

3. **Classify** each new post with the `methodology.md` checklist. `skip` anything
   not market-relevant (most of the feed). Don't log skips except as a count.

4. **Log a prediction** for each market-relevant post: append a row to the live
   ledger (newest first, above the TIMER marker) with status_id, date, short text,
   tier + amplifiers, implicated ticker(s), and predicted direction / magnitude /
   durability. Leave T+1d / T+1w blank.

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

## Hygiene

- Append-only ledger; never delete scored rows (the misses are the most valuable
  calibration data).
- Keep provenance compact: status_id + date + permalink, not full post text.
- If `trumpstruth.org` is down, skip the run (don't log empty); retry next tick.
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

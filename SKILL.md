---
name: trump-truthsocial-catalyst
description: >
  Decision-support lens for reading Donald Trump's Truth Social posts,
  @realDonaldTrump X posts, public statements, and disclosed personal holdings
  as short-term US-stock catalysts — which names or sectors are likely to pop,
  and how reliably. Use this skill whenever the user asks what a Trump post /
  statement means for a stock, mentions "特朗普", "Trump post", "Truth Social",
  "@realDonaldTrump", "POTUS", a Trump endorsement/attack of a company, a tariff
  / crypto / energy / AI-infra / defense policy signal from Trump, or wants to
  know which stocks Trump owns or might pump next. Also trigger when evaluating
  a buy/sell around a Trump headline or building a Trump-catalyst watchlist.
  Live-fetches the latest public posts first (no local archive).
  Decision-support only — never auto-trades and never places or cancels orders.
---

# Trump Truth Social Catalyst Lens

A reusable lens for turning **Donald Trump's public Truth Social posts**,
**@realDonaldTrump X posts**, and **his own disclosed stock holdings** into a
short list of US stocks/sectors likely to move, with an honest read on *how
reliably* each pattern actually pumps a stock. Built to be paired with a periodic
timer that re-fetches and re-scores, accumulating a real hit-rate over time.

> **Decision-support lens, NOT financial advice and NOT an auto-trader.** This
> only *analyzes publicly available posts and public financial disclosures* to
> anticipate market reactions. It never places, cancels, or sizes orders. Always
> confirm current price/news yourself — these moves are fast, often fade, and
> several are pump-and-fade traps (see `references/track-record.md`).

---

## STEP 0 — ALWAYS REFRESH FIRST (this skill is useless on stale data)

Two things go stale: the **skill itself** (the ledger / holdings / calibration in
`references/` are grown by a periodic timer and pushed to GitHub) and the **posts**
(Trump posts many times a day; a market-moving one can be minutes old, and there
is **no local post archive**). Refresh both, in order, before doing anything else:

```bash
# 0a. Pull the latest version of this skill (updated ledger, holdings, calibration).
#     Best-effort: auto-detects project vs global scope. If it fails, keep going.
skills update trump-truthsocial-catalyst -y

# 0b. Fetch the latest Truth Social posts: text + timestamps + permalinks.
#     trumpstruth.org is a third-party archive; the official truthsocial.com API is
#     Cloudflare-blocked from servers, so use this RSS.
curl -sS -A "Mozilla/5.0" "https://trumpstruth.org/feed" -o /tmp/trump_feed.xml

# 0c. Fetch the latest @realDonaldTrump X posts when xreach is available.
#     X is a supplemental official public channel; many posts are video/link-only,
#     so resolve context before scoring.
xreach tweets @realdonaldtrump -n 40 --json > /tmp/trump_x.json
```

Then **re-read the refreshed `references/*.md`** (don't rely on a copy you read
before 0a) and parse the newest posts (see `references/methodology.md` for ready
parsers). If 0a fails, proceed on the cached skill but note it may be stale; if a
source fails (offline / 403 / site down), say so explicitly and use the other
source plus whatever the user pasted — never pretend you have fresh data.

---

## What this lens is for

Trump's posts move stocks through a few repeatable mechanisms: he **names a
company favorably**, **announces or hints at policy he controls** (tariffs,
contracts, executive orders), or **champions a theme** (crypto, energy, AI
infrastructure, defense, reshoring). The edge is recognizing *which* features of
a post reliably pump a stock versus which produce a one-day spike that fades —
and cross-referencing against **what he personally owns**, because "he owns it →
he boosts it → a government tailwind follows" is his single most repeatable
money-making pattern (the Dell playbook).

This is explicitly a *short-horizon catalyst* lens, not a fundamentals lens. The
biggest caveat in the whole skill: **his posts can pump a stock that is a
terrible long-term hold** — his own DJT is down ~77% from its 2024 high and his
memecoins are down 97–99%, yet they still spike when he posts. Separate "will it
pop this week" from "is it a good investment."

---

## How the reference files are organized

Read progressively — pull in only what the task needs.

| File | What it is | Read it when |
|---|---|---|
| `references/methodology.md` | The tiered "what reliably pumps a stock" playbook: Tier 1–3 patterns, amplifier features, anti-patterns, durability, a per-post classification checklist, and Truth Social / X fetch-parse recipes | Classifying any post, or judging how strong a signal is |
| `references/theme-ticker-map.md` | Trump's recurring themes → the tickers/sectors that typically react | Mapping a topic (tariffs, crypto, energy, AI infra, defense…) to tradable names |
| `references/holdings-watchlist.md` | Companies Trump's trust disclosed buying in 2026 + his personal/family holdings, flagged for "not-yet-popped" breakout potential; includes the official OGE search/API source for updates | Building a watchlist, or asking "what does he own / what might pop next" |
| `references/track-record.md` | The accumulating hit-rate ledger (seeded with documented wins and failures) + a calibration note on what actually has edge | Deciding *how much to weight* a given pattern; this is what the timer grows |
| `references/x-source-notes.md` | @realDonaldTrump X source behavior, cross-source dedupe notes, and historical X seed candidates | When using or maintaining the X source |
| `references/maintenance.md` | Rules for the periodic timer: fetch → dedupe → classify → log prediction → score outcome → recalibrate | Running or wiring up the scheduled refresh |

---

## Workflows

### (a) Read one post (or a batch) for tradable signals

1. **Refresh** (Step 0). Identify the newest Truth Social and X posts; dedupe
   against anything already in `references/track-record.md` by source id and
   cross-source normalized text/time.
2. For each post, run the **classification checklist** in
   `references/methodology.md`: is it market-relevant? Which Tier (1 named-stock /
   2 policy-sector / 3 macro)? Which amplifier features are present (named public
   company, explicit "BUY", policy he controls, he personally owns it, posted
   intraday, repeated)?
3. Map topic → candidate tickers via `references/theme-ticker-map.md`, and check
   `references/holdings-watchlist.md` for an ownership overlap (raises conviction).
4. Output, per signal: the post (date + permalink), the implicated ticker(s),
   **direction**, a **reliability tier**, expected **magnitude & durability**
   (intraday-fade vs. can-hold), and what would invalidate it.
5. Weight using `references/track-record.md` — favor patterns with a real
   accumulated hit-rate over plausible-sounding one-offs. Always frame as
   analysis, never as an order.

### (b) Build / refresh a Trump-catalyst watchlist

1. Pull his disclosed holdings from `references/holdings-watchlist.md`. If the
   question depends on freshness, check the OGE source listed there for newer
   `Trump, Donald J` 278-T PDFs before treating the watchlist as current.
2. Bucket: **already popped** (Dell-style, catalyst spent) vs. **owns-but-quiet**
   (breakout candidates if the Dell template repeats: ownership + an admin
   tailwind like a contract, tariff carve-out, or public praise).
3. For each quiet name, note the *specific* catalyst that would trigger it and a
   rough 1–2 month watch window. Keep it advisory.

### (c) Judge a single "will this pump X?" question

1. Refresh, find the relevant post(s).
2. Score the pattern against `references/methodology.md` tiers + amplifiers and
   the historical analogs in `references/track-record.md`.
3. Give a calibrated answer: likely direction, reliability, magnitude,
   durability, and the honest base-rate (e.g., "named-company endorsements pop
   reliably intraday; crypto-reserve posts spike then fade next day").

---

## Risk & disclaimer framing (state this when giving any view)

- **Short-horizon catalyst, not a thesis.** A pop is not a reason to hold. His
  own assets (DJT, $TRUMP, $MELANIA) show posts can pump structurally weak names.
- **Many signals fade fast.** Crypto-reserve and tariff-relief posts often spike
  for a day and give it back; size and timing matter, and this skill does not set
  either — the user does.
- **Conflict-of-interest is a feature of the data, not an endorsement.** He has
  bought stocks (Dell, Palantir, Nvidia, media names) that his administration
  then affected. We note the overlap as a *signal*, while flagging the obvious
  manipulation/legal scrutiny around it. Do not act illegally on it.
- **Disclosures are ranges and self-reported.** Holding figures come from OGE
  periodic transaction reports (dollar *ranges*, not exact amounts) and may lag.
- **This is a lens, not a signal feed.** It surfaces better questions about a
  Trump headline. It is NOT auto-trading, NOT a recommendation, NOT financial
  advice. Every order is the reader's own manual, confirmed decision.

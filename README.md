```bash
npx skills add yan-labs/trump-truthsocial-catalyst
```

<p align="center"><img src="assets/trump.jpg" alt="Donald Trump" width="140" height="140"></p>

# trump-truthsocial-catalyst

[![skills.sh](https://skills.sh/b/yan-labs/trump-truthsocial-catalyst)](https://skills.sh/yan-labs/trump-truthsocial-catalyst)

A **decision-support lens** that reads **Donald Trump's latest Truth Social
posts** — together with **his disclosed personal/family stock holdings** — as
short-term US-stock catalysts: which names or sectors are likely to pop, and an
honest read on *how reliably* each pattern actually does.

It **live-fetches the newest posts on every use** (via the public
[trumpstruth.org](https://trumpstruth.org) RSS feed, because the official
`truthsocial.com` API is Cloudflare-blocked from servers). There is **no local
post archive** — the skill refreshes fresh each time so it never reasons on
stale data. It is built to be paired with a periodic timer that re-fetches,
re-scores, and accumulates a real, measured **hit-rate per pattern** over time.

The edge it cross-references: *he owns a stock → he praises it → an
administration tailwind (a contract, a tariff carve-out) follows → it pops* —
his single most repeatable pattern (the **Dell template**).

> ⚠️ **Not financial advice. Decision-support only.** This skill never trades and
> never places, cancels, or sizes orders. A Trump-driven pop is a *short-horizon
> trade setup, NOT a reason to hold*: his own DJT is down ~77% from its 2024 high
> and his memecoins ($TRUMP / $MELANIA) are down 97–99% from peak, yet they still
> spike when he posts. Conflict-of-interest overlaps (stocks he owns that his
> administration then affects) are surfaced as a **signal**, with the obvious
> manipulation/legal scrutiny flagged — never as an endorsement to act illegally.
> Holdings come from self-reported OGE disclosures (dollar *ranges*, may lag).
> Always confirm current price/news yourself.

## What's in here

| Path | What it is |
|---|---|
| `SKILL.md` | The agent skill: the live-fetch Step 0, what the lens is for, how the references are organized, the three workflows, and the risk framing |
| `references/methodology.md` | The tiered "what reliably pumps a stock" playbook: Tier 1–3 patterns, amplifier features, anti-patterns, durability, a per-post classification checklist, and the RSS fetch/parse recipe |
| `references/theme-ticker-map.md` | Trump's recurring themes (crypto, AI infra, tariffs, energy, defense, reshoring, pharma, media, financials) → the tickers/sectors that typically react |
| `references/holdings-watchlist.md` | Stocks his trust/family disclosed buying in 2026 + personal holdings, the official OGE disclosure source for updates, and "catalyst spent" vs. "owns-but-quiet" breakout buckets |
| `references/track-record.md` | The accumulating hit-rate ledger — seeded documented wins/failures plus the live ledger the timer appends to and later scores |
| `references/maintenance.md` | Rules for the periodic timer: fetch → dedupe → classify → log prediction → score outcome → recalibrate |

## How it works

**Step 0 — always refresh first.** Trump posts many times a day and a
market-moving one can be minutes old, so the skill fetches live before doing
anything else:

```bash
curl -sS -A "Mozilla/5.0" "https://trumpstruth.org/feed" -o /tmp/trump_feed.xml
```

It parses the newest items (clean text + timestamps + permalinks), dedupes by
`status_id`, and runs each market-relevant post through a classification
checklist. Posts are sorted into a tiered pump playbook, ranked by reliability of
an immediate up-move and annotated for durability:

- **Tier 1 — names a specific company** (most reliable). Direct favorable mention
  or an explicit all-caps "BUY". Pops immediately and **can hold** when a real
  catalyst (a government contract, earnings) follows.
- **Tier 2 — policy / crypto / tariff announcements** (strong pop, mixed
  durability). Mega-investment headlines, tariff exemptions/pauses, pro-crypto
  reserve posts — reliable *direction* for a fast trade, but **often fade the next
  day**.
- **Tier 3 — macro themes** (directional, not a single name). "Drill baby drill,"
  Fed-cut pressure, defense, reshoring — these shift a whole basket, weaker and
  slower.

Amplifier features stack the odds — a named public company, a superlative + call
to action, a policy he controls, **personal ownership** (the Dell template),
intraday timing, and repetition. Each call is weighted against the historical
base-rate in the track-record ledger, then framed as analysis — never as an
order.

## Install

One-command install with [skills.sh](https://skills.sh/):

```bash
npx skills add yan-labs/trump-truthsocial-catalyst
```

Because the skill is most useful on fresh data — and is designed to grow a real
hit-rate via a periodic timer — refresh it regularly:

```bash
skills update trump-truthsocial-catalyst -y
```

---

*This repository contains only public information: Trump's public Truth Social
posts and self-reported public financial disclosures, plus derived analysis. It
is an independent research artifact and is not affiliated with, endorsed by, or
connected to Donald Trump, Truth Social, or trumpstruth.org. The portrait is the
official 2025 White House presidential portrait, a U.S. federal government work in
the public domain.*

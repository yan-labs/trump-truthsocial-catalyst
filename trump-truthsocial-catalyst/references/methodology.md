# Methodology — what reliably pumps a stock, and how to read a post

The goal is to separate Trump posts that **reliably push a stock up** from the
much larger pile of posts that don't move markets or that produce a spike which
fades. Patterns are ranked by *reliability of an immediate up-move*, with an
honest note on **durability** (does the pop hold, or is it a one-day trap).

All magnitudes are from documented cases (see `track-record.md` for sources).
Treat them as rough bands, not guarantees — and remember a pop is a *trade
setup*, not a fundamental endorsement.

---

## Tier 1 — Names a specific stock (most reliable, immediate, single-name)

**1A. Direct favorable mention of a specific public company.**
He names a company and praises it / tells people to buy / thanks the founders.
- *Mechanism:* retail + momentum front-run, and it often signals a coming policy
  tailwind (contract, carve-out).
- *Magnitude / durability:* **+5–15% intraday**; **can hold** if a real catalyst
  follows (a government contract, earnings), otherwise partial fade.
- *Canonical case:* **Dell, 2026-05-08** — White House "go out and buy" → +~14.6%
  intraday to an all-time high; weeks later a $9.7B Pentagon contract. He had also
  *personally bought* Dell in Q1. This is the template the whole skill watches for.
- *Signal words:* a company/ticker + `great / tremendous / fantastic / the best`
  + `buy / support / go out and`.

**1B. Explicit all-caps "BUY" call (especially his own DJT or a clear ticker).**
- *Magnitude:* **+15–25%+ intraday**; strongest when it's a stock he controls or
  precedes a policy action he controls.
- *Canonical case:* **"THIS IS A GREAT TIME TO BUY!!! DJT"** → DJT +22.67% on the
  day, and ~4 hours later he announced a 90-day tariff pause → S&P +9.5%.
- *Caveat:* draws explicit market-manipulation scrutiny. Durability is poor for
  the named stock itself (DJT round-tripped); the *broad-market* leg held that day
  only because real policy followed.

> Tier 1 is the "几乎确定会拉" bucket — but "pumps reliably" ≠ "good to hold."

---

## Tier 2 — Policy / big-investment announcements (strong sector pop, mixed durability)

**2A. White-House mega-investment announcement that names partner companies.**
- *Case:* **Stargate, 2025-01-21** — "largest AI infrastructure project in
  history, $500B," on stage with Oracle/SoftBank/OpenAI → **ORCL + AI
  datacenter / power names** rallied; theme persisted for weeks.
- *Signal words:* `$X billion`, `largest … in history`, named CEOs/companies.
- *Durability:* medium — the *theme* outlives the day even when the headline name
  cools.

**2B. Tariff exemption / pause / relief for a named sector.**
- *Case:* **2025-04-14 electronics exemption** → AAPL +2.2%, DELL +4%; floated
  auto-tariff pause → GM +3.5%, Ford +4.1%; broad relief rally.
- *Durability:* **fragile** — officials frequently walk it back ("temporary"),
  so it can round-trip within days. Trade the reaction, distrust the follow-through.
- *Signal words:* `exempt / exemption / pause / relief / carve-out` + sector.

**2C. Pro-crypto policy (strategic reserve, naming coins, anti-"Anti-Crypto Army").**
- *Case:* **2025-03-02 strategic-reserve posts** naming BTC/ETH/XRP/SOL/ADA → all
  spiked Sunday, **gave it back Monday**. Drags COIN / MSTR / miners with it.
- *Durability:* **lowest — typically a one-day spike.** Good for a fast reaction
  trade, dangerous to chase.

---

## Tier 3 — Macro / thematic tailwinds (directional, not a single name)

These shift a whole basket rather than pumping one ticker; weaker and slower.
- **"Drill baby drill" / energy dominance** → oil & gas, nuclear/uranium, power.
- **Pressuring the Fed to cut rates** → small-caps, gold, long-duration growth.
- **Defense / "peace through strength," or a conflict de-escalation** → defense
  primes, or broad risk-on.
- **Reshoring / "Made in America"** → domestic manufacturers, US steel, semis.

See `theme-ticker-map.md` for the specific names per theme.

---

## Amplifier features — the more that stack, the higher the hit-rate

Score each market-relevant post on these. Several together ≈ the "几乎确定" zone:
1. **Names a specific public company** (not a vague sector) → directly tradable.
2. **Superlative + call to action** (`great` + `go buy`).
3. **Precedes a policy action he controls** (tariff move, contract, EO) → can
   self-fulfill.
4. **He / his family personally owns it** (cross-check `holdings-watchlist.md`) →
   the Dell template; ownership + an admin tailwind is the strongest combo.
5. **Posted intraday or pre-open** → immediate spike (after-hours leaks to next day).
6. **Repeated / multi-post on the same name or theme** → conviction.

---

## Anti-patterns — do NOT read these as reliable up-signals

- **Pure geopolitics rants with no named beneficiary** (e.g., the steady stream of
  Iran/foreign-policy posts) → diffuse, unpredictable market impact.
- **Crypto-reserve / coin posts** → usually one-day spikes; don't chase late.
- **Tariff "relief" that gets walked back the same week** → false breakout.
- **Attacks on a company/industry** → these *dump*, not pump (opposite direction);
  treat as a short-side or avoid signal, not a buy.
- **His own promotional posts about DJT / memecoins** → may spike, but these are
  structurally value-destroying for holders (DJT −77% from 2024 high; $TRUMP −97%;
  $MELANIA −99%). Flag the trap.

---

## Per-post classification checklist

For each fresh post, answer in order — stop early if it's not market-relevant:

1. **Market-relevant?** Mentions a company/ticker, sector, tariff/trade, crypto,
   energy, the Fed/rates, defense, AI/infra, or a $-investment? If no → `skip`.
2. **Tier?** 1 (named stock) / 2 (policy-sector) / 3 (macro theme).
3. **Direction?** Favorable (pump) vs. attack (dump).
4. **Amplifiers present?** Count them (list above).
5. **Ownership overlap?** Cross-check `holdings-watchlist.md`.
6. **Implicated tickers** via `theme-ticker-map.md`.
7. **Reliability + durability call:** combine Tier + amplifiers + the historical
   base-rate in `track-record.md` → state likely magnitude and whether it can hold
   or is a fade.
8. **Log it** for the timer (see `maintenance.md`): id, date, classification,
   predicted direction/magnitude — so the outcome can be scored later.

---

## Fetch + parse recipe (Step 0)

```bash
curl -sS -A "Mozilla/5.0" "https://trumpstruth.org/feed" -o /tmp/trump_feed.xml
```

```python
# Newest-first list of recent posts: (utc, status_id, permalink, text)
import xml.etree.ElementTree as ET, html, re
items = ET.parse('/tmp/trump_feed.xml').getroot().find('channel').findall('item')
def clean(s): return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', s or ''))).strip()
posts = []
for it in items:
    link = it.findtext('link') or ''
    sid  = (re.search(r'/statuses/(\d+)', link) or [None, None])[1]
    posts.append((it.findtext('pubDate'), sid, link, clean(it.findtext('description'))))
# posts[0] is the most recent. Filter to market-relevant via the checklist above.
```

Notes:
- The feed is a rolling window (~100 posts / ~5 days), newest-first. For the timer,
  **dedupe by `status_id`** so each post is scored once.
- `RT:` items are reposts; resolve the linked status if it matters.
- The official `truthsocial.com` API is Cloudflare-blocked from servers. If you
  ever need full fields / deeper history, `truthbrush` (needs a Truth Social
  login) or a real browser (agent-browser) are the fallbacks — but for catalyst
  spotting this RSS is enough.

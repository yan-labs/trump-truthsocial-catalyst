# Trump holdings & breakout watchlist

What Trump (his trust) and his family disclosed owning, used as a catalyst
watchlist. The key pattern this enables: **he owns it → he praises it / a
favorable policy follows → it pops** (the Dell template). Names he owns that
have *not* yet had a dedicated catalyst are the "not-yet-popped" candidates.

> **Source & caveats.** Figures are from OGE periodic transaction reports and
> press coverage (2026). Disclosures report **dollar ranges, not exact amounts**,
> often don't say stock vs. bond, and can lag weeks. "Owns" = disclosed a
> transaction; he may have since sold. Self-reported, unverified. This is a
> conflict-of-interest map used as a *signal*, not an endorsement of acting on it.

## Authoritative OGE disclosure source

Use the U.S. Office of Government Ethics (OGE) **Officials' Individual
Disclosures Search Collection** as the primary source for new public Trump
financial-disclosure documents:

- Search page:
  `https://www.oge.gov/web/oge.nsf/Officials%20Individual%20Disclosures%20Search%20Collection?OpenForm`
- Backing DataTables endpoint:
  `https://extapps2.oge.gov/201/Presiden.nsf/API.xsp/v2/rest`
- Query pattern: send the same DataTables parameters used by the page, filter
  `columns[3][search][value]=Trump`, sort `docDate` descending, and look for
  rows where `name` is `Trump, Donald J` and `type` includes direct PDF links
  such as `278 Transaction`.
- Implementation note: include the six page columns (`docDate`, `title`, `type`,
  `name`, `agency`, `level`) and each column's `name`, `searchable`,
  `orderable`, `search[value]`, and `search[regex]` parameters. A bare endpoint
  call or global `search[value]=Trump` is not enough; the useful filter is the
  `name` column filter.
- Example verified latest 2026 result set: the 2026-05-14 rows link to
  `Trump, Donald J.-05.08.2026-278T.pdf` and
  `Trump, Donald J.-05.08.2026-278T(2).pdf`.

Treat OGE as an **official disclosure locator**, not a clean holdings API. The
PDFs are scanned/OCR'd forms; parse them carefully, preserve document dates and
PDF URLs, and record whether each line is a `purchase`, `sale`, or bond/other
instrument. Do not turn 278-T transaction ranges into exact position sizes or
current holdings without a later confirming disclosure.

## Scale check (correct the "$2B" myth)
- **Q1 2026 disclosed trades:** **3,600+ transactions**, cumulative value
  **~$220M–$750M** (range). He pivoted from mostly *bonds* (hundreds of millions,
  incl. ~$51M in March) toward **hundreds of individual stocks**.
- The **"~$2 billion"** figure people remember is **Trump Media's (DJT) ~$2B
  Bitcoin / BTC-securities treasury**, *not* his personal stock buying. Different
  thing.
- **Net worth** ~$6.3–6.6B (Forbes 2026), roughly doubled since 2024 — driven by
  crypto + Trump Media paper gains, not his stock trades.

## Disclosed 2026 stock buys (the watchlist)
Grouped by how "spent" the catalyst looks. Confirm price/news live before using.

**Already had a Trump catalyst (catalyst largely spent — watch for round 2):**
- **DELL** — Q1 buy + May-8 White House endorsement → popped to ATH, then $9.7B
  Pentagon contract. The flagship example; further upside needs a *new* trigger.

**Owns + plausible admin tailwind = top breakout candidates (1–2 month watch):**
- **PLTR (Palantir)** — disclosed buy; admin steers government/defense contracts.
  Catalyst to watch: a named federal contract or public praise.
- **AXON (Axon)** — disclosed buy; policing/border-security tailwind. Catalyst:
  federal/border procurement, public mention.
- **ORCL (Oracle)** — disclosed buy; already a Stargate beneficiary, but more AI-
  infra/federal-cloud announcements could re-trigger.
- **NVDA, AVGO** — disclosed buys; chips ride AI-infra announcements and any
  export/tariff easing toward chips.

**Owns, more macro/quiet (lower-conviction, theme-dependent):**
- **MSFT, META** — mega-cap tech buys; move on broad AI/tariff-relief days.
- **BAC, GS (financials)** — move on deregulation / rate-cut pressure.
- **Media basket: Paramount, WBD, NFLX, DIS, CMCSA** — sensitive to his
  praise/attacks *and* to FCC / merger policy he influences (M&A is the catalyst
  to watch). Note he has bought names he also publicly threatened.
- **Bonds / munis** — large but not catalyst-tradable here.

## Personal / family holdings (mostly NOT things to chase)
- **Trump Media & Technology Group (DJT)** — his stake ~$1.3B (down from ~$4B
  peak). Holds ~9,500+ BTC (~$0.6B) + Cronos (CRO). ⚠️ **Pumps on his posts but is
  a long-term value destroyer:** −~77% from its 2024 high; Q1 2026 net loss
  ~$406M on tiny revenue. Trade spikes, never hold as an investment.
- **World Liberty Financial (WLFI)** — family DeFi venture; ~22.5B WLFI tokens;
  family cashed out ~$1.2B; Abu Dhabi-linked firm bought ~49% for ~$500M. Mostly
  private/token, not a clean equity trade.
- **$TRUMP / $MELANIA memecoins** — ⚠️ **−97% / −99% from peak.** Textbook
  pump-and-dump; canonical "do not chase" cautionary tale.
- **Personal ETH wallet** — disclosed $1M–$5M.
- **Blue chips** also attributed: AAPL, MSFT, NVDA.

## How to use this file
1. When a post names a company, check whether it's on this list → if yes, add the
   **ownership amplifier** (raises conviction; it's the Dell template).
2. For workflow (b) "build a watchlist", lead with the **breakout-candidate**
   group above and pair each with the *specific* catalyst that would trigger it.
3. When updating this file, start from the OGE search/API above, then use
   Reuters or issuer filings only as cross-checks or context.
4. Keep the structural caveat loud: ownership pumps are short-horizon; his own
   assets prove a Trump pump and a good investment are not the same thing.

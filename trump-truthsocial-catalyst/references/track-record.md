# Track record & calibration ledger

This is the file the periodic timer **grows over time** to accumulate a real
hit-rate per pattern. It has two parts: (1) a seeded set of documented historical
cases, and (2) the live ledger the timer appends to and later scores.

> All figures are press-reported or self-disclosed and unverified. A "hit" here
> means the *short-term directional call* worked — it says nothing about whether
> the stock was a good hold.

---

## Seeded historical cases (the calibration starting point)

### ✅ Worked (pumped as the pattern predicts)
| Date | Trigger | Pattern | Name(s) | Outcome |
|---|---|---|---|---|
| 2026-05-08 | "Go out and buy" Dell at White House (he also owned it) | **Tier 1A + ownership + contract follow-through** | DELL | +~14.6% intraday to ATH; +107% YTD; then $9.7B Pentagon contract. **Held** — the gold-standard case. |
| 2025-04 | "THIS IS A GREAT TIME TO BUY!!! DJT" then tariff-pause | **Tier 1B + policy he controls** | DJT / S&P | DJT +22.67% that day; S&P +9.5% on the pause. Broad leg held (real policy); DJT later round-tripped. |
| 2025-01-21 | Stargate "$500B largest AI infra" w/ Oracle | **Tier 2A** | ORCL + AI infra/power | ORCL & datacenter/power names rallied; theme persisted weeks. |
| 2025-04-14 | Electronics tariff exemption; floated auto pause | **Tier 2B** | AAPL +2.2%, DELL +4%, GM +3.5%, F +4.1% | One-day relief rally; ⚠️ flagged "temporary," partial give-back. |
| 2025-03-02 | Crypto strategic-reserve posts naming BTC/ETH/XRP/SOL/ADA | **Tier 2C** | the 5 coins, COIN/MSTR/miners | Spiked Sunday, **gave it back Monday**. Reaction-trade only. |

### ❌ Failed / trap (pumped then destroyed holders, or never delivered)
| Date | Item | What happened | Lesson |
|---|---|---|---|
| 2024→2026 | **DJT for retail** | −~77% from 2024 IPO high ($38.94→$8.77 by 2026-05-12); Q1-26 net loss ~$406M on ~$3.7M 2025 revenue. Insiders fine, retail crushed. | His posts can pump a structurally worthless stock. Pop ≠ hold. |
| 2025–2026 | **$TRUMP memecoin** | −~97% from peak | Pump-and-dump; never chase the late move. |
| 2025–2026 | **$MELANIA memecoin** | −~99% from peak | Same. |
| recurring | **Tariff "relief" walk-backs** | Officials call exemptions "temporary"; sector round-trips within days | Trade the reaction, distrust the follow-through. |
| recurring | **Crypto-reserve / coin posts** | Next-day give-back | Durability is the weakness, not direction. |

### Calibration takeaways (current priors — refine with live data)
- **Highest edge:** Tier 1 named-company praise, *especially* when he owns it and
  a controllable tailwind (contract/carve-out) can follow. These both pop and can
  hold.
- **Strong pop, weak hold:** Tier 2 crypto & tariff-relief — reliable *direction*
  for a fast trade, unreliable *durability*.
- **Avoid as holds:** his own promo (DJT, memecoins) — spikes are exit liquidity.
- **Wrong tool:** pure geopolitics posts (the bulk of his feed) — no clean signal.

---

## Live ledger (the timer appends here; score outcomes on the next runs)

Append one row per market-relevant post. Fill T+1d / T+1w on later runs, then mark
hit/miss. Over time, group by pattern to compute a real hit-rate.

| status_id | date (UTC) | post (short) | tier + amplifiers | implicated ticker(s) | predicted dir / magnitude / durability | T+1d actual | T+1w actual | hit? |
|---|---|---|---|---|---|---|---|---|
| _seed_ | 2026-05-29 | "go out and buy DELL"-style retro note: feed had no fresh Tier-1 stock call as of build | — | — | — | — | — | — |

<!-- TIMER: insert new rows above this line, newest first. Dedupe by status_id. -->

### Rolling hit-rate (recompute each run)
| Pattern | Calls logged | Directional hits | T+1w "held" | Notes |
|---|---|---|---|---|
| Tier 1A named-company praise | 0 | – | – | seed bias: high |
| Tier 1B explicit BUY | 0 | – | – | manipulation scrutiny |
| Tier 2A mega-investment | 0 | – | – | theme-durable |
| Tier 2B tariff relief | 0 | – | – | one-day fade prone |
| Tier 2C crypto | 0 | – | – | one-day fade prone |
| Tier 3 macro theme | 0 | – | – | diffuse |

Update the counts as the live ledger fills. The point of the timer is to replace
the seed priors with *measured* hit-rates so the lens gets sharper over time.

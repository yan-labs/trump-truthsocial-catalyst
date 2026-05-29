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
| 38873 | 2026-05-29 19:05 | [TrumpRx.gov link; MFN prescription-pricing reset](https://trumpstruth.org/statuses/38873) | Tier 2 healthcare/drug-pricing policy; amps: official gov site, MFN/price-control language, intraday post | LLY/NVO/PFE/MRK/JNJ down; PBM/pharmacy impact mixed | Pharma/GLP-1 pricing basket down 0.5% to 3%; medium durability if MFN implementation holds, otherwise headline fade |  |  | pending |
| 38858 | 2026-05-29 18:02 | [EU trade-deal enforcement / auto-tariff pressure](https://trumpstruth.org/statuses/38858) | Tier 2B tariff/trade enforcement; amps: policy he controls, auto-tariff deadline, official ambassador article | STLA/VWAGY/BMWYY/MBGYY down; GM/F/TSLA relative up | EU-auto ADRs down 0.5% to 2%; US domestic autos relative up small; fragile until July 4 deadline |  |  | pending |
| 38852 | 2026-05-29 14:51 | [Hormuz open; naval blockade lifted; Iran final determination pending](https://trumpstruth.org/statuses/38852) | Tier 3 energy/geopolitical de-escalation; amps: Hormuz/shipping, blockade lifted, repeated Iran thread | XOM/CVX/OXY/COP and LMT/RTX down; SPY/IWM risk-on up | Energy/defense -0.5% to -2%; broad risk-on small up; fragile intraday to 1d | Energy/defense basket avg -0.7%, med -1.0%; SPY +0.3%, IWM -0.6% on 2026-05-29 vs 2026-05-28 close; Yahoo Finance chart API fetched 2026-05-29T20:06Z |  | hit (energy/defense; broad mixed) |
| 38838 | 2026-05-27 22:54 | [Armenia route to help American energy companies access Central Asia](https://trumpstruth.org/statuses/38838) | Tier 3 energy corridor; amps: named sector, policy corridor, no named public company | XOM/CVX/LNG/ET/KMI | Up 0.5% to 2%; weak durability unless a concrete project or contract follows | Basket avg -0.3%, med -0.6% on 2026-05-28 vs 2026-05-27 close; Yahoo Finance chart API fetched 2026-05-29T17:07Z |  | miss |
| 38837 | 2026-05-27 22:42 | [Pro-crypto market-structure pledge and "Crypto Capital" framing](https://trumpstruth.org/statuses/38837) | Tier 2C crypto; amps: policy he controls, repeated theme, after-close, personal/family crypto overlap | COIN/MSTR/HOOD/MARA/RIOT/BTC-USD | Up 2% to 5%; low durability and fade-prone | Basket avg +2.4%, med +0.9% on 2026-05-28 vs 2026-05-27 close; Yahoo Finance chart API fetched 2026-05-29T17:07Z |  | hit |
| 38814 | 2026-05-26 21:19 | [CFTC prediction-market authority and crypto protection](https://trumpstruth.org/statuses/38814) | Tier 2C crypto/prediction markets; amps: CFTC policy, repeated crypto, personal/family crypto overlap | HOOD/COIN/MSTR/MARA/RIOT/BTC-USD | Up 1% to 4%; low durability and fade-prone | Basket avg -0.4%, med -0.8% on 2026-05-27 vs 2026-05-26 close; HOOD/RIOT hit but COIN/MSTR/BTC fell; Yahoo Finance chart API fetched 2026-05-29T17:07Z |  | miss (mixed) |
| 38753 | 2026-05-24 14:10 | [Iran talks constructive, but blockade remains until signed deal](https://trumpstruth.org/statuses/38753) | Tier 3 energy/geopolitical risk; amps: blockade, repeated Iran thread, holiday/pre-open | XOM/CVX/OXY/COP and LMT/RTX | Energy/defense up 0.5% to 2%; broad risk-off; fragile until deal clarity | Basket avg -1.9%, med -2.8% on 2026-05-26 vs 2026-05-22 close; Yahoo Finance chart API fetched 2026-05-29T17:07Z |  | miss |
| _seed_ | 2026-05-29 | "go out and buy DELL"-style retro note: feed had no fresh Tier-1 stock call as of build | — | — | — | — | — | — |

<!-- TIMER: insert new rows above this line, newest first. Dedupe by status_id. -->

### Rolling hit-rate (recompute each run)
| Pattern | Calls logged | Directional hits | T+1w "held" | Notes |
|---|---|---|---|---|
| Tier 1A named-company praise | 0 | – | – | seed bias: high |
| Tier 1B explicit BUY | 0 | – | – | manipulation scrutiny |
| Tier 2A mega-investment | 0 | – | – | theme-durable |
| Tier 2B tariff/trade | 1 | 0/0 due | 0/0 due | EU auto-tariff enforcement call pending; durability remains fragile. |
| Tier 2 healthcare pricing | 1 | 0/0 due | 0/0 due | TrumpRx/MFN price-control pressure pending; watch GLP-1 and large pharma basket. |
| Tier 2C crypto | 2 | 1/2 | 0/0 due | One hit and one mixed miss; HOOD/RIOT were strongest, while BTC/MSTR lagged. Durability not yet measured. |
| Tier 3 macro theme | 3 | 1/3 | 0/0 due | Hormuz de-escalation hit energy/defense down, while broad risk was mixed; earlier Iran/energy-corridor calls missed. |

Update the counts as the live ledger fills. The point of the timer is to replace
the seed priors with *measured* hit-rates so the lens gets sharper over time.

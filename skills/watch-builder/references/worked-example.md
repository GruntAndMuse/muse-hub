# Worked Example: Deed Watch (reference) vs GPU Hunt (contrast)

## The deed fraud watch — the reference implementation

**Threat:** a fraudulent grant deed recorded against the house. Slow-moving, high-stakes, legal-grade evidence needed.

- **Baseline:** `hidden_files/baseline.md` — every known legitimate document (doc #, date, grantor, grantee, type), the working search parameters, the site's literal-search quirk, known noise (name-token false positives), and a one-sentence alert rule. Grew over the first week as pre-existing recordings surfaced — each added with a dated "auto-surfaced, NOT a new filing" note.
- **Method:** 4 exact-name searches on the county recorder's public index, daily. The exact-method lesson is canonical here: the simple search flooded with hundreds of noise rows; the exact-name refinement made the check real.
- **Evidence:** 4 timestamped screenshots per run (results tables, count headers visible), PIL timestamp banners burned in, transcription fallback to `hidden_files/deed-watch-YYYY-MM-DD-data.txt` when capture fails.
- **Alert:** any doc number not in the baseline = immediate message with doc #, date, type, parties. Single-name grantee or unknown grantor = highest suspicion. Clean runs get one digest line.
- **Why it's the reference:** tightest baseline, hardest evidence bar, clearest alert rule. When in doubt, build it like the deed watch.

## The GPU hunt — the contrast

**Target:** RTX 40-series under $500 all-in (plus per-model high-VRAM budgets). Fast-moving, deal-driven, evidence is for the digest not the courtroom.

- **Baseline:** the target spec itself — model list, all-in budgets (card + shipping + protection plan combined, never item price alone), seller rules (reputable retailers; eBay only with protection plan + good reputation). No document inventory — the "baseline" is the price bar.
- **Method:** 6 retail sellers + Craigslist + Facebook Marketplace CLI, 2x daily. Two legs with different tools: fast CLI leg (Marketplace, ~1 min) + slow browser leg (~15 min). Timeboxed: browser leg gets ~20 min, then commit partial.
- **Evidence:** append-only `stock-checks.log` with per-run bottom lines, raw CLI JSON dumps per query. No screenshots — prices change too fast for images to matter; the log is the trail.
- **Alert:** qualifying card in stock = digest (or immediate only if genuinely time-sensitive: "only 1 left," auction ending). Near-misses logged, never messaged.
- **Why it differs:** the threat is speed, not fraud. Evidence serves comparison shopping, not legal proof. The all-in pricing rule and the seller-reputation rule are the equivalents of the deed watch's name-format quirk — the details that prevent false positives.

## Lessons from the other two watches

- **Shoe watch — the variant-verification rule.** Amazon variant pages silently switch colorway when you select a width. One real false positive taught the rule: after every selection, RE-VERIFY the final selected variant before calling anything a find. Generalizes to: **re-verify the final state after every interaction, not just the initial query.**
- **FOSS model watch — incumbent/challenger judging.** `top_picks.json` holds current picks per category with license, hardware fit, and quality evidence; new models get scored against incumbents on the same benchmarks. Generalizes to: **when the watch tracks "best of class," the baseline is a leaderboard with scoring rules, and re-evaluation is scheduled, not ad-hoc.**

## Choosing your shape

| | Deed watch | GPU hunt | FOSS watch |
|---|---|---|---|
| Threat speed | slow | fast | medium |
| Evidence bar | legal-grade | log-grade | benchmark-grade |
| Baseline shape | document inventory | price/spec bar | leaderboard + scoring |
| Alert on | any new item | under-cap + in-stock | better score |
| Cadence | daily | 2x daily | 2x daily |

Pick the row that matches your threat. When nothing matches, default to the deed watch — rigor is easier to relax than to retrofit.

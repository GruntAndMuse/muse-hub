---
domain: amazon.com
status: challenged
block_type: ai-agent-interstitial
first_observed: 2026-09-21
last_verified: 2026-10-08
review_after_days: 30
observed_by: gpu-hunt, shoe-watch
confidence: high
---

# amazon.com

## Summary
Amazon serves an explicit anti-automation interstitial to automated browsers
("unauthorized AI agent" / robot-verification text). It held for ~19-20 straight
hunt runs (Sep 21 – Oct 7), then the wall lifted and pages loaded cleanly on
Oct 8. Textbook flapping: treat as hostile until a run proves otherwise.

## Evidence
- 2026-09-26: shoe watch — anti-agent interstitial on 2E family page, 5th straight blocked run, no retry per policy. (goals/dark-soled-ua-assert-10-2e-11-5-restock-watch/hidden_files/reported.json)
- 2026-10-01: shoe watch — ~12th/13th straight blocked runs ("unauthorized AI agent" wall). (~/memory/2026-10-01.md)
- 2026-10-01: GPU hunt — "unauthorized AI agent" bot-block, skipped per standing rule. (goals/rtx-40-series-gpu-under-500-hunt/hidden_files/stock-checks.log)
- 2026-10-02: shoe watch — ~15th straight blocked run. (~/memory/2026-10-02.md)
- 2026-10-05: shoe watch — ~17th straight blocked run. (reported.json)
- 2026-10-06: shoe watch — robot-verification page + "unauthorized AI agent" text, streak continues. (reported.json)
- 2026-10-07: shoe watch — ~19th straight blocked run. (reported.json)
- 2026-10-08: shoe watch — LOADED CLEANLY, anti-agent interstitial streak broken; variant-switch verification clean. (reported.json)
- 2026-10-09: GPU hunt — Amazon blocked by AI-agent wall again (expected, skipped per skip list). (stock-checks.log)

## Notes
- The wall text names AI agents explicitly — this is targeted, not generic bot mitigation.
- Recovery is real: Oct 8 loaded clean after ~3 weeks blocked. Never assume permanent.
- Standing policy in our runs: note and move on, never burn budget retrying.
- Distinct from CAPTCHAs: there is no challenge to solve, just a refusal page.

## History
- 2026-10-09: entry created from hunt run logs (Sep 21 – Oct 9).

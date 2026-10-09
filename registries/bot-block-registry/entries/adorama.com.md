---
domain: adorama.com
status: blocked
block_type: datadome
first_observed: 2026-09-20
last_verified: 2026-10-09
review_after_days: 90
observed_by: gpu-hunt
confidence: medium
---

# adorama.com

## Summary
DataDome-blocked. Sits on the standing skip list — skipped without probing in
every GPU hunt run. No clean load observed in any reviewed run log.

## Evidence
- 2026-09-20: pre-reset probe confirmed DataDome block; placed on skip list. (gpu-hunt cron definition)
- 2026-10-01 through 2026-10-09: skipped per standing bot-block list in every run; never probed (policy: don't burn budget on a known wall). (stock-checks.log, multiple entries)

## Notes
- Confidence is medium, not high: "blocked" is carried-forward knowledge. The
  skip policy means no fresh first-hand probe has been attempted recently — the
  wall is assumed, not re-verified each run. A quarterly re-probe is the honest
  way to keep this entry truthful (see review_after_days).
- DataDome is a dedicated bot-mitigation vendor (distinct from Cloudflare) —
  expect a hard wall, not a solvable challenge.

## History
- 2026-10-09: entry created from GPU hunt run logs and cron skip-list notes.

---
domain: dsw.com
status: clean
block_type: null
first_observed: 2026-09-15
last_verified: 2026-10-09
review_after_days: 90
observed_by: shoe-watch
confidence: high
---

# dsw.com

## Summary
Loads cleanly in essentially every shoe-watch run. One Akamai "Access Denied"
on search Sep 27 — single instance, never recurred.

## Evidence
- 2026-09-15 – 2026-10-09: checked in every shoe-watch run; clean throughout. (reported.json)
- 2026-09-27: one Akamai Access Denied on search; not retried; no recurrence in any later run. (reported.json)

## Notes
- A single vendor block that never repeats is a data point, not a verdict.
  Recorded here so the next person who sees an Akamai wall knows it's happened
  before — once.

## History
- 2026-10-09: entry created from shoe-watch run logs.

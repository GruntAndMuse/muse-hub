---
domain: roadrunnersports.com
status: clean
block_type: null
first_observed: 2026-09-20
last_verified: 2026-10-09
review_after_days: 90
observed_by: shoe-watch
confidence: high
---

# roadrunnersports.com

## Summary
Loads cleanly in every shoe-watch run where it was checked. One TLS/certificate
privacy error Oct 2 made the site unloadable that run — transient transport
issue, not a bot block; fine before and after.

## Evidence
- 2026-09-20 – 2026-10-09: checked in shoe-watch runs; clean throughout. (reported.json)
- 2026-10-02: TLS/certificate privacy error — site unloadable this run; noted, moved on; subsequent runs clean. (~/memory/2026-10-02.md)

## Notes
- TLS errors are infrastructure, not access control. Don't file transport
  failures as blocks.

## History
- 2026-10-09: entry created from shoe-watch run logs.

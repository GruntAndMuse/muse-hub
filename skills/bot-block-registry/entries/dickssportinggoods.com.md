---
domain: dickssportinggoods.com
status: challenged
block_type: antibot-generic
first_observed: 2026-10-01
last_verified: 2026-10-08
review_after_days: 30
observed_by: shoe-watch
confidence: high
---

# dickssportinggoods.com

## Summary
Flapping anti-bot behavior. Served a blank wall page (Oct 1), "Site Unavailable"
(Oct 2), and an "error on the play" anti-bot wall (Oct 5) — then loaded cleanly
Oct 6, 7, and 8. Had previously been restored to rotation Sep 20 after loading
cleanly in a probe. Currently clean, but the wall has appeared three separate
times, so keep it on the watch list.

## Evidence
- 2026-09-20: restored to regular rotation after loading cleanly in pre-reset probe. (shoe-watch cron definition)
- 2026-10-01: BOT-BLOCKED — blank wall page. (~/memory/2026-10-01.md)
- 2026-10-02: BOT-BLOCKED — "Site Unavailable". (~/memory/2026-10-02.md)
- 2026-10-05: product + search pages hit anti-bot "error on the play" wall, not retried. (reported.json)
- 2026-10-06: LOADED CLEANLY. (reported.json)
- 2026-10-07: LOADED CLEANLY. (reported.json)
- 2026-10-08: LOADED CLEANLY. (reported.json)

## Notes
- No named vendor observed (unlike Cloudflare/DataDome/Akamai elsewhere) — wall
  copy varies run to run, suggesting either rotating mitigations or flaky infra.
- Three clean runs in a row as of Oct 8, but history says don't trust it blindly.

## History
- 2026-10-09: entry created from shoe-watch run logs and memory notes.

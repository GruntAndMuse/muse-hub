---
tool: muse-db
title: Muse DB introspection — schema first, column names lie in wait
status: verified
first_observed: 2026-10-01
last_verified: 2026-10-01
review_after_days: 90
observed_by: heartbeat / user-activity checks
confidence: high
---

# muse-db

## Summary
The `muse.db` read-only SQL tool covers Muse's own records (transcripts,
messages, goals, crons...). Column names are not what you'd guess — read the
schema reference before composing SQL, every time.

## Quirks
- 2026-10-01: `activity.activity_monitor_carrier_user_messages` latest-message
  column is `created_at` (`SELECT created_at ... ORDER BY created_at DESC
  LIMIT 1`) — `message_time_utc` doesn't exist. Fix: read
  `/opt/hatch/skills/muse_db/references/schema.md` before composing SQL;
  never guess column names. (~/AGENTS.md)

## Sources
- First-hand: user-activity check, 2026-10-01

## Invalidation triggers
- muse_db schema change (new columns, renamed tables)

## History
- 2026-10-09: entry created from AGENTS.md one-liner.

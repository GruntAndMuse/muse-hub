---
skill: forget
source: bundled
rating: good
confidence: high
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: none yet
---

# forget

## Summary
Remove a personal fact/preference/relationship/event from Muse's active memory
and stop copies/automations from bringing it back. Plan → confirm → execute.

## When to use / vs alternatives
Explicit "forget that" / "don't remember this" requests. NOT for "forget it"
meaning cancel the current task.

## Quality notes
SKILL.md read in full (121 lines) — the most carefully designed destructive
op in the catalog. The plan/confirm two-phase flow, the pending.json claim-
retraction staging, the "silence is not confirmation" rule, and the honest
limits section (outside services, backups may remain) show real care. The
"don't present chat visibility as a cleanup failure" note is product wisdom.

## Gotchas
- Never `rm -r`; exact paths only, revalidated immediately before removal.
- The request doesn't authorize deleting outside email/calendar/device data —
  those need their own approval.

## Evidence
- 2026-10-09: SKILL.md read in full (121 lines). (first-hand)

## History
- 2026-10-09: entry created.

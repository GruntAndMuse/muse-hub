---
skill: device-data
source: bundled
rating: good
confidence: medium
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: none yet
---

# device-data

## Summary
Read cached contacts and calendar events from Muse storage without contacting
the device. Also deletes the local copy on explicit request.

## When to use / vs alternatives
Device offline, or no live `contacts.search`/`calendar.search`. For live
device reads, use the device tools directly. Note the standing privacy
boundary here: nothing may access texts or call logs, period.

## Quality notes
SKILL.md read (138 lines). The ranked-search design (literal → nickname →
phonetic → bounded fuzzy, with selection_evidence for collisions) is careful
contact-resolution engineering. The call-authorization policy tie-in (fuzzy
evidence must pass revalidation before autodial) is the right safety shape.
Not used first-hand here — the privacy boundary keeps it parked.

## Gotchas
- Fuzzy/phonetic matches never autodial; literal matches have their own rules.
- Check `cache.coverage` — the cache may be incomplete.

## Evidence
- 2026-10-09: SKILL.md read (138 lines). (first-hand)

## History
- 2026-10-09: entry created.

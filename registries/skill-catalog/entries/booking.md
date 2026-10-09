---
skill: booking
source: bundled
rating: good
confidence: medium
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: none yet
---

# booking

## Summary
Entry point for flight/hotel/restaurant/event-ticket transactions and bounded
live availability checks. Orchestration layer over provider skills and browser.

## When to use / vs alternatives
Any transaction intent (book, buy, reserve) or live availability/price check.
Use `travel-planning` for open-ended trip planning WITHOUT transaction intent;
use `flightaware` for status of an existing flight. Never substitute a provider
skill or generic browser search for this orchestration layer.

## Quality notes
SKILL.md read in full (309 lines). Clean separation: Booking owns
transactions, Travel Planning owns trip structure. The "load the category
reference before searching" non-negotiables and the detached-worker rules
(reversible assumptions, blockers in the final message) are well designed.
Not used first-hand here — no bookings made in this environment.

## Gotchas
- Watch for: none observed; the skill warns against duplicating inventory in
  two equivalent selection widgets.

## Evidence
- 2026-10-09: SKILL.md read in full (309 lines). (first-hand)

## History
- 2026-10-09: entry created.

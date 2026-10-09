---
skill: places-search
source: bundled
rating: good
confidence: medium
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: none yet
---

# places-search

## Summary
Find and compare physical places: restaurants, cafes, hotels, parks, shops,
local services. `browser.search` for discovery, `places` CLI for details.

## When to use / vs alternatives
"Find me a sushi place near X." Not for itineraries, directions, travel times,
or dated events/showtimes. For restaurant booking (not just finding), that's
the `booking` skill.

## Quality notes
SKILL.md read in full (140 lines). Strong grounding discipline: "never name a
place that did not come back from a tool," no inferred IDs, no estimated
travel times. The location rule ("near me" only with a real message_location)
prevents the classic wrong-city results. Not used first-hand here.

## Gotchas
- `places details` takes numeric IDs only — never derive an ID from a name.
- No addresses, ratings, or price levels in text output (widget carries them).

## Evidence
- 2026-10-09: SKILL.md read in full (140 lines). (first-hand)

## History
- 2026-10-09: entry created.

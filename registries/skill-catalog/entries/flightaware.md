---
skill: flightaware
source: bundled
rating: excellent
confidence: high
first_observed: 2026-10-04
last_verified: 2026-10-09
review_after_days: 90
used_by: bahamas-cruise return flight UAL1513 monitoring
---

# flightaware

## Summary
FlightAware AeroAPI: flight status, delays, cancellations, positions, tracks,
airport activity, schedules. Nothing to connect, no key.

## When to use / vs alternatives
Any specific-flight question ("when's my flight?", delays, monitoring). For
booking or buying tickets, that's the `booking` skill. For airline policies or
terminal maps, web search — FlightAware doesn't cover those.

## Quality notes
147 lines of operational excellence. The monitoring flow (cron cadence bands:
daily → hourly → 10-15 min by departure proximity), the event-fingerprint
deduplication, and the cancellation-corroboration rule (never report from
`cancelled: true` alone) are exactly how you run a flight watch without
spamming. The silence rules (first gate assignment, on-time, boarding = silent)
show real product judgment.

## Gotchas
- Use ICAO flight numbers (`UAL123`, not `UA123`); resolve ambiguity with
  `canonical-flight` first.
- `--date` must be within two days; use `--start`/`--end` for other windows.
- A failed read is not evidence nothing changed — keep monitoring.

## Evidence
- 2026-10-04 through 2026-10-09: UAL1513 FLL→SFO Oct 12 monitoring; baseline
  8:00 AM EDT → 11:05 AM PDT recorded. (travel notes)

## History
- 2026-10-09: entry created.

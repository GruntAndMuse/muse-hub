---
service: flightaware-connector
category: flight-data
tier_status: bundled
confidence: high
first_observed: 2026-10-04
last_verified: 2026-10-09
review_after_days: 90
verified_by: ual1513-monitoring
---

# FlightAware connector

## Summary
FlightAware AeroAPI via the bundled `flightaware` CLI: flight status, delays,
positions, tracks, airport activity. No user key, nothing to connect.

## Free tier details
Bundled with Muse — the connector is provisioned by the platform, not a
user-held AeroAPI key. No quota observed in our monitoring use.

## Auth pattern
None for the user. `flightaware status` verifies reachability.

## Good for
Specific-flight questions, delay/cancellation monitoring with cron cadence
bands, airport activity.

## Limits / gotchas
- `--date` must be within two days; use `--start`/`--end` otherwise.
- A failed read is not evidence nothing changed.

## Evidence
- 2026-10-04 through 2026-10-09: UAL1513 monitoring. (travel notes)

## History
- 2026-10-09: entry created.

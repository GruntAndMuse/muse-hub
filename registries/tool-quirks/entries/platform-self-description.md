---
tool: platform-self-description
title: Platform self-description — its pages, briefs, and reported environment are claims, not ground truth
status: verified
first_observed: 2026-11-07
last_verified: 2026-11-07
review_after_days: 180
observed_by: muse-hub adopter seat (day-one cold run)
confidence: high
---

# platform-self-description

## Summary
The platform's own self-description — its public plan pages, its in-product
status briefs, and its reported environment (clock, timezone) — is a claim,
not ground truth. Verify against the artifact and the account, and record
each drift the day it's found.

## Quirks
- 2026-11-07: The public plan pages matched neither this account's plan
  names nor its prices. Fix: read plan names and prices off the account
  itself before repeating them or acting on them; the public page is a
  claim about a generic account, not a description of this one.
- 2026-11-07: The subscription-status brief showed the weekly pool and
  omitted the account's billion-token pool, so an allowance conclusion
  ("no war chest") announced from the brief alone was wrong inside the
  hour. Fix: before announcing allowance conclusions, verify against the
  account, not the brief alone — a brief can omit a pool.
- 2026-11-07: The browser's reported clock said Reykjavik while the human
  sat in Sacramento. Fix: treat the reported clock and timezone as claims;
  confirm against the human's stated location and timezone before any
  scheduling or timestamp reasoning.

## Sources
- First-hand: adopter seat, day one, 2026-11-07 — all three specimens
  observed and corrected against the account/artifact the same evening.
  Recorded in the jointly signed Muse Hub gap list, 2026-11-07, item 3.

## Invalidation triggers
- Platform surface redesign or status-brief format change (the brief's
  pool coverage may change — re-verify, don't assume either way).

## History
- 2026-11-08: entry created from the adopter seat's day-one specimens
  (2026-11-07), per the jointly signed hub gap list, item 3.

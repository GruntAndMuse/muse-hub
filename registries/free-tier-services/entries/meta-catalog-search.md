---
service: meta-catalog-search
category: product-search
tier_status: bundled
confidence: high
first_observed: 2026-09-13
last_verified: 2026-10-09
review_after_days: 90
verified_by: gpu-hunt, shoe-watch
---

# Meta catalog search

## Summary
Bundled product-search tool (`meta-catalog-search`): up to 8 semantic queries
in one call, ~2.4s measured. The discovery tier of both hunts.

## Free tier details
Bundled with Muse — no vendor tier, no key, no quota observed. It's part of
the platform, not a third-party service.

## Auth pattern
None — invoked as a tool.

## Good for
Fast product discovery and triage. Discovery ONLY — results are noisy
(PCs, posters, and fans appear in GPU results); finalists always go to the
browser for price/stock/variant verification.

## Limits / gotchas
- Measured 2.4s whether 1 or 8 queries — always batch. (catalog-sweep.sh)
- Never trust it for verification: no stock/variant/seller guarantees.

## Evidence
- 2026-09-13 through 2026-10-09: measured in the browser-throughput audit.
  (~/workspace/browser-throughput-audit.md, ~/workspace/bin/catalog-sweep.sh)

## History
- 2026-10-09: entry created.

---
skill: shopping
source: bundled
rating: excellent
confidence: high
first_observed: 2026-09-13
last_verified: 2026-10-09
review_after_days: 90
used_by: gpu-hunt, shoe-watch (twice daily)
---

# shopping

## Summary
Product search and evaluation: Meta catalog search, browser product search,
Facebook Marketplace, result resolution with product markers, purchase flows.

## When to use / vs alternatives
Load FIRST for any shopping intent, before any other skill. For Marketplace
listing management (own listings), that's `facebook-cli`; for finding/buying,
it's this skill. Never report prices from search snippets — only product pages.

## Quality notes
The workhorse of both hunts. `meta-catalog-search` measured at ~2.4s for up
to 8 queries (see `~/workspace/bin/catalog-sweep.sh`) — the discovery tier.
The product-marker discipline (markers belong to the product, not the widget)
prevents the classic "that merino one" unverifiable reference. The required-
attributes flow (resolve gender/size/device BEFORE searching) killed a whole
class of wrong-product results.

## Gotchas
- Catalog results are noisy (PCs, posters in GPU results) — discovery only,
  never verification. Finalists go to the browser.
- `browser.open` cannot fetch Meta first-party links (instagram/facebook);
  use native tools for those.
- One shopping-results presentation per request; don't dribble products out
  across turns.

## Evidence
- 2026-09-13 through 2026-10-09: GPU hunt (48 runs) and shoe watch (twice daily).
  Every near-miss came through this skill's fast leg. (hunt logs)

## History
- 2026-10-09: entry created.

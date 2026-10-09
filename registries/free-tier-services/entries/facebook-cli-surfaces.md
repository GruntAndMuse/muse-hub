---
service: facebook-cli-surfaces
category: social-api
tier_status: bundled
confidence: high
first_observed: 2026-09-13
last_verified: 2026-10-09
review_after_days: 90
verified_by: gpu-hunt
---

# Facebook CLI surfaces

## Summary
The `facebook-cli` tool surfaces (Marketplace search, posts, friends, groups)
run on the user's connected account — no separate API tier.

## Free tier details
Bundled with Muse via the connected Facebook account. No key, no quota
observed. It's the account's access, not a developer tier.

## Auth pattern
Meta Accounts Center connect flow (handled once by the user). Commands run
against that grant.

## Good for
Marketplace searches (the GPU hunt's best leg — every near-miss), structured
Facebook lookups without the browser login wall.

## Limits / gotchas
- Omit `--sort-by` on marketplace search (silently returns zero results).
- Pasted links: never open in the browser; decode and use CLI detail commands.

## Evidence
- 2026-09-13 through 2026-10-09: twice-daily hunt use. (stock-checks.log)

## History
- 2026-10-09: entry created.

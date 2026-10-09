---
service: cloudflare
category: network
tier_status: needs-verification
confidence: low
first_observed: 2026-10-08
last_verified: 2026-10-09
review_after_days: 30
verified_by: security-md-discussion
---

# Cloudflare (Email Routing / Tunnel)

## Summary
Cloudflare was proposed for Email Routing (security@gruntandmuse.com
forwarding) and Tunnel (future mesh-node dashboard). Whether the free tier
covers these uses is UNVERIFIED — this entry exists to prevent the assumption.

## Free tier details
NOT YET CHECKED against Cloudflare's live pricing/terms. Do not assert
anything about cost until someone opens the pricing page and records it here
with URL + date.

## Auth pattern
Unknown until the setup is attempted. Expected: Cloudflare account + DNS
control of gruntandmuse.com (Porkbun registrar).

## Good for
Proposed: email forwarding for SECURITY.md contact addresses; private tunnel
for dashboards. Both pending Dennis being home (DNS changes).

## Limits / gotchas
- The standing rule from the Oct 8 correction: "cost honesty pays" — the
  earlier "it's free" assertion flipped a real decision once corrected to
  "check live terms before setup."
- Email Routing requires DNS hosted on Cloudflare (nameserver change at the
  registrar) — not just an account.

## Evidence
- 2026-10-08: proposed in SECURITY.md red-pen threads; corrected same day to
  "check current terms and DNS requirements live before setup."
  (~/memory/2026-10-08.md, ~/workspace/research-cache/topics/cloudflare-free-tier.md)

## History
- 2026-10-09: entry created as needs-verification. Graduates when the pricing page
  is read and recorded.

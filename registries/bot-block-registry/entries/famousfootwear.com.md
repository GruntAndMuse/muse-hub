---
domain: famousfootwear.com
status: challenged
block_type: cloudflare-challenge
first_observed: 2026-09-15
last_verified: 2026-10-08
review_after_days: 30
observed_by: shoe-watch
confidence: high
---

# famousfootwear.com

## Summary
Cloudflare human-verification wall ("Verifying you are human" / "Just a moment" /
"Access Temporarily Blocked") on most visits. Blocked in the large majority of
shoe-watch runs since Sep 15, with one clean load on Sep 28. Never attempted —
standing rule is ask-Dennis-first on CAPTCHAs.

## Evidence
- 2026-09-15: Cloudflare bot-blocked, not checkable. (reported.json)
- 2026-09-16: Cloudflare bot-blocked. (reported.json)
- 2026-09-20: bot-blocked again by Cloudflare challenge — was restored to rotation in the 12:15am probe but blocked this run; candidate for skip list. (reported.json)
- 2026-09-21: bot-blocked (blank page). (reported.json)
- 2026-09-26: Cloudflare-blocked (security verification wall, not attempted). (reported.json)
- 2026-09-27: Cloudflare-blocked (homepage challenge wall, not attempted). (reported.json)
- 2026-09-28: LOADED CLEANLY — no Cloudflare challenge this run. (reported.json)
- 2026-10-05: Cloudflare "Verifying you are human" challenge, not attempted. (reported.json)
- 2026-10-06: Cloudflare "Just a moment" security verification, not attempted. (reported.json)
- 2026-10-07: Cloudflare "Access Temporarily Blocked", not attempted. (reported.json)
- 2026-10-08: "Access Temporarily Blocked" Cloudflare wall, not attempted. (reported.json)
- 2026-10-09: Cloudflare human challenge, not attempted. (shoe-watch run handoff)

## Notes
- Challenge copy escalated over time: "Verifying you are human" → "Just a moment" → "Access Temporarily Blocked". The last one reads like a harder block tier.
- One clean load (Sep 28) proves flapping — keep probing on the backoff schedule, don't write it off.
- Never attempt the challenge without Dennis's explicit call (standing CAPTCHA rule).

## History
- 2026-10-09: entry created from shoe-watch run logs (Sep 15 – Oct 9).

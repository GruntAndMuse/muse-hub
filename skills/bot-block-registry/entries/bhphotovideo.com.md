---
domain: bhphotovideo.com
status: challenged
block_type: cloudflare-challenge
first_observed: 2026-10-02
last_verified: 2026-10-09
review_after_days: 30
observed_by: gpu-hunt
confidence: high
---

# bhphotovideo.com

## Summary
Cloudflare challenge ("Verify you are human" / "Performing security verification")
appeared Oct 2 and held for about a week, then cleared — loaded clean Oct 8 and
Oct 9. Same timeline as microcenter.com; likely the same Cloudflare policy wave.

## Evidence
- 2026-10-02: NEW — Cloudflare "verifying you are human" stuck, no retry. (stock-checks.log)
- 2026-10-03/04: Cloudflare "Verify you are human" / "Performing security verification", not engaged per ask-first rule. (stock-checks.log)
- 2026-10-05/06: BLOCKED — Cloudflare human-challenge, not solved. (stock-checks.log)
- 2026-10-07: BLOCKED — Cloudflare human-challenge. (stock-checks.log)
- 2026-10-08: loaded clean — no Cloudflare challenge this run. (stock-checks.log)
- 2026-10-09: loaded clean this run. (GPU hunt run handoff)

## Notes
- Blocked Oct 2–7, clean Oct 8–9. Walls come and go; the entry's value is the
  date range, not a permanent verdict.
- Challenge was never attempted (standing ask-first rule on human verification).

## History
- 2026-10-09: entry created from GPU hunt run logs (Oct 2 – Oct 9).

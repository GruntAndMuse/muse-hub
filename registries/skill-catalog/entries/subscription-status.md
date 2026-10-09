---
skill: subscription-status
source: bundled
rating: excellent
confidence: high
first_observed: 2026-09-20
last_verified: 2026-10-09
review_after_days: 90
used_by: burn-pace tracking, allowance math
---

# subscription-status

## Summary
Answers Muse subscription questions: plan, usage %, reset timing, available
plans. One command, one factual brief.

## When to use / vs alternatives
Only when the user asks about the subscription/allowance, or to verify a
claim about it. Do not probe it speculatively.

## Quality notes
21 lines — the smallest skill in the catalog and a model of scope discipline.
Does one thing. The burn-pace math (Friday checks, digest watermarks) runs on
its output. "Muse reports usage against the allowance rather than an exact
token balance" — honest framing, no false precision.

## Gotchas
- None observed. It's a read-only status command.

## Evidence
- 2026-09-20 through 2026-10-09: weekly burn tracking, Friday burn-math checks.
  (burn-pace.md)

## History
- 2026-10-09: entry created.

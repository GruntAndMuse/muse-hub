# Alert Rules

Two tiers. Nothing else.

## Tier 1 — immediate message

ALL of these must hold:
1. **Genuinely time-sensitive**: clear evidence the item will be gone before the next digest (e.g., "only 1 left in stock," auction ending in hours, a fraudulent deed just recorded).
2. **Hard evidence**: the finding is verified, not a snippet or a maybe. Product page, listing page, recorded document — the real thing.
3. **Not a duplicate**: check the dedup fingerprint before messaging.

A new grant deed under a watched name = immediate. A GPU $50 under cap with "only 2 left" = immediate. A GPU $5 under cap with plenty of stock = digest.

## Tier 2 — next digest

Everything else. Routine findings, near-misses, clean runs, coverage notes — they all go in the 8am/5pm digests. The digest is the user's standing appointment with the watch; don't preempt it.

## Quiet hours

Routine findings wait. The user set digest times for a reason — a 2am "nothing new" message is noise, and noise trains the user to ignore the real alerts. Immediate tier overrides quiet hours; nothing else does.

## Deduplication

Compute a stable event fingerprint BEFORE messaging (e.g., `deed-new-grantdeed-<docnumber>`, `gpu-under500-<listing-id>`). Persist it in the state file. Never message the same fingerprint twice. Update `last_notified` after messaging. A worsening situation gets a new fingerprint only when it crosses a band (delay 30-59 → 60-119 → 120+).

## What stays silent

- Clean runs ("nothing new") — the digest line covers it.
- First-time observations that aren't findings (first gate assignment, first sighting of a known item).
- Progress noise (search started, page loaded, task running).

## Burn guardrail

Watches cost allowance. Each run checks the digest's burn watermark: if projected use crosses the trip threshold before reset, the run skips (and says so in the state file). A skipped run is a decision, not a failure — log it as one.

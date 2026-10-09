---
name: "watch_builder"
description: "Build a recurring monitoring watch (fraud, stock, price, release, model) with baseline, evidence, and alert rules. Use when the user asks to watch something over time, set up a recurring check, or when a one-off lookup keeps repeating and deserves a durable pipeline."
---

# Watch Builder

## Purpose
Turn a recurring "check X for changes" need into a durable, evidence-backed watch — baseline first, exact method, saved evidence, clear alert rules — without re-deriving the pattern every time. Built from four production watches: deed fraud (the reference implementation), GPU stock, shoe restock, FOSS model watch.

## Workflow
1. **Baseline first.** Before the first check, record the known-good state in `hidden_files/baseline.md`: what exists today, what counts as "normal," the exact search parameters that work, and the site's quirks (literal search, name formats, token noise). Every future diff is measured against this file, not against memory. Template: `references/baseline-template.md`.
2. **Design the check.** Write the exact method, not the noisy one. One run = a fixed coverage list (every source, every variant), fixed cadence, and a timebox on the flaky leg. See `references/check-design.md` for the exact-method rule and bot-block policy.
3. **Set evidence conventions.** Decide up front what each run saves: screenshots (timestamp burned in for legal-grade trails), append-only logs, JSON state files. Evidence is per-run and dated. The fallback when capture fails: transcribe, don't fabricate. See `references/evidence-conventions.md`.
4. **Write the alert rules.** Two tiers only: immediate message (genuinely time-sensitive + hard evidence) vs next digest (everything else). Respect quiet hours. Deduplicate with stable fingerprints. See `references/alert-rules.md`.
5. **Lay out the state.** Goal workspace layout: `GOAL.md` (what/why), `crons/` (the schedule definitions), `hidden_files/` (baseline, logs, JSON state — never user-facing), `files/` (user-facing evidence like screenshots). See `references/state-layout.md`.
6. **Go live.** Run once manually, verify the baseline against reality, fix the method's rough edges (the first run always finds one), then schedule. Worked example: `references/worked-example.md` (deed watch as reference, GPU hunt as contrast).

## Output Contract
A finished watch has: a `GOAL.md`, a `baseline.md` in `hidden_files/`, a cron definition carrying the full method, a state file (JSON) and append-only log, evidence files per run, and an alert rule with a dedup fingerprint scheme. Another agent can run it cold from these artifacts alone.

## Operating Rules
1. **Baseline is the authority.** A new finding is "not in the baseline," never "looks suspicious." Update the baseline when reality changes; never silently.
2. **Never fabricate evidence.** A missing screenshot is a missing screenshot — transcribe or report the gap honestly. This rule has no exceptions.
3. **Read-only.** Never order, purchase, bid, sign in, or change anything on the watched site. Searches only.
4. **Bot blocks: note and move on.** Never burn run budget retrying a wall, never solve challenges. Record the block, back off per the bot-block registry, keep going. Circumvention is never the fix.
5. **Quiet hours stand.** Routine findings wait for the digest. Immediate messages need clear evidence the item will be gone before the next digest.
6. **Partial beats nothing.** A run that covers 6 of 8 sources with the other 2 named is a completed run. A timed-out run with nothing committed is a failure.
7. **First run fixes the method.** The baseline and method are drafts until the first live run. Budget for it.

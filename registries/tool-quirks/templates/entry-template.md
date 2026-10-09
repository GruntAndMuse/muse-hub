---
tool: example-tool
title: Example Tool — short human title
status: verified
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
observed_by: your-project-or-run
confidence: high
---

# Example Tool

## Summary
One or two sentences: what this tool is and what class of gotchas live here.

## Quirks
Dated bullets. Each: what breaks → the fix/workaround.
- 2026-10-09: `some-command --some-flag` silently does the wrong thing (describe the wrong output). Fix: use `--other-flag` instead. (your run log path)

## Sources
- First-hand: where and when you hit it.

## Invalidation triggers
- Tool version bump (behavior may change).

## History
- 2026-10-09: entry created.

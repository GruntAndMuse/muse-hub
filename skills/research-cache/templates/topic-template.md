---
topic: <slug-lowercase-with-dashes>
title: <Human-readable title>
status: needs-verification
# status is one of: verified | needs-verification | inference | stale | disputed
verified: <YYYY-MM-DD of last verification of the core claims, or "never">
last_checked: <YYYY-MM-DD>
review_after_days: 90
# review_after_days: how long the findings are trusted without re-check.
# 30 = fast-moving (prices, site availability), 90 = tooling, 180 = stable tech, 0 = check every use.
aliases:
# aliases: comma-separated alternate search terms, e.g. "pip, numpy 2"
---

## Findings

Atomic claims, one per bullet. Each ends with a status tag and date.
A claim is [verified] only if someone actually ran/checked it — not "read about it."

- <Claim in one sentence.> [verified YYYY-MM-DD]
- <Claim you believe but haven't checked.> [inference YYYY-MM-DD]

## Sources

- <URL, file path, or "first-hand: <what was run>" — one per finding where possible>

## Invalidation triggers

Events that should force an immediate re-check regardless of `review_after_days`:

- <e.g. "FreeCAD 1.2 release", "vendor pricing page changes">

## History

- YYYY-MM-DD: <what changed and why>

---
topic: facebook-cli-marketplace-quirks
title: facebook-cli marketplace search — known quirks
status: verified
verified: 2026-09-16
last_checked: 2026-10-08
review_after_days: 90
aliases: fb marketplace, gpu hunt, shoe hunt, blocked sources
---

## Findings

- `facebook-cli marketplace search --sort-by price_ascend` silently returns zero results. Verified 2026-09-16: all 6 GPU queries came back empty with the flag, results returned without it. Omit `--sort-by`; `--allowed-item-conditions` + `--max-price` + location flags work fine. [verified 2026-09-16]
- Hunt source reachability is volatile run-to-run: on 2026-10-08 evening, Amazon Renewed, B&H, and Micro Center were all blocked mid-run while other sources worked. Assume any source can be blocked on any given run; record per-run reachability in the run log, don't bake "works" into the hunt scripts. [verified 2026-10-08]

## Sources

- First-hand: GPU hunt runs, `~/workspace/goals/rtx-40-series-gpu-under-500-hunt/hidden_files/` (fb-*.log per run)
- `~/AGENTS.md` ("Tool quirks" section) — one-line version lives there too; this entry carries the dates and evidence

## Invalidation triggers

- facebook-cli version update (sort behavior may get fixed)
- Hunt scripts changed to use a different search path

## History

- 2026-10-09: Created from the AGENTS.md one-liner, promoted with verification dates and the Oct 8 reachability finding. Rationale: tool quirks in AGENTS.md are write-only memory — nobody re-reads them before a hunt. The cache is checked *before* researching.

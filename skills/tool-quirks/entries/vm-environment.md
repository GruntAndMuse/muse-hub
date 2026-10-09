---
tool: vm-environment
title: VM environment — /tmp is wiped mid-session without warning
status: verified
first_observed: 2026-09-29
last_verified: 2026-09-29
review_after_days: 180
observed_by: gmt800-ocr (unzip + page-image pipeline)
confidence: medium
---

# vm-environment

## Summary
This VM's `/tmp` can be wiped between tool calls — files vanish with no
error at write time. Anything a later step needs must live in the workspace.

## Quirks
- 2026-09-29: An unzip directory and page images in `/tmp` vanished between
  tool calls mid-session. Fix: session scratch lives in the workspace
  (`~/workspace/`), never `/tmp`. `/tmp` is only for disposable single-call
  intermediates. (~/AGENTS.md)

## Sources
- First-hand: GMT800 OCR pipeline run, 2026-09-29

## Invalidation triggers
- VM image / runtime change (tmp handling may differ per environment)

## History
- 2026-10-09: entry created from AGENTS.md one-liner. Single observation —
  confidence medium until independently re-observed.

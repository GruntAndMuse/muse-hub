---
tool: facebook-cli
title: facebook-cli marketplace search — silent empty results, volatile reachability
status: verified
first_observed: 2026-09-16
last_verified: 2026-10-08
review_after_days: 90
observed_by: gpu-hunt, shoe-watch
confidence: high
---

# facebook-cli

## Summary
Marketplace search CLI used by the GPU and shoe hunts. One flag silently
empties every result set, and source reachability varies run to run — never
bake "works" into hunt scripts.

## Quirks
- 2026-09-16: `facebook-cli marketplace search --sort-by price_ascend`
  silently returns zero results. Verified: all 6 GPU queries came back empty
  with the flag, results returned without it. Fix: omit `--sort-by`;
  `--allowed-item-conditions` + `--max-price` + location flags work fine.
  (~/AGENTS.md, gpu-hunt fb logs)
- 2026-10-08: Hunt source reachability is volatile run-to-run — Amazon
  Renewed, B&H, and Micro Center were all blocked mid-run on 2026-10-08
  evening while other sources worked. Fix: record per-run reachability in
  the run log; check the bot-block registry before assuming a source is
  reachable. (~/memory/2026-10-08.md, evening hunt report)

## Sources
- First-hand: GPU/shoe hunt runs, `~/workspace/goals/rtx-40-series-gpu-under-500-hunt/hidden_files/` (fb-*.log per run)
- Promoted from research-cache topic `facebook-cli-marketplace-quirks` (2026-10-09)
- Related: bot-block registry (`~/workspace/browser/block-registry/`) for per-domain reachability

## Invalidation triggers
- facebook-cli version update (sort behavior may get fixed)

## History
- 2026-10-09: entry created from AGENTS.md one-liner + research-cache topic.

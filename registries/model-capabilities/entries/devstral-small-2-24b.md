---
slug: devstral-small-2-24b
model: Devstral Small 2 24B
category: coding
license: Apache 2.0
status: incumbent
hardware: ~14GB at Q4_K_M
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# Devstral Small 2 24B

## Summary
Best coding fit for 16GB VRAM. Primary agentic-coding pick.

## Quality evidence
68% SWE-bench Verified [verified: watch benchmarks, 2026-09-18]. Vs Qwen3-Coder-30B-A3B (51.6% SWE-V OpenHands) and Mellum2.1 (47.0% SWE-V, vendor-reported 2026-10-08): Devstral leads on the shared agentic benchmark.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: ~14GB at Q4_K_M.

## Notes
Mellum2.1's only edge is LiveCodeBench v6 82.0 — no LCB number exists for either incumbent, so no displacement.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

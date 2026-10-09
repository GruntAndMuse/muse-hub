---
slug: qwen3-coder-30b-a3b
model: Qwen3-Coder-30B-A3B
category: coding
license: Apache 2.0
status: incumbent
hardware: IQ3/IQ4 quants ~11-16GB or Q4_K_M partial offload
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# Qwen3-Coder-30B-A3B

## Summary
Bigger-context MoE coding pick. Slower than Devstral, wider context window.

## Quality evidence
51.6% SWE-bench Verified (OpenHands harness) [verified: watch benchmarks].

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: IQ3/IQ4 quants ~11-16GB or Q4_K_M partial offload.

## Notes
Secondary pick — Devstral leads the lane on quality-per-VRAM.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

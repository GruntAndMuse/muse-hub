---
slug: muse-glimmer-30b
model: Meta Muse Glimmer 30B
category: coding
license: Apache 2.0
status: challenger
hardware: ~20GB at AWQ 4-bit — needs IQ/Q3 quant or partial CPU offload for 16GB
first_observed: 2026-09-16
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: medium
---

# Meta Muse Glimmer 30B

## Summary
30B dense multimodal tuned for local agents + coding + function calling. Backfill (released Aug 10 2026, found Sep 16).

## Quality evidence
76.0 SWE-Bench Verified / 51.2 SWE-Bench Pro / 51.7 Terminal-Bench 2.1 [verified: watch notes, tech-insider source]. SWE-V 76.0 beats Devstral Small 2 (68%) — but at ~20GB AWQ it needs aggressive quantization or offload to fit 16GB.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: ~20GB at AWQ 4-bit — needs IQ/Q3 quant or partial CPU offload for 16GB.

## Notes
Quality leader on paper; hardware fit is the question. vLLM/llama.cpp/Transformers.

## History
- 2026-09-16: entry created (seeded from FOSS watch history).

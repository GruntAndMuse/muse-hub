---
slug: qwen-image-20b
model: Qwen-Image 20B
category: image
license: Apache 2.0
status: incumbent
hardware: needs GGUF/fp8 on 16GB
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# Qwen-Image 20B

## Summary
Best complex/multilingual text rendering + editing in the image lane.

## Quality evidence
GenEval 0.91, DPG-Bench leading [verified: watch benchmarks]. Qwen-Image-Edit-2511 (edit variant) scored 4.51 ImgEdit_O vs FireRed-Image-Edit-1.1's 4.56 [vendor-reported, FireRed README, 2026-10-08] — close race, watch it.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: needs GGUF/fp8 on 16GB.

## Notes
Needs quantized builds on 16GB — fp8 or GGUF, no full-precision local run.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

---
slug: z-image-turbo-6b
model: Z-Image-Turbo 6B
category: image
license: Apache 2.0
status: incumbent
hardware: fits comfortably in 16GB; sub-second at 8 steps
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# Z-Image-Turbo 6B

## Summary
Fast high-quality text-to-image. Speed lane pick.

## Quality evidence
GenEval 0.82 [verified: watch benchmarks] vs Qwen-Image 0.91 — Z-Image wins on speed, Qwen-Image on quality/complexity.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: fits comfortably in 16GB; sub-second at 8 steps.

## Notes
Pair with Qwen-Image: fast drafts on Z-Image-Turbo, final/complex renders on Qwen-Image.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

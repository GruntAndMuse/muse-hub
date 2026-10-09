---
slug: swinir
model: SwinIR
category: jpg-cleanup
license: Apache 2.0
status: incumbent
hardware: fits 16GB easily
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# SwinIR

## Summary
Dedicated JPEG-artifact removal / denoise model. Fidelity-first pick for scanned-page cleanup.

## Quality evidence
Classic5 JPEG CAR (q=10/20/30/40) PSNR 30.27/32.52/33.73/34.52 [verified: SwinIR paper Table 4, 2026-09-18]. LIVE1 q=10-40 PSNR 29.86-34.67 [verified: same paper]. Directly relevant to JPEG-scanned manual cleanup; Real-ESRGAN has nothing published on JPEG artifact removal [verified: benchmarks.md gap analysis, 2026-09-18].

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: fits 16GB easily.

## Notes
Replaced DiffBIR v2 after the 2026-09-17 deep audit (DiffBIR's SD 2.1 weights are OpenRAIL — fails the license rule).

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

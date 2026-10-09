---
slug: real-esrgan
model: Real-ESRGAN
category: jpg-cleanup
license: BSD-3-Clause
status: incumbent
hardware: tiled inference fits 16GB; NCNN Windows builds
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# Real-ESRGAN

## Summary
General restoration/upscaling backup behind SwinIR. Perceptual quality on real camera degradations.

## Quality evidence
RealSR-Canon NIQE 4.5899, RealSR-Nikon 5.0759, DRealSR 4.9799 [verified: Real-ESRGAN paper Table 1, 2026-09-18]. Paper reports only NIQE (no PSNR/LPIPS in own paper) [verified: benchmarks.md, 2026-09-18].

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: tiled inference fits 16GB; NCNN Windows builds.

## Notes
Backup role only — for the user's JPEG-scan task SwinIR has the directly relevant numbers.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

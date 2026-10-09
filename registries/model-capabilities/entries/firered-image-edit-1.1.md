---
slug: firered-image-edit-1.1
model: FireRed-Image-Edit-1.1
category: image
license: Apache 2.0
status: challenger
hardware: ~30GB VRAM optimized build — needs partial RAM offload (acceptable per his rules)
first_observed: 2026-10-08
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: medium
---

# FireRed-Image-Edit-1.1

## Summary
Image-EDITING model (instruction-following edits, identity consistency, multi-element fusion, old-photo restoration). First Apache-2.0 edit model with published leading numbers on the watch.

## Quality evidence
ImgEdit_O 4.56 / GEdit_O EN 7.943 / CN 7.887 / REDEdit EN 4.26 / CN 4.33 — beats every open-source row in their table (Qwen-Image-Edit-2511 4.51/7.877, LongCat-Image-Edit 4.45, FLUX.2[Dev] 4.35) [VENDOR-REPORTED, official README, 2026-10-08 — unconfirmed]. No GenEval/DPG-Bench — not head-to-head with Z-Image-Turbo (0.82) / Qwen-Image (0.91).

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: ~30GB VRAM optimized build — needs partial RAM offload (acceptable per his rules).

## Notes
License verified 2026-10-08 on official GitHub (License field + LICENSE file + README). Backfill: weights released 2026-03-03; Oct 6 coverage was a recrawl. Photo restoration + portrait consistency relevant to his GruntAndMuse graphic work.

## History
- 2026-10-08: entry created (seeded from FOSS watch history).

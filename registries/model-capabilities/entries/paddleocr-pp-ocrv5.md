---
slug: paddleocr-pp-ocrv5
model: PaddleOCR PP-OCRv5
category: ocr
license: Apache 2.0
status: incumbent
hardware: fits 16GB
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# PaddleOCR PP-OCRv5

## Summary
Classic detect+recognize pipeline. Holds the rotated/vertical schematic-text lane.

## Quality evidence
PaddleOCR's internal Rotation/Vertical scenario splits are private [verified: benchmarks.md, 2026-09-18]. Lane held on architectural fit for bottom-to-top rotated schematic labels, not on a public rotation benchmark (none exists).

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: fits 16GB.

## Notes
Complement to PaddleOCR-VL-1.6, not a competitor — different lane (rotated text vs full-page parsing).

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

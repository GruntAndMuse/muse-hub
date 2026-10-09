---
slug: paddleocr-vl-1.6
model: PaddleOCR-VL-1.6 0.9B
category: ocr
license: Apache 2.0
status: incumbent
hardware: ~2-4GB (0.9B bf16; GGUF for llama.cpp)
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# PaddleOCR-VL-1.6 0.9B

## Summary
SOTA document-parsing VLM. User-flagged best fit for the S10 manual pages.

## Quality evidence
OmniDocBench v1.6 Overall 96.33 = ((1-0.033)*100 + 94.76 + 97.49)/3 [verified: official leaderboard, 2026-09-18]. Full page-to-Markdown pipeline score (layout/tables/formulas), not raw line accuracy. Real5-OmniDocBench covers skew/warp degradations [verified: tech report].

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: ~2-4GB (0.9B bf16; GGUF for llama.cpp).

## Notes
No standard public benchmark exists for 90-degree bottom-to-top rotated text recognition [verified: benchmarks.md research, 2026-09-18] — PP-OCRv5 keeps the rotated-text lane on pipeline grounds, not benchmark grounds.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

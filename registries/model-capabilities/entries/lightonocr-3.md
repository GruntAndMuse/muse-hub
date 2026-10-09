---
slug: lightonocr-3
model: LightOnOCR-3 (0.8B/1B/4B)
category: ocr
license: Apache 2.0
status: challenger
hardware: trivially fits 16GB
first_observed: 2026-10-08
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: medium
---

# LightOnOCR-3 (0.8B/1B/4B)

## Summary
Strongest published-score doc-OCR challenger on the watch. New grounding mode: labeled bboxes + image descriptions + chart data as HTML tables in one pass.

## Quality evidence
olmOCR-Bench: 4B 86.3 / 0.8B 85.5 / 1B 84.5 vs Infinity Parser Pro 87.6 (35.1B) [VENDOR-REPORTED, official HF blog, 2026-10-08 — unconfirmed]. ParseBench overall: 4B 75.1 vs Infinity Parser Pro 74.3 [same source, unconfirmed]. NOT head-to-head with PaddleOCR-VL-1.6: no OmniDocBench v1.6 number published; no 90-degree rotation score.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: trivially fits 16GB.

## Notes
License verified 2026-10-08 on the official HF blog. Re-evaluation rule: watch for an OmniDocBench v1.6 score — until then it cannot displace PaddleOCR-VL-1.6. Recommended: side-by-side on his S10 manual pages.

## History
- 2026-10-08: entry created (seeded from FOSS watch history).

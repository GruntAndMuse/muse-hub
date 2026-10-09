---
slug: mellum2.1-12b-a2.5b-thinking
model: JetBrains Mellum2.1-12B-A2.5B-Thinking
category: coding
license: Apache 2.0
status: challenger
hardware: GGUF Q4_K_M 8.1GB / MXFP4_MOE 7.0GB — trivially fits 16GB
first_observed: 2026-10-08
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: medium
---

# JetBrains Mellum2.1-12B-A2.5B-Thinking

## Summary
Small/fast agentic-coding MoE (12B total, 2.5B active/token, 131K ctx). Not a quality challenger on agentic coding; candidate for the small/fast lane.

## Quality evidence
SWE-V 47.0 / SWE-Pro 28.0 / Terminal-Bench 2.1 17.4 / LiveCodeBench v6 82.0 / HumanEval+ 91.5 [VENDOR-REPORTED by JetBrains on its own pipeline, 2026-10-08 — unconfirmed]. Vs Devstral Small 2 (68.0% SWE-V): not a quality challenger. LCB v6 82.0 is the only published LCB number on the watch.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: GGUF Q4_K_M 8.1GB / MXFP4_MOE 7.0GB — trivially fits 16GB.

## Notes
License: Apache 2.0 stated by JetBrains (marktechpost cites HF release). Fit: shootout candidacy on his own tasks, small/fast lane.

## History
- 2026-10-08: entry created (seeded from FOSS watch history).

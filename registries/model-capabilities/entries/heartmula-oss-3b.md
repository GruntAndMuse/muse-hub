---
slug: heartmula-oss-3b
model: HeartMuLa-oss-3B
category: audio
license: Apache 2.0
status: incumbent
hardware: ~6.2GB
first_observed: 2026-09-17
last_verified: 2026-10-09
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: high
---

# HeartMuLa-oss-3B

## Summary
Text-to-music with the best lyric controllability on the watch.

## Quality evidence
Triton/Win11 caveats noted in watch logs — verify the inference stack on the target machine.

## Hardware fit
Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. Partial RAM offload acceptable per standing rules. This entry: ~6.2GB.

## Notes
Kandinsky 6.0 (MIT) is the only permissive video+audio model — adjacent, not a replacement.

## History
- 2026-09-17: entry created (seeded from FOSS watch history).

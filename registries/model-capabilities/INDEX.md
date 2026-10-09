# Model capabilities — index

One-line summaries state the *finding*, not the subject. Sorted by category,
then slug. Status in brackets.

## jpg-cleanup

- [real-esrgan](entries/real-esrgan.md) — backup restorer; perceptual NIQE numbers only, nothing published on JPEG artifact removal [incumbent]
- [swinir](entries/swinir.md) — the JPEG-cleanup pick: Classic5/LIVE1 q=10–40 PSNR numbers directly match the scanned-manual task [incumbent]

## ocr

- [deepseek-ocr-2](entries/deepseek-ocr-2.md) — v2 fixes v1's silent license card with an explicit Apache 2.0 repo license [challenger]
- [lightonocr-3](entries/lightonocr-3.md) — strongest published-score doc-OCR challenger; no OmniDocBench v1.6 number yet, so no displacement [challenger]
- [ovisocr2](entries/ovisocr2.md) — clean Apache 2.0 on code and weights, mid-pack challenger [challenger]
- [paddleocr-pp-ocrv5](entries/paddleocr-pp-ocrv5.md) — holds the rotated/vertical schematic-text lane on pipeline fit; no public rotation benchmark exists [incumbent]
- [paddleocr-vl-1.6](entries/paddleocr-vl-1.6.md) — the doc-parsing pick: 96.33 OmniDocBench v1.6, best fit for the S10 manual pages [incumbent]
- [teleocr](entries/teleocr.md) — ParseBench datum logged 2026-10-07; license badge exists but no LICENSE text in tree — verify before commercial-adjacent use [challenger]
- [xiaomi-ocr-0](entries/xiaomi-ocr-0.md) — 96.83 OmniDocBench v1.6 sits in a three-way cluster with PaddleOCR-VL-1.6 and TeleOCR, no clear winner [challenger]

## coding

- [devstral-small-2-24b](entries/devstral-small-2-24b.md) — the coding pick: 68% SWE-bench Verified at ~14GB Q4_K_M, leads the lane on quality-per-VRAM [incumbent]
- [gpt-oss-20b](entries/gpt-oss-20b.md) — 20B-class open-weight alternative; smaller/faster than the 24–30B incumbents [challenger]
- [mellum2.1-12b-a2.5b-thinking](entries/mellum2.1-12b-a2.5b-thinking.md) — small/fast MoE (8.1GB Q4); only edge is LiveCodeBench v6 82.0, a benchmark with no incumbent score [challenger]
- [muse-glimmer-30b](entries/muse-glimmer-30b.md) — 76.0% SWE-V beats Devstral on paper, but ~20GB AWQ needs aggressive quant/offload to fit 16GB [challenger]
- [qwen3-coder-30b-a3b](entries/qwen3-coder-30b-a3b.md) — bigger-context MoE second pick; slower than Devstral, wider window [incumbent]

## image

- [firered-image-edit-1.1](entries/firered-image-edit-1.1.md) — first Apache-2.0 image-EDIT model with leading published numbers; needs partial RAM offload [challenger]
- [ming-image-0.1](entries/ming-image-0.1.md) — MIT-licensed image challenger; license simplicity is the edge under the MIT-for-everything rule [challenger]
- [qwen-image-20b](entries/qwen-image-20b.md) — the quality pick: GenEval 0.91, best complex/multilingual text rendering; needs GGUF/fp8 on 16GB [incumbent]
- [z-image-turbo-6b](entries/z-image-turbo-6b.md) — the speed pick: sub-second at 8 steps, fast drafts before Qwen-Image finals [incumbent]

## video

- [kandinsky-6.0](entries/kandinsky-6.0.md) — the only permissive video+audio model on the watch; adjacent to the lane, not a direct challenger [challenger]
- [ltx-video-13b](entries/ltx-video-13b.md) — the speed pick; use only 0.9.x Apache weights, 2.x are community-licensed [incumbent]
- [wan2.2-ti2v-5b](entries/wan2.2-ti2v-5b.md) — the quality pick: 720p/24fps text+image-to-video; VDOT++ weights pending mid-October is the lead to watch [incumbent]

## audio

- [chatterbox-multilingual-v3](entries/chatterbox-multilingual-v3.md) — the TTS pick: 23+ languages, voice cloning, 0.5B tiny [incumbent]
- [heartmula-oss-3b](entries/heartmula-oss-3b.md) — the text-to-music pick: best lyric controllability; Triton/Win11 caveats [incumbent]
- [sopro-v2-turbo](entries/sopro-v2-turbo.md) — TTS challenger pinned to rev 2610; revision pin is part of the pick [challenger]
- [voxcpm2](entries/voxcpm2.md) — TTS challenger with confirmed repo license; Breeze/Voxtral exclusions keep this lane permissive-only [challenger]

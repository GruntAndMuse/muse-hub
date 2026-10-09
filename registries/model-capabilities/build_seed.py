#!/usr/bin/env python3
"""Seed generator for the model-capabilities registry.
Run once: python3 build_seed.py
Provenance for the 25 seed entries (2026-10-09). Kept, not deleted.
Sources: ~/workspace/goals/foss-local-ai-model-watch/hidden_files/
         {top_picks.json, seen_models.json, model-checks.log (2026-10-07..09)}
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ENTRIES = os.path.join(ROOT, "entries")

# slug, model, category, license, status, hardware, first_observed,
# last_verified, confidence, summary, quality, notes
MODELS = [
# ---------------- INCUMBENTS (top_picks.json, 6 lanes) ----------------
("swinir", "SwinIR", "jpg-cleanup", "Apache 2.0", "incumbent",
 "fits 16GB easily", "2026-09-17", "2026-10-09", "high",
 "Dedicated JPEG-artifact removal / denoise model. Fidelity-first pick for scanned-page cleanup.",
 "Classic5 JPEG CAR (q=10/20/30/40) PSNR 30.27/32.52/33.73/34.52 [verified: SwinIR paper Table 4, 2026-09-18]. "
 "LIVE1 q=10-40 PSNR 29.86-34.67 [verified: same paper]. Directly relevant to JPEG-scanned manual cleanup; "
 "Real-ESRGAN has nothing published on JPEG artifact removal [verified: benchmarks.md gap analysis, 2026-09-18].",
 "Replaced DiffBIR v2 after the 2026-09-17 deep audit (DiffBIR's SD 2.1 weights are OpenRAIL — fails the license rule)."),
("real-esrgan", "Real-ESRGAN", "jpg-cleanup", "BSD-3-Clause", "incumbent",
 "tiled inference fits 16GB; NCNN Windows builds", "2026-09-17", "2026-10-09", "high",
 "General restoration/upscaling backup behind SwinIR. Perceptual quality on real camera degradations.",
 "RealSR-Canon NIQE 4.5899, RealSR-Nikon 5.0759, DRealSR 4.9799 [verified: Real-ESRGAN paper Table 1, 2026-09-18]. "
 "Paper reports only NIQE (no PSNR/LPIPS in own paper) [verified: benchmarks.md, 2026-09-18].",
 "Backup role only — for the user's JPEG-scan task SwinIR has the directly relevant numbers."),
("paddleocr-vl-1.6", "PaddleOCR-VL-1.6 0.9B", "ocr", "Apache 2.0", "incumbent",
 "~2-4GB (0.9B bf16; GGUF for llama.cpp)", "2026-09-17", "2026-10-09", "high",
 "SOTA document-parsing VLM. User-flagged best fit for the S10 manual pages.",
 "OmniDocBench v1.6 Overall 96.33 = ((1-0.033)*100 + 94.76 + 97.49)/3 [verified: official leaderboard, 2026-09-18]. "
 "Full page-to-Markdown pipeline score (layout/tables/formulas), not raw line accuracy. "
 "Real5-OmniDocBench covers skew/warp degradations [verified: tech report].",
 "No standard public benchmark exists for 90-degree bottom-to-top rotated text recognition "
 "[verified: benchmarks.md research, 2026-09-18] — PP-OCRv5 keeps the rotated-text lane on pipeline grounds, not benchmark grounds."),
("paddleocr-pp-ocrv5", "PaddleOCR PP-OCRv5", "ocr", "Apache 2.0", "incumbent",
 "fits 16GB", "2026-09-17", "2026-10-09", "high",
 "Classic detect+recognize pipeline. Holds the rotated/vertical schematic-text lane.",
 "PaddleOCR's internal Rotation/Vertical scenario splits are private [verified: benchmarks.md, 2026-09-18]. "
 "Lane held on architectural fit for bottom-to-top rotated schematic labels, not on a public rotation benchmark (none exists).",
 "Complement to PaddleOCR-VL-1.6, not a competitor — different lane (rotated text vs full-page parsing)."),
("devstral-small-2-24b", "Devstral Small 2 24B", "coding", "Apache 2.0", "incumbent",
 "~14GB at Q4_K_M", "2026-09-17", "2026-10-09", "high",
 "Best coding fit for 16GB VRAM. Primary agentic-coding pick.",
 "68% SWE-bench Verified [verified: watch benchmarks, 2026-09-18]. "
 "Vs Qwen3-Coder-30B-A3B (51.6% SWE-V OpenHands) and Mellum2.1 (47.0% SWE-V, vendor-reported 2026-10-08): "
 "Devstral leads on the shared agentic benchmark.",
 "Mellum2.1's only edge is LiveCodeBench v6 82.0 — no LCB number exists for either incumbent, so no displacement."),
("qwen3-coder-30b-a3b", "Qwen3-Coder-30B-A3B", "coding", "Apache 2.0", "incumbent",
 "IQ3/IQ4 quants ~11-16GB or Q4_K_M partial offload", "2026-09-17", "2026-10-09", "high",
 "Bigger-context MoE coding pick. Slower than Devstral, wider context window.",
 "51.6% SWE-bench Verified (OpenHands harness) [verified: watch benchmarks].",
 "Secondary pick — Devstral leads the lane on quality-per-VRAM."),
("z-image-turbo-6b", "Z-Image-Turbo 6B", "image", "Apache 2.0", "incumbent",
 "fits comfortably in 16GB; sub-second at 8 steps", "2026-09-17", "2026-10-09", "high",
 "Fast high-quality text-to-image. Speed lane pick.",
 "GenEval 0.82 [verified: watch benchmarks] vs Qwen-Image 0.91 — Z-Image wins on speed, Qwen-Image on quality/complexity.",
 "Pair with Qwen-Image: fast drafts on Z-Image-Turbo, final/complex renders on Qwen-Image."),
("qwen-image-20b", "Qwen-Image 20B", "image", "Apache 2.0", "incumbent",
 "needs GGUF/fp8 on 16GB", "2026-09-17", "2026-10-09", "high",
 "Best complex/multilingual text rendering + editing in the image lane.",
 "GenEval 0.91, DPG-Bench leading [verified: watch benchmarks]. "
 "Qwen-Image-Edit-2511 (edit variant) scored 4.51 ImgEdit_O vs FireRed-Image-Edit-1.1's 4.56 [vendor-reported, FireRed README, 2026-10-08] — close race, watch it.",
 "Needs quantized builds on 16GB — fp8 or GGUF, no full-precision local run."),
("wan2.2-ti2v-5b", "Wan2.2-TI2V-5B", "video", "Apache 2.0", "incumbent",
 "8-16GB", "2026-09-17", "2026-10-09", "high",
 "Text+image to video, 720p/24fps. Quality lane pick.",
 "Watch benchmarks logged 2026-09-18; VDOT++ (few-step video, weights pending mid-October) is the lead to watch in this lane.",
 "VDOT++ code+weights promised before mid-October 2026 — re-check on arrival."),
("ltx-video-13b", "LTX-Video 13B distilled", "video", "Apache 2.0", "incumbent",
 "~12GB min, 16GB ComfyUI builds", "2026-09-17", "2026-10-09", "high",
 "Fastest video generation pick. Speed lane.",
 "License caveat: 2.x weights are community-licensed — use only the Apache-2.0 0.9.x core weights "
 "[verified: watch license notes]. Verify the specific weight file before use.",
 "The license caveat is load-bearing — wrong weight file voids the pick."),
("heartmula-oss-3b", "HeartMuLa-oss-3B", "audio", "Apache 2.0", "incumbent",
 "~6.2GB", "2026-09-17", "2026-10-09", "high",
 "Text-to-music with the best lyric controllability on the watch.",
 "Triton/Win11 caveats noted in watch logs — verify the inference stack on the target machine.",
 "Kandinsky 6.0 (MIT) is the only permissive video+audio model — adjacent, not a replacement."),
("chatterbox-multilingual-v3", "Chatterbox Multilingual V3", "audio", "MIT", "incumbent",
 "0.5B, tiny", "2026-09-17", "2026-10-09", "high",
 "TTS: 23+ languages with voice cloning. Tiny enough to run anywhere.",
 "Demucs (MIT) covers stem separation alongside it [verified: watch notes].",
 "PocketTTS (Kyutai, Jan 2026) was excluded 2026-10-09: weights CC-BY-4.0 gated behind HF access agreement — "
 "violates the no-accounts rule. Chatterbox keeps the lane."),
# ---------------- OCT 8 QUALIFYING LEADS ----------------
("lightonocr-3", "LightOnOCR-3 (0.8B/1B/4B)", "ocr", "Apache 2.0", "challenger",
 "trivially fits 16GB", "2026-10-08", "2026-10-09", "medium",
 "Strongest published-score doc-OCR challenger on the watch. New grounding mode: labeled bboxes + image descriptions + chart data as HTML tables in one pass.",
 "olmOCR-Bench: 4B 86.3 / 0.8B 85.5 / 1B 84.5 vs Infinity Parser Pro 87.6 (35.1B) [VENDOR-REPORTED, official HF blog, 2026-10-08 — unconfirmed]. "
 "ParseBench overall: 4B 75.1 vs Infinity Parser Pro 74.3 [same source, unconfirmed]. "
 "NOT head-to-head with PaddleOCR-VL-1.6: no OmniDocBench v1.6 number published; no 90-degree rotation score.",
 "License verified 2026-10-08 on the official HF blog. Re-evaluation rule: watch for an OmniDocBench v1.6 score — "
 "until then it cannot displace PaddleOCR-VL-1.6. Recommended: side-by-side on his S10 manual pages."),
("mellum2.1-12b-a2.5b-thinking", "JetBrains Mellum2.1-12B-A2.5B-Thinking", "coding", "Apache 2.0", "challenger",
 "GGUF Q4_K_M 8.1GB / MXFP4_MOE 7.0GB — trivially fits 16GB", "2026-10-08", "2026-10-09", "medium",
 "Small/fast agentic-coding MoE (12B total, 2.5B active/token, 131K ctx). Not a quality challenger on agentic coding; candidate for the small/fast lane.",
 "SWE-V 47.0 / SWE-Pro 28.0 / Terminal-Bench 2.1 17.4 / LiveCodeBench v6 82.0 / HumanEval+ 91.5 "
 "[VENDOR-REPORTED by JetBrains on its own pipeline, 2026-10-08 — unconfirmed]. "
 "Vs Devstral Small 2 (68.0% SWE-V): not a quality challenger. LCB v6 82.0 is the only published LCB number on the watch.",
 "License: Apache 2.0 stated by JetBrains (marktechpost cites HF release). Fit: shootout candidacy on his own tasks, small/fast lane."),
("firered-image-edit-1.1", "FireRed-Image-Edit-1.1", "image", "Apache 2.0", "challenger",
 "~30GB VRAM optimized build — needs partial RAM offload (acceptable per his rules)", "2026-10-08", "2026-10-09", "medium",
 "Image-EDITING model (instruction-following edits, identity consistency, multi-element fusion, old-photo restoration). "
 "First Apache-2.0 edit model with published leading numbers on the watch.",
 "ImgEdit_O 4.56 / GEdit_O EN 7.943 / CN 7.887 / REDEdit EN 4.26 / CN 4.33 — beats every open-source row in their table "
 "(Qwen-Image-Edit-2511 4.51/7.877, LongCat-Image-Edit 4.45, FLUX.2[Dev] 4.35) [VENDOR-REPORTED, official README, 2026-10-08 — unconfirmed]. "
 "No GenEval/DPG-Bench — not head-to-head with Z-Image-Turbo (0.82) / Qwen-Image (0.91).",
 "License verified 2026-10-08 on official GitHub (License field + LICENSE file + README). Backfill: weights released 2026-03-03; "
 "Oct 6 coverage was a recrawl. Photo restoration + portrait consistency relevant to his GruntAndMuse graphic work."),
# ---------------- KEY CHALLENGERS (seen_models.json) ----------------
("teleocr", "TeleOCR (StarDoc-AI/TeleOCR)", "ocr", "Apache 2.0", "challenger",
 "fits 16GB", "2026-10-07", "2026-10-09", "medium",
 "Doc-OCR challenger (formerly NaviDC-OCR). ParseBench third-party datum recorded 2026-10-07.",
 "ParseBench third-party datum logged 2026-10-07 PM run [verified: model-checks.log].",
 "License caveat: Apache 2.0 declared on README badge + HF metadata, but a third-party audit found no actual LICENSE text "
 "in the repo tree — intent looks clear, verify before any commercial-adjacent use."),
("xiaomi-ocr-0", "Xiaomi-OCR-0 (SeerRay-Lab/Xiaomi-OCR-0)", "ocr", "Apache-2.0", "challenger",
 "fits 16GB", "2026-10-02", "2026-10-09", "medium",
 "Doc-OCR challenger in the OmniDocBench 96+ cluster.",
 "OmniDocBench v1.6 Overall 96.83 [verified: watch benchmarks] — vs PaddleOCR-VL-1.6 (96.33) and TeleOCR (96.87): three-way cluster, no clear winner.",
 "License verified 2026-10-02 on official HF card 'Citation and License' section."),
("ovisocr2", "OvisOCR2 (ATH-MaaS/OvisOCR2)", "ocr", "Apache 2.0", "challenger",
 "fits 16GB", "2026-09-16", "2026-10-09", "medium",
 "Doc-OCR challenger. License clean on both code and weights.",
 "License verified on official HF card LICENSE section + repo [verified: seen_models.json].",
 "Seeded from watch history; exact first-log date approximate (watch seeding era)."),
("deepseek-ocr-2", "DeepSeek-OCR 2 (deepseek-ai/DeepSeek-OCR-2)", "ocr", "Apache 2.0", "challenger",
 "fits 16GB", "2026-09-25", "2026-10-09", "medium",
 "Doc-OCR challenger from DeepSeek. Cleaner license story than v1.",
 "Apache 2.0 verified 2026-09-25 on the official GitHub repo (LICENSE.txt in root); the HF card page text still states no license, as with v1.",
 "v1's license was MIT-per-third-party-only with a silent official card — v2 fixes this with an explicit repo license."),
("gpt-oss-20b", "gpt-oss-20b", "coding", "Apache 2.0", "challenger",
 "fits 16GB", "2026-09-16", "2026-10-09", "medium",
 "Open-weight coding/general model in the 20B class. Watch-listed challenger.",
 "Seeded from watch history; exact first-log date approximate (watch seeding era).",
 "Smaller/faster alternative to the 24-30B incumbents; quality position per watch benchmarks."),
("muse-glimmer-30b", "Meta Muse Glimmer 30B", "coding", "Apache 2.0", "challenger",
 "~20GB at AWQ 4-bit — needs IQ/Q3 quant or partial CPU offload for 16GB", "2026-09-16", "2026-10-09", "medium",
 "30B dense multimodal tuned for local agents + coding + function calling. Backfill (released Aug 10 2026, found Sep 16).",
 "76.0 SWE-Bench Verified / 51.2 SWE-Bench Pro / 51.7 Terminal-Bench 2.1 [verified: watch notes, tech-insider source]. "
 "SWE-V 76.0 beats Devstral Small 2 (68%) — but at ~20GB AWQ it needs aggressive quantization or offload to fit 16GB.",
 "Quality leader on paper; hardware fit is the question. vLLM/llama.cpp/Transformers."),
("kandinsky-6.0", "Kandinsky 6.0 Video", "video", "MIT", "challenger",
 "fits 16GB", "2026-10-06", "2026-10-09", "medium",
 "The only permissive video+AUDIO model on the watch. Logged 2026-10-06 PM.",
 "MIT verified 2026-10-06 on official GitHub (LICENSE file in root); multiple secondary sources confirm MIT covers code + weights.",
 "Adjacent to the video lane rather than a direct challenger — video+audio in one permissive package is unique on the watch."),
("ming-image-0.1", "Ming-Image-0.1-Design (inclusionAI)", "image", "MIT", "challenger",
 "fits 16GB", "2026-09-25", "2026-10-09", "medium",
 "MIT-licensed image generation challenger.",
 "MIT verified 2026-09-25 via HF card metadata + third-party review of both cards.",
 "MIT (vs Apache-2.0 incumbents) is a license-simplicity edge under his MIT-for-everything rule."),
("sopro-v2-turbo", "Sopro v2 Turbo (rev 2610)", "audio", "Apache-2.0", "challenger",
 "fits 16GB", "2026-10-04", "2026-10-09", "medium",
 "TTS challenger. Pinned to revision 2610 checkpoint — the revision pin is part of the pick.",
 "Apache-2.0 verified 2026-10-04 on official GitHub (LICENSE.txt in root); HF card page text itself states no license.",
 "Revision pinning matters — unpinned TTS checkpoints drift. Record the rev with the pick."),
("voxcpm2", "VoxCPM2 (OpenBMB)", "audio", "Apache 2.0", "challenger",
 "fits 16GB", "2026-09-26", "2026-10-09", "medium",
 "TTS challenger with confirmed repo license.",
 "Apache 2.0 confirmed via official GitHub repo LICENSE (github.com/OpenBMB/VoxCPM).",
 "Breeze TTS 2 was excluded as non-commercial; Voxtral TTS as CC BY-NC — VoxCPM2 and Sopro keep the permissive TTS lane."),
]

TEMPLATE = """---
slug: {slug}
model: {model}
category: {category}
license: {license}
status: {status}
hardware: {hardware}
first_observed: {first_observed}
last_verified: {last_verified}
review_after_days: 30
observed_by: foss-local-ai-model-watch
confidence: {confidence}
---

# {model}

## Summary
{summary}

## Quality evidence
{quality}

## Hardware fit
{hardware_fit}

## Notes
{notes}

## History
- {first_observed}: entry created (seeded from FOSS watch history).
"""

def main():
    os.makedirs(ENTRIES, exist_ok=True)
    for row in MODELS:
        (slug, model, category, license, status, hardware, first_observed,
         last_verified, confidence, summary, quality, notes) = row
        hw_fit = ("Target rig: RTX 4070 Ti SUPER 16GB VRAM, 32GB system RAM. "
                  "Partial RAM offload acceptable per standing rules. "
                  "This entry: " + hardware + ".")
        text = TEMPLATE.format(slug=slug, model=model, category=category,
                               license=license, status=status, hardware=hardware,
                               first_observed=first_observed,
                               last_verified=last_verified, confidence=confidence,
                               summary=summary, quality=quality,
                               hardware_fit=hw_fit, notes=notes)
        with open(os.path.join(ENTRIES, slug + ".md"), "w") as f:
            f.write(text)
    print(f"wrote {len(MODELS)} entries")

if __name__ == "__main__":
    main()

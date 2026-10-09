---
service: huggingface-hub
category: model-registry
tier_status: needs-verification
confidence: medium
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 30
verified_by: foss-model-watch
---

# Hugging Face Hub

## Summary
Model registry — the source for FOSS model weights (the twice-daily FOSS
watch tracks new models here). Public model downloads observed free.

## Free tier details
Public model downloads work without payment (observed). Inference API limits
and PRO tier details NOT verified — check the live pricing page before any
design depends on hosted inference.

## Auth pattern
Downloads: none needed for public models (hf_transfer/huggingface_hub).
Private models and inference endpoints need a token (not our use).

## Good for
Pulling open model weights for local runs (the FOSS watch's whole purpose —
models that run on the user's RTX 4070 Ti Super, judged on quality).

## Limits / gotchas
- Large model downloads are bandwidth-heavy; the VM handles them, but don't
  re-download what's cached.

## Evidence
- 2026-10-09: FOSS watch pulls model info from HF daily; public downloads observed
  working. Inference pricing not checked. (foss watch logs)

## History
- 2026-10-09: entry created as needs-verification for inference; downloads observed free.

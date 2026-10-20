# Personal GPU Node — run your AI's heavy work on your own hardware

**Status:** living playbook. First drafted 2026-10-10 from the GruntAndMuse
setup (RTX 4070 Ti SUPER 16GB, Windows 11 Pro). Update as the setup evolves.

## The idea

Cloud GPU rentals and metered AI pipelines charge you monthly for compute you
may already own. A mid-range gaming PC (16GB VRAM) can run modern open-weight
models locally: image generation (Flux.1 Schnell), transcription (Whisper),
document understanding, even video. Your AI assistant drives it remotely; you
pay nothing per use.

## What it unlocks

- **FOSS media pipeline** — image/video/TTS generation with Apache 2.0 / open
  weights. No vendor lock-in, no per-image meter.
- **Batch document work** — OCR whole manual libraries overnight.
- **Local model inference** — Q&A over your own document collections.
- **App testing** — Android emulator for APK testing without cloud device farms.
- **Community jobs** — free batch services (scan cleanup, OCR) for your
  community, scheduled when idle.

## Setup (Windows 11 Pro example)

1. **Remote access:** Tailscale (free personal tier) + Windows OpenSSH server.
   The assistant SSHes in over the encrypted tailnet. Nothing else inbound.
2. **Storage:** a dedicated folder on a data drive (D:) — the assistant's
   bulk storage for models, datasets, renders.
3. **Image gen:** ComfyUI + Flux.1 Schnell (Apache 2.0). Runs well in 16GB.
4. **Android:** Android Studio emulator (free, official) for APK testing.
5. **Transcription:** Whisper (open weights) for fast local STT.

## Security model (the part that matters)

- **Nobody touches the machine except the assistant.** No public IPs, no open
  ports, no inbound internet services. Tailscale only.
- **Community submissions are curated, never automatic.** Uploads land in a
  quarantine folder; the assistant inspects every file before it touches the
  GPU. Anything sketchy dies there.
- **Start with your trusted circle**, not the open internet.
- **Your work preempts everything.** The assistant schedules community batch
  jobs overnight/idle; your jobs always jump the queue.

## Cost reality

- Hardware: already paid for (sunk cost).
- Electricity: a 300W GPU running overnight batches — pennies per job.
- vs. cloud: no monthly fee, no per-image/per-minute meter, no caps.

## What we learned (GruntAndMuse, 2026-10-10)

- The idea came from hitting a 16/day metered-image budget — own the iron,
  drop the meter.
- Dennis's rule: local iteration is free, deployments are the scarce resource.
  Same logic applies here: experiment freely on the node, ship carefully.
- When brainstorming "how do I give my assistant more ability," check your
  own hardware first. We missed this for weeks.

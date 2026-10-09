---
skill: tts
source: bundled
rating: excellent
confidence: high
first_observed: 2026-10-02
last_verified: 2026-10-09
review_after_days: 90
used_by: voice notes, driving mode
---

# tts

## Summary
Text-to-speech via bundled `tts` CLI: single-shot `speak` and multi-speaker
`synthesize-script`. Voice notes, artifact audio, cron audio.

## When to use / vs alternatives
Voice notes/messages, reading text aloud, artifact narration. For podcasts or
briefings, use `podcast`/`generate_podcast`. Dennis's voice pick:
`avocado_v2:TruthTeller`; offer voice mode when he mentions driving.

## Quality notes
240 lines, excellent operational detail. The failure ladder (retry same
request at 5m/10m/30m/1h, never switch voices — "a failure is not a reason to
pick another voice") is the standout: it prevents the classic flailing.
Voice-source discipline (exact IDs from authoritative files, never from memory)
killed a whole class of "wrong voice" bugs.

## Gotchas
- Non-English quality varies significantly — set `--language` to match the
  text, never send non-English text with `--language en`.
- The TTS API caches aggressively; vary text slightly before concluding
  voice routing is broken.
- Write text in spoken form ("forty-two", not "42").

## Evidence
- 2026-10-02: voice notes enabled; voice pick recorded in USER.md. Ongoing
  use for driving mode. (USER.md)

## History
- 2026-10-09: entry created.

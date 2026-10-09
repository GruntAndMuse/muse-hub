---
tool: chat-attachments
title: Chat STL attachments fail on the Android app — zip them first
status: verified
first_observed: 2026-09-25
last_verified: 2026-09-25
review_after_days: 180
observed_by: k2-riser (STL delivery to Dennis's phone)
confidence: high
---

# chat-attachments

## Summary
STL files attached via `sandbox://` fail on the receiving end: the Android
app shows "?" (unknown file type) and Creality Print reports "no geometry
data." The files are valid — it's a delivery issue, not a file issue.

## Quirks
- 2026-09-25: `sandbox://` STL attachments arrive broken on the Muse Android
  app ("?" icon) and Creality Print reports "no geometry data." Fix: zip the
  STL before attaching — the .zip downloads clean. (~/AGENTS.md, k2-riser
  delivery)

## Sources
- First-hand: 2026-09-25 delivery failure and zip workaround
- Promoted from research-cache topic `chat-stl-attachments` (2026-10-09)

## Invalidation triggers
- Muse Android app update (attachment handling may change)
- Creality Print app update

## History
- 2026-10-09: entry created from AGENTS.md one-liner + research-cache topic.

---
topic: chat-stl-attachments
title: Chat STL attachments fail — zip them first
status: verified
verified: 2026-09-25
last_checked: 2026-09-25
review_after_days: 180
aliases: sandbox stl, 3d print files, attachments
---

## Findings

- STL files attached via `sandbox://` fail on Dennis's side: the Android app shows "?" (unknown file type) and Creality Print reports "no geometry data." The files themselves are valid — it's a delivery issue, not a file issue. [verified 2026-09-25]
- Workaround: zip STLs before attaching. The .zip downloads clean. [verified 2026-09-25]

## Sources

- First-hand: 2026-09-25 delivery failure and zip workaround
- `~/AGENTS.md` ("Tool quirks" section)

## Invalidation triggers

- Muse Android app update (attachment handling may change)
- Creality Print app update

## History

- 2026-10-09: Created from the AGENTS.md one-liner.

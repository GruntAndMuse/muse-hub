---
topic: hatch-gws-cli-drive-quirks
title: hatch_gws_cli drive — folder creation and large-upload gotchas
status: verified
verified: 2026-10-05
last_checked: 2026-10-05
review_after_days: 90
aliases: google drive cli, gws, drive upload, mimeType
---

## Findings

- To create a REAL Drive folder, the `mimeType: application/vnd.google-apps.folder` goes in the `--json` request body, NOT in `--params`. Putting mimeType in `--params` silently creates a regular octet-stream file literally named "Untitled"; uploads using it as parent then fail with "The specified parent is not a folder." Same for renames: `files update` needs the name in `--json`, not `--params`. [verified 2026-10-01]
- `files create --upload` fails on files over ~1GB (HTTP request failed after 4–7 min, 3/3 attempts on a 1.7GB PDF). Split large PDFs into <500MB parts before uploading — the parts upload cleanly. Don't retry giants; skip and note. [verified 2026-10-05]

## Sources

- First-hand: mid-upload failure 2026-10-01 (the folder quirk — "learned the hard way, mid-upload"); 1.7GB GMT800 PDF upload failures 2026-10-05
- `~/AGENTS.md` ("Tool quirks" section) — one-line versions; this entry carries dates and the failure signatures

## Invalidation triggers

- `hatch_gws_cli` version update (flag handling may change)
- Google Drive API behavior change on large uploads

## History

- 2026-10-09: Created from the AGENTS.md one-liners. These two cost real failed uploads; the cache entry exists so the next agent reads it instead of paying again.

---
tool: hatch-gws-cli
title: hatch_gws_cli drive — folder creation and large-upload gotchas
status: verified
first_observed: 2026-10-01
last_verified: 2026-10-05
review_after_days: 90
observed_by: gmt800-ocr, drive uploads
confidence: high
---

# hatch_gws_cli drive

## Summary
Google Workspace CLI for Drive operations. Two gotchas cost real failed
uploads: folder creation silently makes the wrong object type when the
mimeType goes in the wrong place, and large uploads die outright past ~1GB.

## Quirks
- 2026-10-01: To create a REAL Drive folder, `mimeType:
  application/vnd.google-apps.folder` goes in the `--json` request body, NOT
  in `--params`. Putting mimeType in `--params` silently creates a regular
  octet-stream file literally named "Untitled"; uploads using it as parent
  then fail with "The specified parent is not a folder." Same for renames:
  `files update` needs the name in `--json`, not `--params`. Learned the hard
  way, mid-upload. (~/memory/2026-10-01.md)
- 2026-10-05: `files create --upload` fails on files over ~1GB — HTTP request
  failed after 4–7 min, 3/3 attempts on a 1.7GB PDF. Fix: split large PDFs
  into <500MB parts before uploading; the parts upload cleanly. Don't retry
  giants; skip and note. (~/workspace/gmt800-ocr-test/, ~/AGENTS.md)

## Sources
- First-hand: mid-upload failure 2026-10-01; 1.7GB GMT800 PDF upload failures 2026-10-05
- Promoted from research-cache topic `hatch-gws-cli-drive-quirks` (2026-10-09)

## Invalidation triggers
- `hatch_gws_cli` version update (flag handling may change)
- Google Drive API behavior change on large uploads

## History
- 2026-10-09: entry created from AGENTS.md one-liners + research-cache topic.

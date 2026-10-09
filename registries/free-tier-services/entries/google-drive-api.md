---
service: google-drive-api
category: cloud-storage
tier_status: free-tier
confidence: high
first_observed: 2026-10-01
last_verified: 2026-10-09
review_after_days: 90
verified_by: gmt800-ocr-uploads, med-tracker
---

# Google Drive API

## Summary
Drive file operations via `hatch_gws_cli drive`: folders, uploads, downloads,
sharing, in-place content updates. Used daily.

## Free tier details
The Drive API itself is free within Google Cloud project quotas. NOTE: the
user's storage is a paid 5TB plan (~8GB used, ~18 months headroom per
2026-10-02) — storage is not the free tier here, API access is. His standing
call: "go ham," storage is not a constraint.

## Auth pattern
`hatch_gws_cli` with the connected Google account. Folder creation quirk
(documented): real folders need mimeType in the `--json` request body, not
`--params` (AGENTS.md, 2026-10-01).

## Good for
Large file hosting (multi-GB PDFs), shared folders, backup discipline ("2 is 1
and 1 is none"), the Book Drop shared folder.

## Limits / gotchas
- `files create --upload` fails on files over ~1GB (verified 2026-10-05, 3/3
  attempts on 1.7GB PDFs). Split large PDFs into <500MB parts before uploading.
- API quotas are per project; batch operations should stay sequential.

## Evidence
- 2026-10-01 through 2026-10-09: daily Drive operations — GMT800 PDF uploads (39
  files), Book Drop, shared folders. (AGENTS.md tool quirks; memory logs)

## History
- 2026-10-09: entry created.

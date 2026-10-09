---
service: github
category: version-control
tier_status: free-tier
confidence: high
first_observed: 2026-10-02
last_verified: 2026-10-09
review_after_days: 90
verified_by: gruntandmuse-releases
---

# GitHub

## Summary
Git hosting, issue/PR tracking, Releases, and Actions CI. The home of all
GruntAndMuse public repos (mesh-to-cad, document-ocr, med-tracker).

## Free tier details
Public repositories are free with unlimited collaborators. GitHub Actions is
free for public repos (usage limits apply to private repos). Release hosting
included — we ship APKs and binaries via Releases. (Long-standing public
GitHub terms; re-verify exact Actions minute quotas on the pricing page if a
private-repo CI design depends on them.)

## Auth pattern
Two paths in this environment: (1) the `github-custom` workspace skill with
the user-connected `custom.github` credential via surrogate helpers —
api.github.com only; (2) the bundled `github` skill's OAuth/MCP connect flow
for new authorizations. Plain git over HTTPS/SSH for clone/push.

## Good for
Public FOSS releases, CI builds (Windows/macOS/Linux via Actions), release
artifact hosting, transparency logs.

## Limits / gotchas
- Release asset storage is generous but not infinite; very large binaries
  (>2GB per file) hit release asset limits.
- Actions minutes for private repos are metered — public repos are the free path.

## Evidence
- 2026-10-02 through 2026-10-09: mesh-to-cad, document-ocr, med-tracker (v1.0.30,
  v1.0.31) releases published; CI green across 3 OSes. (release URLs in
  ~/memory/2026-10-0*.md)

## History
- 2026-10-09: entry created.

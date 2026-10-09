---
skill: github-custom
source: custom
rating: excellent
confidence: high
first_observed: 2026-10-05
last_verified: 2026-10-09
review_after_days: 90
used_by: med-tracker, mesh-to-cad, document-ocr releases
---

# github-custom (workspace skill)

## Summary
Workspace skill (`~/workspace/skills/github/`) for the GitHub REST API via the
user-connected `custom.github` credential. This is the skill actually used for
all GruntAndMuse repo work — releases, raw file verification, repo management.

## When to use / vs alternatives
Use for any GitHub API work: releases, repo reads, issue/PR operations. Use
the **bundled** `github` skill instead when the task needs the OAuth/MCP
connect flow or repository-installation UX. For pure git operations (clone,
push, log), plain shell git is faster — no skill needed.

## Quality notes
Only 25 lines and exactly right: credential mechanics (surrogate helpers),
host restriction to api.github.com, and the key diagnostic insight — "a 401/403
is a question about the request before it is a question about the key." The
Auth section forbids asking the user to paste keys. Minimal and correct.

## Gotchas
- Authenticated requests must go through the `dynamic_credentials.py` helpers;
  a request built without them carries nothing and looks exactly like a bad token.
- Restricted to api.github.com — raw.githubusercontent.com reads go through
  plain fetch, not this skill.

## Evidence
- 2026-10-05 through 2026-10-09: used for med-tracker v1.0.30/v1.0.31 release
  publishing, APK checksum verification, mesh-to-cad and document-ocr pushes.
  (release URLs in ~/memory/2026-10-0*.md)

## History
- 2026-10-09: entry created.

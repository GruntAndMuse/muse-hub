---
skill: github
source: bundled
rating: good
confidence: medium
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: none yet
---

# github (bundled)

## Summary
GitHub via the official MCP server with a Muse-owned GitHub App identity.
Handles OAuth connect flow and repository-installation UX.

## When to use / vs alternatives
Use when the task needs the connect/install UX (new user, new repo access) or
MCP tool calls. Use `github-custom` (workspace skill) for day-to-day API work
on already-connected repos — it's lighter. Plain git for clone/push/log.

## Quality notes
SKILL.md read in full (75 lines). The connect flow is carefully specified:
exact `install_url` handling, widget presentation, no invented links, and the
honest note that OAuth status alone doesn't prove repo access. The
read/write tool split (`call-read-tool` vs `call-tool` with approval) is the
right safety shape. Not battle-tested here — we use the custom skill instead.

## Gotchas
- "Do not claim private-repository access from OAuth status or a click on the
  installation link alone" — verify with a reviewed read tool.
- Never infer read safety from GitHub's live catalogue; newly advertised tools
  stay write-capable until reviewed.

## Evidence
- 2026-10-09: SKILL.md read in full (75 lines). (first-hand)

## History
- 2026-10-09: entry created.

---
tool: git-workflow
title: git — verify the PUSHED tree, not just the local tree
status: verified
first_observed: 2026-10-07
last_verified: 2026-10-07
review_after_days: 180
observed_by: document-ocr CI repair
confidence: high
---

# git-workflow

## Summary
`git status` clean locally does not mean the push is complete. A commit can
amend-away a file the CI workflow references, and local checks won't catch
it — the pushed tree is the only truth that matters.

## Quirks
- 2026-10-07: Commit 548017e broke document-ocr CI because
  `tests/make_qc_fixtures.py` was never in the pushed commit (the workflow
  referenced it); a fix commit had to land 4 min later. Local `git status`
  showed clean the whole time. Fix: after every push, verify the pushed tree
  with `git ls-tree` or a raw.githubusercontent check on the new commit —
  never call a push done from local state alone. (~/AGENTS.md)

## Sources
- First-hand: document-ocr CI break and repair, 2026-10-07

## Invalidation triggers
- None expected — this is git semantics, not tool behavior. Re-verify if CI
  moves off GitHub Actions.

## History
- 2026-10-09: entry created from AGENTS.md lesson.

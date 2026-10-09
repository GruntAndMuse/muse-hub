---
service: pypi
category: package-registry
tier_status: free-tier
confidence: high
first_observed: 2026-09-18
last_verified: 2026-10-09
review_after_days: 90
verified_by: daily-agent-work
---

# PyPI

## Summary
Python package registry. Free, unlimited public package installs.

## Free tier details
No tier — PyPI is free for downloads, no account needed for `pip install`.
The whole Python ecosystem rides on it.

## Auth pattern
None for installs. (Publishing needs an account + API token; not our use.)

## Good for
Every Python dependency: trimesh, numpy, scipy, and everything in the
pipelines.

## Limits / gotchas
- Unpinned installs can break environments (documented numpy-2.x breakage vs
  FreeCAD's bundled numpy 1.26.4 — see research-cache `freecad-python-env-quirks`).
  Pin versions; use `--no-deps` when the host bundle already provides them.

## Evidence
- Daily use since 2026-09-18 across all pipeline work. (memory logs)

## History
- 2026-10-09: entry created.

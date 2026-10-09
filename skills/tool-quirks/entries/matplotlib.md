---
tool: matplotlib
title: matplotlib as CAD — Path CLOSEPOLY drops the last corner
status: verified
first_observed: 2026-09-26
last_verified: 2026-09-26
review_after_days: 180
observed_by: k2-riser (2D technical drawings)
confidence: high
---

# matplotlib

## Summary
matplotlib is a plotting library, not CAD — but it was the drawing tool for
the K2 riser 2D sheets, and its `Path` API has a sharp edge that silently
deforms polygons.

## Quirks
- 2026-09-26: `Path.CLOSEPOLY` ignores its vertex coordinates — the last real
  corner must be an explicit `LINETO`. An 8-vertex/8-code path draws a
  diagonal "point" instead of the 8th corner. Fix: use N+1 vertices (repeat
  the first point at the end) with `[MOVETO] + [LINETO]*(N-1) + [CLOSEPOLY]`.
  (~/AGENTS.md, k2-riser drawing corrections)

## Sources
- First-hand: K2 riser drawing work, 2026-09-26 (V-series drawing corrections)

## Invalidation triggers
- matplotlib major version change in Path handling (unlikely — long-standing behavior)

## History
- 2026-10-09: entry created from AGENTS.md lesson.

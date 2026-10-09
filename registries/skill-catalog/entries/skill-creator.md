---
skill: skill-creator
source: bundled
rating: good
confidence: high
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: muse-hub skill publication path
---

# skill-creator

## Summary
Create or update workspace skills: description, structure, instructions,
supporting files. The publication mechanism for the hub.

## When to use / vs alternatives
When a workflow is reusable enough to become a skill. For one-off tasks,
don't. Prefer `scaffold-connector-skill --provider` for connector skills —
don't hand-write auth sections.

## Quality notes
53 lines, and it's the reason the hub's "ships as a skill" plan is credible.
The core loop (narrow scope → plan layout → draft → trim aggressively →
sanity-check) plus the operating rules ("preserve working commands; do not
invent binaries, paths, or auth flows") encode real authoring judgment. The
`references/authoring_guide.md` carries the detail without bloating SKILL.md.

## Gotchas
- Python CLIs: `py_compile` before reporting success.
- Keep bulky docs in `references/`, not SKILL.md.

## Evidence
- 2026-10-09: SKILL.md read in full (53 lines); designated as the hub's skill
  publication path. (first-hand)

## History
- 2026-10-09: entry created.

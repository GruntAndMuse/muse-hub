---
skill: research-cache
source: draft
rating: excellent
confidence: high
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: muse-hub prototype (live)
---

# research-cache (draft)

## Summary
Topic-keyed store of verified research findings. Check before researching;
write back everything verified. Kills re-derivation.

## When to use / vs alternatives
Before ANY web research: `./rc.py lookup <keywords>`. After verifying
anything: `./rc.py new <slug>`, fill, `./rc.py check`. Holds research
findings — not user facts (memory), not run logs (project folders).

## Quality notes
Live prototype at `~/workspace/research-cache/` — built, validated, and
already proved its point (the numpy-2.x same-day re-derivation case). The
status taxonomy (verified/needs-verification/inference/stale/disputed),
the claim discipline ("unlabeled claims are lies"), and the mechanical
`check` enforcement are the strongest epistemic design in the hub so far.
SKILL.md draft ships with it; nothing needs restructuring to publish.

## Gotchas
- Only as good as the lookup-before-research habit — the skill must make it a
  hard rule, not a suggestion.
- INDEX.md hand-maintained; revisit past ~50 topics.

## Evidence
- 2026-10-09: prototype built and validated end-to-end (lookup/show/stale/new/check;
  checker proven against 5 deliberately broken entries).
  (~/workspace/research-cache/)

## History
- 2026-10-09: entry created.

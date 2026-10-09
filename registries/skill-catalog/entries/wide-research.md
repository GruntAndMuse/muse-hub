---
skill: wide-research
source: bundled
rating: excellent
confidence: high
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: mit-rebuild-candidates survey (4 parallel agents)
---

# wide-research

## Summary
Fan out one research task across many independent inputs via a manager
subagent; returns a single normalized result set.

## When to use / vs alternatives
Many independent items, shared output schema ("wide research", screening,
parallel lookups). NOT for single items or dependent subtasks.

## Quality notes
44 lines, tight. The manager contract (operation_brief, inputs, output_schema,
worker_prompt_template, completion_format) and the output contract
(total/success/failure/results/failures/notes) are exactly the right
abstraction. "Reply to the user immediately that wide research has started;
do not block on completion" — correct async UX. Proven same-day: the
MIT-rebuild survey fanned 4 cluster agents and returned a ranked list.

## Gotchas
- One manager per user goal; don't fan out multiple sibling root subagents.
- Deduplicate inputs before spawning.

## Evidence
- 2026-10-09: 4-agent MIT-rebuild candidate survey completed via this pattern.
  (mit-rebuild-candidates-2026-10-09.md)

## History
- 2026-10-09: entry created.

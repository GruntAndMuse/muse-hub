# Reconciliation: corrections, conflicts, newer evidence

Memory is wrong the moment the user corrects you or the world changes. The
fix happens **the same turn** — a stale claim left active next to its
correction is a lie.

## The two file types, two treatments

**Dated logs (`~/memory/YYYY-MM-DD.md`) are append-only.** Never rewrite
history to look clean. When a correction arrives, append a dated entry:

```markdown
## Correction (2026-10-09)
- Earlier note said the target was 1.0.x. Verified 2026-10-09: the stable
  line is 1.1.x — 1.1.4 is the current release. The 1.0.x recommendation
  is superseded.
```

The old entry stays. The correction names it, dates the change, and says what
replaced what. Anyone reading the log sees the full story, including that you
were wrong and when you learned it.

**Curated files (`~/MEMORY.md`, `~/memory/people/*.md`) are edited in place.**
Replace the stale claim with the corrected one and date the change inline:

```markdown
- Wire-label system (changed 2026-09-20): simple name + the manual's book
  page only — blue tape temporary, printed permanent (old start/end/circuit
  system abandoned).
```

The parenthetical dates are the mechanism: they show *when the fact changed*
without keeping the dead version around.

## Conflicting sources

When two sources disagree (a memory entry vs. a fresh message, two messages
from different days), resolve by recency and authority:

1. **The user's latest explicit statement wins** over older entries.
2. **First-hand evidence wins** over second-hand reports.
3. If genuinely ambiguous, **ask** — one short question beats a wrong guess
   baked into the record.

Record the resolution, not just the result: "User corrected X on 2026-10-09;
prior entry from 2026-10-03 superseded." Future you needs to know *why* the
record changed, or you'll "correct" it back.

## The `muse.memory_explain` habit

When the user asks "how do you know that?" or "is that still true?", use
`muse.memory_explain` on the claim before answering. It shows where the
memory came from, what it replaced, and what replaced it — which is exactly
what you need to answer honestly. Never defend a memory you haven't
re-checked; the tool is faster than your confidence.

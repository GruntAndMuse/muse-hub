# State vs History: Telling Current from Archival

## Current (trust for "what's happening")
- **Today's daily log** (`~/memory/YYYY-MM-DD.md`) — what actually happened today
- **Job run history** — what ran, when, with what result (last few runs)
- **Tracking/goal statuses** — active vs closed, as the system reports them *now*
- **Tails of working files** — the last lines of logs, notes, and specs in `hidden_files/`
- **NOW boards / status files** — only if they're maintained daily (check the mtime; a NOW.md untouched for a month is history wearing a "now" costume)

## Archival (trust for "what happened," never for "what's next")
- Older daily logs (context, not state)
- Compaction summaries (lossy by design — the summary says what it kept, not what it dropped)
- Completed goal records and old run logs
- Design docs and plans (intent at write time; verify against run history)

## The tests
1. **The mtime test.** `ls -la` the file. A working file updated today is state; one untouched for weeks is history. When in doubt, the newer file wins over the older file's claims.
2. **The "next action" test.** Any file naming a next step must be verified against a live source before you act on it. Ask: "is there a newer record that supersedes this?" Check today's log, the goal's current status, the file's own tail.
3. **The completion-marker test.** Before reading a notes file first-hand, check its tail for COMPLETE / FINISHED / "closed." Finished work re-read is the most common orientation tax in this shop — it has happened at least six documented times.
4. **The pointer-freshness test.** A pointer ("continue at X," "next: Y") is only as fresh as the file holding it. Pointers in daily logs go stale within hours; pointers in the target file's own tail are the authority. When two pointers disagree, the target file's tail wins.

## Common traps
- **The summary trap.** A compaction summary says "the pass ended at 127/134" — useful orientation, but the *findings file* is the source. Never quote a summary as the record; re-read the source when the detail matters.
- **The checklist trap.** A checklist line naming the current item ("start Genius of Birds") may predate the work it names. The notes tail is the authority, not the checklist.
- **The "another file" trap.** LOG.md, wantlists, daily logs, and summaries are all "another file." Their pointers go stale. Only the target file's own tail is authoritative. This specific trap has burned ~10 minutes per occurrence, repeatedly.

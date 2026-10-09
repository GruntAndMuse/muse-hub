---
name: "workspace_orientation"
description: "First-15-minutes orientation in an unfamiliar workspace. Use when you wake up in a workspace you don't know: read order, live-state vs archive, and the anti-patterns that waste the most time. Triggers on: new session, post-compaction recovery, 'where are we', picking up someone else's project."
---

# Workspace Orientation

## Purpose
Get a working map of an unfamiliar workspace in ~15 minutes: who you're helping, what's active, and where the live state lives — without re-reading finished work or acting on stale pointers.

## Workflow

**1. Read what's already in your context (free).**
The standing files are injected into every session: who you are (SOUL/IDENTITY), who the user is (USER), curated memory (MEMORY), how this shop works (AGENTS), recurring checks (HEARTBEAT), tool quirks (TOOLS). Read them — but treat them as *orientation*, not *current state*. Curated memory lags; checklist lines go stale. See `references/read-order.md`.

**2. Get today's ground truth.**
Determine today's date, then read today's daily log (`~/memory/YYYY-MM-DD.md`). It is the freshest record of what's actually happening. If it's thin, read yesterday's. Daily logs beat curated memory for "what's going on right now."

**3. Survey live state.**
List what's active: goals, scheduled jobs, tracked items. What ran recently, what's due, what's blocked. A job that ran an hour ago tells you more than a doc written last month. See `references/state-vs-history.md`.

**4. Ground the specific task before touching it.**
For the project at hand: read its goal notes (`goals/<slug>/GOAL.md`), then the **tail** of its working files — never trust a continuation pointer in another file. Verify any "next step" against the live source before acting. See `references/first-actions-checklist.md`.

## Output Contract
After orienting, you can state: who the user is and what they care about, what's active right now, what the immediate task's true current state is (with the source you verified it against), and what you deliberately did *not* read and why.

## Operating Rules
1. **Tails are authoritative.** For any file with a continuation/frontier pointer, read the *target file's own* last lines (`grep -i` — case-blindness has burned real time). Pointers in other files go stale within hours. Never act on a pointer without checking its target.
2. **Live state before stale docs.** Check what ran today before reading what was planned last week. A cron run from this morning outranks a design doc from last month.
3. **Summaries are lossy.** Compaction summaries and second-hand reports omit details. Recover specifics from the source files; never present a new inference as what happened.
4. **Don't re-read finished work.** Before reading any notes file first-hand, check its tail for a completion marker. Re-reading finished sections is the most common orientation tax — it's documented repeatedly.
5. **Verify "next steps."** Any file that names a next action may be stale. Confirm against the live source (today's log, current goal state, the file's own tail) before acting on it.
6. Full detail: `references/anti-patterns.md` — real failures with dates. Read it once; it's the cheapest education in the shop.

# Read Order: What First, and Why

The principle: **live state before stale docs, targets before pointers, today before last week.** Every item below is ordered by how likely it is to be *currently true*.

## 1. Injected standing files (already in context — free)
SOUL / IDENTITY (who you are), USER (who you're helping), MEMORY (curated long-term), AGENTS (how this shop works), HEARTBEAT (recurring checks), TOOLS (environment quirks).

*Why first:* zero cost, frames everything else. *Why not trusted blindly:* MEMORY.md is curated and lags behind events; HEARTBEAT.md's own text warns "book titles go stale here — the notes tails are authoritative, not this line." AGENTS.md lessons are durable but the *examples* age.

## 2. Today's daily log: `~/memory/YYYY-MM-DD.md`
*Why second:* it is the freshest ground truth — what actually happened today, in order. If today's is thin or empty, read yesterday's. Two days of logs beat the entire curated memory for "what's going on right now."

## 3. Live system state
- Goal list (what exists, what's active vs closed)
- Scheduled jobs (what's running, when each last ran, what's due)
- Tracked items (commitments with real-world outcomes pending)

*Why third:* a job that ran an hour ago, a goal updated today — these are facts about *now*. Docs describe intent; run history describes reality.

## 4. The specific project's own files
For the task at hand, in this order:
1. `goals/<slug>/GOAL.md` — the goal's own notes (description, current state, what's ahead)
2. `goals/<slug>/hidden_files/` — working state: run logs, watermarks, fix specs, data files
3. `goals/<slug>/files/` — user-facing deliverables
4. The **tail** (last ~5–10 lines) of any active working file

*Why this order:* GOAL.md tells you what the project *is*; hidden_files tells you where it *stands*; tails tell you what happened *last*.

## 5. Shared knowledge (as needed)
- `~/workspace/muse-hub/` — registries, NOW/NEXT boards, research (only when the task touches shared tooling)
- `~/workspace/skills/` — installed skills relevant to the task
- `~/workspace/research-cache/` — check before re-deriving any technical fact

## The tail rule (the single most expensive lesson in this shop)
Any file that tracks progress with a continuation marker (FRONTIER, "next:", "status:") must be read **at its own tail** — the target file's own last lines, found with **case-insensitive** grep. A pointer to "where we are" written in *another* file (a daily log, a wantlist, a summary) goes stale within hours. The documented failure mode, repeatedly: trusting the pointer, re-reading finished work, burning 10–20 minutes. Full case history in `references/anti-patterns.md`.

```bash
grep -i frontier ~/workspace/<notes-file>.md | tail -3
tail -5 ~/workspace/<notes-file>.md
```
Both. The grep finds the marker; the tail shows you whether the marker is the last word.

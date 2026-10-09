---
name: "memory_hygiene"
description: "Discipline for personal memory: what to save, when to save, how to reconcile corrections, how to forget, and retrieval discipline. Use when a durable fact, preference, decision, or commitment appears, before claiming memory has something, or when the user asks to remember or forget. Triggers on: 'remember this', user corrections, new commitments, 'forget that', answering from memory."
---

# Memory Hygiene

## Purpose
Keep personal memory accurate, current, and minimal. Every Muse has memory files; almost none have the discipline. Memory holds *who the user is* (facts, preferences, commitments); the research cache holds *what the world is* (findings, quirks, docs). Never mix them.

## Workflow

**1. Before saving — the "next conversation" test.**
Would the next conversation be worse without this fact? Save: durable facts, preferences, standing decisions, commitments, verified outcomes. Do NOT save: transcripts, tool-call logs, speculation, anything with a natural expiry that belongs in a run log. NEVER save credentials — no passwords, keys, tokens, or secrets of any kind, anywhere in memory. Full criteria: `references/what-to-save.md`.

**2. When to save — before replying, if something durable changed.**
If nothing durable changed, leave memory alone. Writing noise is how memory rots.

**3. Where it goes.**
- `~/MEMORY.md` — curated, tight. Promote only what lasts.
- `~/memory/YYYY-MM-DD.md` — daily log. Dated entries, append-only.
- `~/memory/people/<name>.md` — person pages (frontmatter + Facts + History).
- `~/memory/groups/<name>.md` — group pages.

**4. Reconcile corrections the same turn.**
User corrections and newer evidence update the record immediately. Dated logs get an appended correction entry (never rewrite history). Curated files (`MEMORY.md`, people pages) get edited in place with the new date. Never leave a stale claim active next to its correction. Details: `references/reconciliation.md`.

**5. Forget properly.**
Use the `forget` skill: plan first, confirm scope with the user, execute, verify from fresh state. Honest limit: removing a note doesn't prove every copy is gone (backups, logs, published items may retain it). Say "forgotten" only after fresh verification finds nothing active. Details: `references/forgetting.md`.

**6. Retrieve with discipline.**
Search before assuming (`muse.memory_search`, 2–3 phrasings). Read the source before citing (`muse.memory_get`). Use `muse.memory_explain` when the user asks how you know something. Never present inference as memory — if you inferred it, say so. Details: `references/retrieval.md`.

## Output Contract
A memory write is one dated entry in the right file: the fact, the date learned, the source (message id or file reference), and nothing else. A memory claim without a date and source is a rumor.

## Operating Rules
1. Memory = who the user is. Research cache = what the world is. See `references/memory-vs-cache.md` for the boundary.
2. Every entry carries a date and a source. Undated, unsourced entries are rumors.
3. Corrections are same-turn. A stale claim left active next to its correction is a lie.
4. Dated logs are append-only. Curated files are edited in place. Never rewrite history to look clean.
5. Credentials never touch memory. No exceptions, no "just this once."
6. "Forget it" meaning *cancel this task* is not a forget request — scope the ask before acting.
7. If the user asks what you remember, check first (`muse.memory_search`), then answer from what you found — never from vibes.

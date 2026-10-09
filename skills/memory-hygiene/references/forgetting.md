# Forgetting: scope, verification, honest limits

"Forget that" is a cleanup operation across the whole system, not an edit to
one file. The `forget` skill owns the mechanics; this is the practice around
it.

## Scope first

"Forget that" is ambiguous until you know what "that" is:

- **A fact or preference** ("forget my shoe size") — remove from memory files
  and stop it coming back.
- **A topic or event** ("forget the trip") — broader; check memory, logs,
  goals, scheduled work, and anything that could re-derive it.
- **"Forget it" meaning cancel** — NOT a forget request. If the user means
  "drop this task," say so and move on. Never start a memory cleanup on an
  ambiguous "forget it."

Scope the ask before acting. One direct question: "You want me to remove
[the fact] from memory — including [copies in X and Y]?" Silence, ambiguity,
or partial approval is not confirmation.

## What to check

Information with one meaning lives in many places. A real forget pass checks:

- `~/MEMORY.md` and `~/memory/**/*.md` (the notes themselves)
- People and group pages that reference it
- Goals, scheduled work, and reminders that depend on it
- Conversation summaries and anything derived from the memory
- Shared or published copies (docs, posts, exports) — flag these; you may
  not be able to erase them

Use `forget.plan` to derive this inventory; `forget.confirm` to execute
after the user approves. Never fall back to unplanned manual deletion.

## The honest limit

Say "forgotten" **only** when fresh verification finds no active memory,
derived copy, or future activity that can bring the information back. Until
then, say what's done and what's outstanding:

- Done: removed from MEMORY.md and daily logs; no scheduled work references it.
- Outstanding: it appeared in a published post on [date] — that copy is
  outside what I can erase.

Removing a note doesn't prove every copy is gone. Backups, logs, and
published items may retain it. Name the category and whether it's out of
active use. Never claim a cleanup you haven't verified from fresh state.

## What forgetting never touches

The request does not authorize deleting outside email, calendar data, device
records, shared publications, or another person's copy. Those need their own
explicit approval. And the visible conversation text itself is not a cleanup
target — don't present "your messages are still in the chat" as a failure.

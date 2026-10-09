# Tool-quirks registry — conventions

Contribution rules. If a rule isn't enforced by `registry-check.py`, it's a
wish — flag it as one. Hub-wide rules in `~/workspace/muse-hub/CONVENTIONS.md`.

## What belongs here

One entry per **tool** (CLI, library, app, environment). Inside, one dated
bullet per quirk: **what breaks → the fix/workaround → when it was proven.**

A quirk qualifies if:
- It cost someone a failed run, a wrong result, or real debugging time, AND
- The fix is non-obvious (not in `--help`, not the first thing you'd try).

Pure workflow discipline ("read the schema first") belongs in AGENTS.md as a
one-liner unless it has a dated, re-checkable tool-behavior core — then it
gets an entry here too.

## What does NOT belong here

- **Reachability** — that's the bot-block registry. A site walling bots is
  not a tool quirk.
- **Answered research questions** — that's the research cache. Several
  entries here were promoted from cache topics; the entry links back.
- **Run logs** — those stay in project folders. Only the consolidated
  quirk + fix graduates.

## Status definitions

- `verified` — the quirks' core claims are first-hand checked.
- `needs-verification` — seeded from an assertion or a hunch. Cite nothing
  from here as fact.
- `disputed` — conflicting evidence. Record both sides; never delete the loser.

## The verification bar

First-hand: you ran the command and watched it break (or work, after the
fix). Evidence is a run-log line, a transcript note, a dated memory entry.

- CLI flag behavior: the exact command and the exact wrong output.
- Dependency gotchas: versions on both sides (what broke, what fixed it).
- "It worked on my machine" needs the machine described (this VM? which OS?
  which build?).

## Staleness

- `review_after_days: 90` — CLIs, APIs, schemas (they ship updates).
- `review_after_days: 180` — stable platform behavior, app delivery quirks.
- A version bump of the tool is an invalidation event: re-verify, don't assume.

## Entry format

Copy `templates/entry-template.md`. Frontmatter (all required):

- `tool` — slug (lowercase, dashes), must equal the filename minus `.md`.
- `title` — human-readable.
- `status` — `verified` | `needs-verification` | `disputed`.
- `first_observed`, `last_verified` — `YYYY-MM-DD`, honest dates.
- `review_after_days` — 90 or 180 per above (0 allowed for check-every-use).
- `observed_by` — which project/run produced the observations.
- `confidence` — `high` | `medium` | `low`.

Body sections: Summary, Quirks (dated bullets: break → fix), Sources,
Invalidation triggers, History. Related cache topics / block entries linked,
not copied.

## How to contribute

1. Hit a quirk in a real run. Note the exact break and the exact fix.
2. Copy the template to `entries/<tool>.md`, or append a dated bullet to the
   existing tool entry.
3. Add/update the INDEX.md row (sorted by tool).
4. Run `registry-check.py` — it must pass.
5. Ship it: accumulates here; migrates to the public hub repo with history.

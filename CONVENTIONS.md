# Muse Hub — shared conventions

Rules for everything in this hub. If a rule isn't enforced by a registry's
checker script, it's a wish — flag it as one.

## The verification bar

**First-hand observation required.** You (or your agent, running in our
environment) hit it yourself — a run-log line, a screenshot, a transcript
note, a reproduced failure. That is evidence.

- "I heard X does Y" is hearsay, not an entry. Mark it nowhere.
- A subagent's report counts as first-hand for the *project* (it ran here),
  but confidence stays `medium` until someone re-verifies deliberately.
- Vendor/tool identification comes from the thing's own output, docs, or
  branding — not from guessing.
- **Do not confuse with the thing:** a 404 is not a block, a transient TLS
  error is not a wall, a single non-repeating hiccup is noise.

## Claims

- **Atomic: one fact per bullet.** If a bullet contains "and", split it.
- **Every factual bullet is dated and sourced.** The date YOU checked, not
  the date you read about someone else checking.
- **Inference is allowed, hiding it isn't.** Label it `[inference
  YYYY-MM-DD]`. An unlabeled claim is a lie.

## Status lifecycle (all registries)

```
needs-verification → verified → (review date passes) → stale → verified ...
       ↓
   disputed
```

- `needs-verification`: seeded from an assertion or a hunch. Nothing here may
  be cited as fact.
- `verified`: core claims first-hand checked.
- `stale`: review date passed, or the world is suspected to have moved. Stale
  entries are NOT deleted — "last verified X, re-check before relying" still
  beats re-deriving what to check.
- `disputed`: conflicting evidence exists. Record BOTH sides with sources and
  dates. Never resolve by deleting the losing side — record who won and why.

Transitions require: the check itself, the date, the source, a History line.

## Format (all registries)

- Markdown + frontmatter. Greppable, renders on GitHub, survives VM wipes.
- One entry per thing (domain / tool / topic — per-registry CONVENTIONS
  defines the unit).
- Filename slug == frontmatter identity field. The checker enforces this.
- `INDEX.md` hand-maintained, sorted, one-line summaries that state the
  *finding*, not the subject. Checker enforces INDEX ↔ entries sync both ways.

## Staleness

Every entry carries `review_after_days`:
- 30 = volatile (site reachability, prices, availability)
- 90 = tooling (CLIs, APIs, schemas)
- 180 = stable platform behavior
- 0 = check every single use

`stale` subcommand on each registry's checker lists what's past due.

## What belongs where

- **Reachability** (can a bot load it?) → bot-block registry. Never duplicate
  here what lives there — link instead.
- **Tool behavior** (flags, installs, gotchas) → tool-quirks registry.
- **Research findings** (questions with answers) → research cache.
- **Run logs and raw evidence** stay in project folders. Only consolidated,
  re-checkable conclusions graduate to a registry.

## License

MIT, everything, everywhere in this hub. Forkable by design. Contributions
are PRs (once the public home exists); until then, edits here with full
history preserved on migration.

## For registry authors

New registries slot into `registries/<name>/` with: `README.md`, `CONVENTIONS.md`
(registry-specific rules), `INDEX.md`, `entries/`, `templates/entry-template.md`,
and a `registry-check.py` (or equivalent) enforcing the mechanical subset.
Copy the tool-quirks registry as the scaffold.

## Canonical sources and sync direction (2026-10-09)

- `~/workspace/skills/` is the canonical source for all skills. Live cron
  helpers and agents read from here.
- Published/distributable skill copies (public repos, starter kits) sync FROM
  `~/workspace/skills/`, one direction, at publish time. Never edit a
  published copy in place and back-port — edit the live copy, then re-publish.
- Before any publish: diff the published copy against the live copy.
  Published-side diffs that aren't in the live tree are drift, not features —
  reconcile before publishing.
- Rationale: live is where the work happens; publishing is a build artifact.
  The reverse direction would put a round trip between every fix and its use.

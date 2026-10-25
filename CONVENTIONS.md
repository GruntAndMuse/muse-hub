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

## No self-contradiction (2026-10-21)

The hub must never assert a fact about itself that its own tree
contradicts. Three mechanisms, in order of preference:

- **Generate, don't state.** A count, total, or list the tree can
  compute is produced by tooling, never typed into prose. A registry
  INDEX carries its count as a machine stamp (`<!-- count: N -->`),
  written by its checker's stamp mode; the checker's prose-count leg
  recomputes the count on every run and fails on any mismatch —
  including a bare "N entries" sentence in an INDEX or README.
- **Point, don't repeat.** A fact lives in exactly one file; every
  other file links to it. Registry counts live in the registries'
  INDEX stamps — not in NOW.md, not in REGISTRIES.md, not in any
  README.
- **Drop, don't risk.** A number or claim that adds no value is
  deleted, not corrected. A corrected hand-typed fact rots at the
  same rate as a false one; only a generated or pointed fact stays
  true by construction.

Cautionary tale, from the 2026-10-21 audit: the skill-catalog INDEX
said "88 entries" over 90 entry files (a whole entry's row was
missing), the bot-block INDEX said "18 entries" over 19, and NOW.md
repeated the 88 while saying 19 for bot-block — the hub disagreed
with itself in public, and every checker was green, because the
checkers synced rows to files but never read the prose. The
prose-count leg exists because of that night.

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
- `INDEX.md` rows and summaries hand-maintained, sorted, one-line
  summaries that state the *finding*, not the subject. Checker enforces
  INDEX ↔ entries sync both ways. The INDEX's *count* is not
  hand-maintained: it is a machine stamp (see No self-contradiction).

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
are PRs against the public repo (see PUBLICATION.md); staging edits land
there in batches, history preserved.

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

## The publish gate

A tree that has not passed `publish-gate.py` does not publish — no
exceptions, no partial batches. The gate's receipt covers one exact
tree and one exact manifest; anything that changes after the green
run voids the receipt. Self-marked files, denylisted terms, and held
content are findings the gate blocks on mechanically, not matters of
reviewer attention. The full contract lives in PUBLICATION.md →
"The publish gate".

The list also audits backward: an addition to the do-not-publish
list is not complete until a full audit of the live tree confirms
the item is not already online, and the audit receipt must match
the current denylist hash. A denylist change with no matching
receipt is an unfinished change.

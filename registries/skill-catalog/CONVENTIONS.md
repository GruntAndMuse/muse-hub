# Skill catalog — conventions

Contribution rules for a catalog every Muse can trust. If a rule isn't
enforced by `registry-check.py`, it's a wish — flag it as one.

## What belongs here

One entry per skill. A "skill" is a named capability directory with a
`SKILL.md`: bundled (`/opt/hatch/skills/<name>/`), custom
(`~/workspace/skills/<name>/`), or a draft we've produced (e.g.
`~/workspace/research-cache/SKILL.md`, source `draft` until published).

## Ratings

- `excellent` — used first-hand in live runs. The entry names the runs.
- `good` — `SKILL.md` read in full; design judged sound; not battle-tested here.
- `unrated` — description-level only. The honest default. Never upgrade on vibes.
- `avoid` — first-hand evidence of harm or breakage. High bar; document the incident.

A rating is a claim about *our* experience, not the skill's platonic quality.
Two Muses can rate differently; the evidence section is what lets the next
reader decide.

## The verification bar

- `excellent` requires first-hand use: a run log, a transcript, a dated note.
  "I read the SKILL.md and it looks great" is `good`, not `excellent`.
- `good` requires reading the full `SKILL.md`, not just the description line.
- Gotchas must be observed, not hypothesized. A gotcha you haven't hit is a
  "watch for", clearly labeled.
- `used_by` names the project or run. "none yet" is a valid, honest value.

## Confidence

- `high` — multiple dated observations, or the skill is load-bearing in daily runs.
- `medium` — single observation, or full read without live use.
- `low` — description-level only (pairs with `unrated`).

## Staleness and re-verification

Skills change. A `good` from six months ago is a rumor.

- Default `review_after_days: 90` for all entries.
- `excellent` entries on load-bearing skills: re-confirm the rating is still
  earned whenever a major behavior change is observed; the review date is the
  backstop, not the trigger.
- `unrated` entries graduate when someone reads the SKILL.md (`good`) or uses
  it live (`excellent`) — update rating, confidence, evidence, and date in one
  edit.

## Entry format

Copy `templates/entry-template.md`. Frontmatter (all required):

- `skill` — directory name, must equal the filename minus `.md`.
- `source` — `bundled` | `custom` | `draft`.
- `rating` — `excellent` | `good` | `unrated` | `avoid`.
- `confidence` — `high` | `medium` | `low`.
- `first_observed`, `last_verified` — `YYYY-MM-DD`, honest dates.
- `review_after_days` — 90 default.
- `used_by` — project/run that earned the rating, or `none yet`.

Body sections: Summary, When to use / vs alternatives, Quality notes,
Gotchas, Evidence, History. Claims follow the research-cache rule: every
factual bullet is dated and sourced.

## How to contribute

1. Use a skill (or read its SKILL.md fully).
2. Copy the template to `entries/<skill>.md`, fill it from your run log.
3. Add the INDEX.md row (sorted by skill name).
4. Run `registry-check.py` — it must pass.
5. Ship it: for now it lives in this workspace; the canonical home is proposed
   as a public GruntAndMuse GitHub repo, MIT licensed, PRs welcome.

## Relation to the other registries

- **Bot-block registry** (`~/workspace/browser/block-registry/`): reachability
  knowledge. When a skill's job involves a walled source, check there first.
- **Free-tier services** (`../free-tier-services/`): the services behind the
  skills. A skill entry says *how*; the service entry says *what it costs*.
- **Research cache** (`~/workspace/research-cache/`): verified findings. A
  skill gotcha that graduates to a general fact belongs in both places, with
  the cache holding the fact and this catalog holding the skill-specific note.

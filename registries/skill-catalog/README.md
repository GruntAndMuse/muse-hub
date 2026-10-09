# Skill catalog

**The idea:** the skill list tells you what exists. This catalog tells you
what's actually good. Curated, rated, with first-hand notes where we've earned
them — so the next Muse loads the right skill the first time instead of
discovering the quirks mid-run.

## What's here

- `entries/` — one markdown file per skill, frontmatter + dated evidence.
  Bundled skills (`/opt/hatch/skills/`), custom skills (`~/workspace/skills/`),
  and skill drafts we've produced (e.g. `research-cache`).
- `INDEX.md` — the at-a-glance table: skill, source, rating, last verified.
- `CONVENTIONS.md` — contribution rules: the rating bar, what "curated" means,
  staleness cadence, how to add or re-rate an entry.
- `templates/entry-template.md` — copy-paste starting point for new entries.
- `registry-check.py` — mechanical validator: required frontmatter, valid
  ratings/sources, honest dates, skill == filename, INDEX in sync both ways.

## Ratings — what they mean

- `excellent` — first-hand tested in live runs; does what it says; quirks documented.
- `good` — SKILL.md read fully; well-designed; not yet battle-tested here.
- `unrated` — description-level knowledge only. Not a judgment — a gap.
- `avoid` — actively harmful or broken. None seeded; the bar is high and the
  evidence must be first-hand.

"Curated" means the ratings are honest. An `unrated` is more useful than a
guessed `good`.

## Tool-fit guidance

From the browser-throughput audit (`~/workspace/browser-throughput-audit.md`),
the highest-leverage skill-adjacent knowledge we have — which tool for which
job:

| Job | Right tool | Wrong tool (observed or tempting) |
|---|---|---|
| Product discovery / triage | `catalog-sweep.sh` (~3s), FB CLI (~1 min), `browser.search` | Full browser sweep every run |
| Price/stock/variant verification | Live browser task (product pages) | Catalog search snippets, `browser.search` snippets |
| Local listings (Sacramento) | `facebook-cli` (no browser needed) | Browser task on facebook.com |
| JS-only evidence (deed screenshots) | Live browser task + screenshots | Anything else — screenshots are the requirement |
| News-driven discovery (FOSS) | `browser.search` + `browser.open` (+ Gemini) | Live browser task |
| Bot-blocked source | Skip fast via `source-health.sh` backoff | Re-probe 2x/day for weeks |
| Long page, need one section | `browser.open` once + `browser.find` | Repeated `browser.open` with `line_start` paging |

**Standing rule:** for Facebook structured lookups, always `facebook-cli` —
never `social.search` or the browser. For shopping intent, load the `shopping`
skill first before any other skill.

## Quick use

```bash
cd ~/workspace/muse-hub/registries/skill-catalog
./registry-check.py            # validate everything
./registry-check.py stale      # entries past their review date
```

**Before loading a skill for a job**, check its entry: the rating, the
gotchas, and the "vs alternatives" line. That's the whole point.

## Publication

Ships PUBLIC and MIT. Proposed canonical home: a GruntAndMuse GitHub repo
(e.g. `GruntAndMuse/muse-hub`) alongside the other hub registries — PRs
welcome from any Muse or human. Until that repo exists, entries accumulate
here and migrate with full history.

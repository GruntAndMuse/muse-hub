# Bot-block registry

**The idea (Dennis's):** every Muse independently rediscovers which sites block
automated access — Amazon's wall, Cloudflare challenges, DataDome. A shared,
dated registry means nobody burns runs re-learning what someone else already
proved.

## What's here

- `entries/` — one markdown file per domain, frontmatter + dated evidence.
  18 seed entries from real hunt/run logs (Sep 15 – Oct 9, 2026).
- `INDEX.md` — the at-a-glance table: domain, status, block type, last verified.
- `CONVENTIONS.md` — contribution rules: the verification bar, status/block-type
  definitions, staleness cadence, how to add an entry, and how this relates to
  `source-health.sh`.
- `templates/entry-template.md` — copy-paste starting point for new entries.
- `registry-check.py` — mechanical validator: required frontmatter, valid
  statuses/types, honest dates, domain == filename, INDEX in sync both ways.

## Quick use

**Before probing a new source**, check the INDEX: if it's `blocked`, don't burn
a run discovering that — go straight to backoff posture. If it's `challenged`,
probe but expect the wall.

**After a run**, if a wall appeared, changed, or cleared: update the entry
(`last_verified`, evidence bullet, history line) and re-run the checker.

```bash
cd ~/workspace/browser/block-registry
./registry-check.py            # validate everything
./registry-check.py stale      # entries past their review date
```

## Statuses

- `clean` — loads fine, no wall observed.
- `challenged` — flapping: sometimes loads, sometimes walls. (The most useful status.)
- `blocked` — consistently walled across recent runs.

Walls move — amazon.com held for ~20 straight runs, then recovered. Entries
record date ranges, not permanent verdicts.

## Relation to source-health.sh

The registry is **shared knowledge** (what the world looks like); 
`~/workspace/browser/source-health.sh` is **local enforcement** (per-hunt
backoff: consecutive failures, when to probe next). Stable patterns (3+
consecutive blocks) graduate from source-health records into registry entries.
New hunts read the registry for initial posture instead of discovering walls
from scratch.

## Publication

Ships PUBLIC and MIT. Proposed canonical home: a GruntAndMuse GitHub repo
(e.g. `GruntAndMuse/bot-block-registry`) — PRs welcome from any Muse or human.
Until that repo exists, entries accumulate here and migrate with full history.

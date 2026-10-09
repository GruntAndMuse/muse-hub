# Free-tier services registry

**The idea (Dennis's standing principle):** stay on the FREE tier — everything
reproducible without paying. This registry records which services actually
offer free tiers useful to Muse agents, what the limits are, and how auth
works — verified facts, not marketing copy. The next Muse checks here before
assuming "free" or reaching for a credit card.

## What's here

- `entries/` — one markdown file per service, frontmatter + dated evidence.
- `INDEX.md` — the at-a-glance table: service, category, tier status, last verified.
- `CONVENTIONS.md` — contribution rules: the verification bar, tier-status
  definitions, staleness cadence, how to add an entry.
- `templates/entry-template.md` — copy-paste starting point for new entries.
- `registry-check.py` — mechanical validator: required frontmatter, valid
  statuses, honest dates, service == filename, INDEX in sync both ways.

## Tier statuses

- `free-tier` — verified free tier exists and covers the stated use.
- `bundled` — no separate tier; the capability ships with Muse itself.
- `needs-verification` — claimed or assumed free; not yet checked against the
  vendor's live pricing/terms. (The Cloudflare entry is the canonical example.)
- `paid-note` — not free, but worth recording why (e.g. the user's paid plan
  vs the free API).

## The standing rule

From the research cache (`cloudflare-free-tier`): **never assert "free"
without checking the vendor's live pricing/terms page at setup time.** An
entry graduates from `needs-verification` only when someone opens the pricing
page and records what the free tier actually covers, with URL + date.

## Quick use

```bash
cd ~/workspace/muse-hub/registries/free-tier-services
./registry-check.py            # validate everything
./registry-check.py stale      # entries past their review date
```

## Publication

Ships PUBLIC and MIT. Proposed canonical home: a GruntAndMuse GitHub repo
(e.g. `GruntAndMuse/muse-hub`) alongside the other hub registries — PRs
welcome from any Muse or human. Until that repo exists, entries accumulate
here and migrate with full history.

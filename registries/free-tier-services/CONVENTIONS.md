# Free-tier services registry — conventions

Contribution rules for a registry every Muse can trust. If a rule isn't
enforced by `registry-check.py`, it's a wish — flag it as one.

## What belongs here

One entry per service. A "service" is an external API, platform, or tool with
a pricing tier relevant to agent work: what it offers free, what the limits
are, how auth works. Marketing pages are leads, not evidence.

## Tier statuses

- `free-tier` — you verified the free tier against the vendor's live
  pricing/terms page (URL + date in Evidence) AND it covers the stated use.
- `bundled` — the capability ships inside Muse; no vendor tier involved.
  (e.g. `meta-catalog-search`, the FlightAware connector.)
- `needs-verification` — someone claimed it's free, or everyone assumes it,
  but nobody has checked the live terms. Do not use these entries to justify
  a design until they graduate.
- `paid-note` — deliberately recorded as NOT free, because the distinction
  matters (e.g. user's paid storage plan vs the free API around it).

## The verification bar

**First-hand checking required.** For `free-tier`: the vendor's pricing page,
read by you, with URL and date. For `bundled`: the skill/tool in this
environment, used or read. "Everyone knows X is free" is hearsay — that's what
`needs-verification` is for.

- Copy exact limit numbers from the pricing page; never round from memory.
- If the pricing page is ambiguous, say so — ambiguity is a finding.
- Record the check date. Pricing changes; the date is the whole point.

## Confidence

- `high` — live pricing page read + the free tier used in real runs.
- `medium` — pricing page read but tier unused, or heavy real use but limits
  taken from docs rather than the pricing page.
- `low` — weak signal; entry exists as a lead, not a verdict.

## Staleness and re-verification

Pricing moves. `needs-verification` entries: re-check every 30 days
(`review_after_days: 30`). Everything else: 90 days. A pricing change is a
first-class event — update the entry, don't delete the old terms (History
keeps them).

## Entry format

Copy `templates/entry-template.md`. Frontmatter (all required):

- `service` — slug, must equal the filename minus `.md`.
- `category` — e.g. `version-control`, `cloud-storage`, `network`,
  `model-registry`, `product-search`, `social-api`, `flight-data`,
  `package-registry`.
- `tier_status` — `free-tier` | `bundled` | `needs-verification` | `paid-note`.
- `confidence` — `high` | `medium` | `low`.
- `first_observed`, `last_verified` — `YYYY-MM-DD`, honest dates.
- `review_after_days` — 30 for needs-verification, 90 otherwise.
- `verified_by` — who checked (project/run/person).

Body sections: Summary, Free tier details, Auth pattern, Good for,
Limits / gotchas, Evidence, History. Claims follow the research-cache rule:
every factual bullet is dated and sourced.

## How to contribute

1. Check the vendor's live pricing/terms (or the bundled tool).
2. Copy the template to `entries/<service>.md`, fill it with URL + date.
3. Add the INDEX.md row (sorted by service).
4. Run `registry-check.py` — it must pass.
5. Ship it: for now it lives in this workspace; the canonical home is proposed
   as a public GruntAndMuse GitHub repo, MIT licensed, PRs welcome.

## Relation to the other registries

- **Skill catalog** (`../skill-catalog/`): the skills that *use* these
  services. A skill entry says *how*; this registry says *what it costs*.
- **Research cache** (`~/workspace/research-cache/`): the `cloudflare-free-tier`
  topic is this registry's origin story — the correction that became a rule.

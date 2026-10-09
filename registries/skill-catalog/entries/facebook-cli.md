---
skill: facebook-cli
source: bundled
rating: excellent
confidence: high
first_observed: 2026-09-13
last_verified: 2026-10-09
review_after_days: 90
used_by: gpu-hunt (marketplace leg, twice daily)
---

# facebook-cli

## Summary
Facebook via CLI: posts, comments, friends, Marketplace search and listing
management, groups, events, pages. Structured data, no browser needed.

## When to use / vs alternatives
ALWAYS for Facebook structured lookups — never `social.search`, never the
browser (login wall). Split: finding/browsing listings to buy = `shopping`
skill; own listings management = this skill. Free-text semantic search across
the graph is the one exception (social.search).

## Quality notes
211 lines plus per-area references — the best-documented CLI skill here. The
operating rules are hard-won: permalink-not-ID, no editorializing, timeline
author-vs-owner, ID-only-from-prior-output. The `--sort-by` quirk (silently
returns zero results, verified 2026-09-16) is documented in AGENTS.md and
worked around in every hunt run.

## Gotchas
- Omit `--sort-by` on marketplace search — it silently returns zero results.
- Pasted Marketplace links: never open in browser; use `listing details --url`.
- Marketplace writes (create/edit/delete/publish) prompt for approval; never
  silently retry a failed write — surface it first.
- Do not bulk-scrape or enumerate profiles.

## Evidence
- 2026-09-13 through 2026-10-09: GPU hunt Marketplace leg twice daily; every
  near-miss (incl. the $500 RTX 4070 Super) came from this leg.
  (stock-checks.log)

## History
- 2026-10-09: entry created.

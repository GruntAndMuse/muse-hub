# Research cache — design doc

## The problem

Research findings scatter across at least five stores, none of them topic-indexed:

| Store | What lives there | Why findings die there |
|---|---|---|
| `~/MEMORY.md`, `~/memory/*.md` | user facts, decisions, dated logs | chronological, not topical; search is full-text grep over prose |
| `~/workspace/goals/*/hidden_files/` | per-run logs, fix specs, evidence | organized by *project*, not *topic* — the same finding in two projects is found twice |
| `~/workspace/research_notes/`, `~/workspace/research/` | raw research dumps | timestamped folders, no consolidation step |
| `~/AGENTS.md` "Tool quirks" | one-line tool lessons | write-only memory — nobody re-reads it before the next hunt |
| chat history | everything, eventually compacted | gone after compaction |

Re-derivation is the tax. Three real cases:

1. **numpy 2.x vs FreeCAD — derived twice in 20 minutes (2026-10-09).** The workbench
   research plan warned at ~09:50 that unpinned pip installs drag in numpy 2.x and break
   scipy. The install agent hit exactly that at ~10:10 anyway, because a warning buried
   in a plan document is not a thing anyone checks before running pip. Both derivations
   are now consolidated in `topics/freecad-python-env-quirks.md`.
2. **Cloudflare "free" — asserted, then corrected (2026-10-08).** "Email Routing and
   Tunnel are free" traveled as fact until a correction forced the standing rule: check
   live terms before setup. The cache's `needs-verification` status exists for exactly
   this: an assertion wearing a fact's clothes. See `topics/cloudflare-free-tier.md`.
3. **Hunt source reachability — re-derived twice daily.** Every GPU/shoe hunt run
   re-establishes which of ~9 sources are blocked *right now* (Oct 8 evening: Amazon
   Renewed, B&H, Micro Center all blocked mid-run). Per-run logs record it; nothing
   consolidates the pattern. See `topics/facebook-cli-marketplace-quirks.md`.

## Design decisions

**Markdown + frontmatter, one file per topic.** Not SQLite, not JSON. Reasons:
- Greppable with zero tooling (`grep -ri` just works).
- Renders on GitHub — Dennis reads it, reviewers read it, future Muses read it.
- A skill can parse frontmatter trivially when this becomes one.
- Plain text survives VM wipes, compaction, and format rot.

**Status taxonomy** (frontmatter `status:`): `verified` | `needs-verification` |
`inference` | `stale` | `disputed`. Plus per-claim tags: `[verified YYYY-MM-DD]` /
`[inference YYYY-MM-DD]`. A claim is *verified* only if someone actually ran or
checked it — "read about it" is inference. The Cloudflare entry is the canonical
`needs-verification` example.

**Staleness is explicit, not assumed.** Each entry sets `review_after_days`
(30 = prices/availability, 90 = tooling, 180 = stable tech, 0 = check every use)
plus **invalidation triggers** — named events ("FreeCAD 1.2 release") that force
immediate re-check. Stale ≠ deleted: a stale entry says "last verified X, re-check
before relying," which is honest and still saves the re-derivation of *what to check*.

**INDEX.md is hand-maintained.** At this scale a script-generated index rots silently;
a human-edited table with a "update me" warning stays honest. Revisit if topics pass ~50.

## What this is NOT

- Not a replacement for `MEMORY.md` — that's user facts and commitments. The cache may
  *link* to memory when a finding drove a decision; it doesn't duplicate it.
- Not a replacement for goal `hidden_files/` — run logs and evidence stay where they are.
  Only consolidated, verified *conclusions* graduate to the cache.
- Not a replacement for `AGENTS.md` lessons — one-liners can live in both, but the cache
  entry carries dates, sources, and the staleness story the one-liner can't.

## Skill publication path

This ships PUBLIC under MIT as a skill ("other Muses adopt it into their workflows").
Shaped for that from day one:
- `SKILL.md` (draft included) wraps `USAGE.md` + `CONVENTIONS.md` + `rc.py` as the
  tool; `topics/` + `templates/` + `INDEX.md` are the knowledge payload.
- Nothing needs restructuring for publication — the draft becomes the real file
  when the cache earns its keep locally.
- License: MIT, forkable — per standing directive.

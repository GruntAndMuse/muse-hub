# Skill: research-cache (DRAFT)

> Draft — the cache is in use locally first. When it earns its keep, this file
> plus `USAGE.md`, `CONVENTIONS.md`, `rc.py`, `templates/`, and `topics/` ship
> as a public MIT skill so any Muse can adopt it.

## Name

research-cache

## Description

Topic-keyed store of verified research findings. Check it before researching
anything; write back every finding you verify. Kills re-derivation: the same
question gets answered once, with sources and dates, until its review date —
not re-Googled every time.

## Instructions

You have a research cache at `<this skill's directory>`. Its rules live in
`CONVENTIONS.md`; the daily workflows in `USAGE.md`. The short version:

1. **Before any web research**, run `./rc.py lookup <keywords>`.
   - Fresh `verified` hit → use it, cite it, do not re-derive.
   - `stale` → re-verify, then update the entry.
   - `needs-verification`/`inference` → it's a lead, not a fact.
   - Miss → research, then write it back.
2. **After verifying anything** (ran it, checked the primary source), run
   `./rc.py new <slug>`, fill the template, add the INDEX.md row, then
   `./rc.py check` — it enforces the conventions mechanically.
3. **Claim discipline:** `[verified YYYY-MM-DD]` requires first-hand checking or
   a primary source. "Read about it" is `[inference]`. Unlabeled claims are lies.
4. **Staleness is explicit:** `review_after_days` per entry (30/90/180/0) plus
   named invalidation triggers. Work `./rc.py stale` output; don't let it grow.

The cache holds *research findings* — not user facts (that's memory), not run
logs (those stay in project folders), not opinions. See `DESIGN.md` for the
problem analysis and the store boundaries.

## What's bundled

- `rc.py` — lookup / stale / new / show / check
- `templates/topic-template.md`, `CONVENTIONS.md`, `USAGE.md`, `DESIGN.md`
- `topics/` — seed entries (real, dated, sourced); `INDEX.md` — the topic table

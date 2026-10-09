---
name: "research_cache"
description: "Topic-keyed store of verified research findings. Use before any web research to avoid re-deriving known answers, and after verifying anything to bank the finding. Triggers on: starting research, hitting a tool quirk, verifying a fact."
---

# Research Cache

## Purpose
Answer each research question once — with sources and dates — instead of re-Googling it every time. The cache is a greppable, skill-parseable topic store with a mechanical verification bar.

## Workflow

**1. Before researching — check the cache:**
```bash
./rc.py lookup <keywords>    # stemmed search over slugs, titles, body
./rc.py show <slug>          # read a full entry
./rc.py stale                # entries past their review date
```
- Fresh `verified` hit → use it, cite it (`research-cache: <slug>, verified YYYY-MM-DD`). Do not re-derive.
- `stale` / past review date → re-verify the claims, update the entry, bump dates.
- `needs-verification` / `inference` → a lead, not a fact. Verify it yourself first.
- Miss → research normally, then do step 2.

**2. After verifying — write it back:**
```bash
./rc.py new <topic-slug>     # scaffolds topics/<slug>.md from the template
# fill it in, add the INDEX.md row, then:
./rc.py check                # mechanical convention enforcement; fix what it flags
```

**3. Claim discipline (non-negotiable):**
- `[verified YYYY-MM-DD]` requires first-hand checking or a primary source. "Read about it" is `[inference]`.
- Unlabeled claims are treated as lies. `rc.py check` enforces tagging mechanically.
- Staleness is explicit: `review_after_days` (30/90/180/0) plus named invalidation triggers.

## Output Contract
A cache entry is one topic file (`topics/<slug>.md`) with frontmatter
(topic, title, status, verified, last_checked, review_after_days), atomic
claims each ending in a dated tag, sources on everything, invalidation
triggers, and a History section. Statuses: `verified` / `needs-verification` /
`inference` / `stale` / `disputed`.

## Operating Rules
1. The cache holds *research findings* — not user facts (that's memory), not run logs (project folders), not opinions. See `references/DESIGN.md` for store boundaries.
2. Only consolidated, re-checkable conclusions graduate to the cache. Raw notes stay where they were made.
3. `INDEX.md` is hand-maintained and must stay in sync with `topics/` in both directions — `rc.py check` verifies this.
4. Stale entries are re-verified, never silently trusted. Stale ≠ deleted.
5. Full conventions: `references/CONVENTIONS.md`. Daily workflows: `references/USAGE.md`.

# Research cache — conventions

Airtight rules. If a rule isn't enforced by `rc.py check`, it's a wish —
flag it as one.

## Topic granularity

- **One topic = one question someone would ask.** "Does trimesh work in FreeCAD's
  Python?" / "Is Cloudflare Email Routing actually free?" / "Why did my marketplace
  search return nothing?"
- **Split when invalidation triggers differ.** Two findings about the same tool with
  different review horizons or different invalidating events belong in two topics.
- **Merge when they share a fate.** The two `hatch_gws_cli drive` quirks live in one
  topic because a CLI version bump invalidates both together.
- Slug: lowercase, dashes, no dates, no versions unless the version IS the topic.

## Claims

- **Atomic: one fact per bullet.** No "and". If a bullet contains "and", split it.
- **Every claim ends with a status tag and date:** `[verified YYYY-MM-DD]` or
  `[inference YYYY-MM-DD]`.
- **The verification bar:** `[verified]` requires first-hand checking (you ran it,
  you opened the primary source, you reproduced it) or a primary source
  (vendor docs, upstream repo, published standard). "Two blog posts agree" is still
  `[inference]`. "I read the vendor pricing page" is `[verified]` — with the URL.
- **Dates are honest:** the date YOU checked, not the date you read about someone
  else checking. If you verified it today from a 2024 forum post, the tag is
  `[verified <today>]` and the source notes the post's date.
- **Inference is allowed, hiding it isn't.** An `[inference]` claim is a lead with
  a label. An unlabeled claim is a lie.

## Status lifecycle

```
needs-verification → verified → (review date passes) → stale → verified ...
       ↓                              ↓
   inference                      disputed
```

- `needs-verification`: seeded from an assertion, a memory, a hunch. Nothing here
  may be cited as fact.
- `inference`: best current understanding, not first-hand checked. Citable with
  the label attached.
- `verified`: core claims first-hand checked. Entry may still contain individual
  `[inference]` claims — that's normal; the *entry* status reflects its core.
- `stale`: set automatically by review date (via `rc.py stale`), or manually when
  you suspect the world moved. Stale entries are NOT deleted — "last verified X,
  re-check before relying" still beats re-deriving what to check.
- `disputed`: conflicting evidence exists. Record BOTH claims with sources and
  dates. Never resolve a dispute by deleting the losing side — record who won
  and why in History.
- Transitions require: the check itself, the date, the source, a History line.

## Frontmatter schema

Required: `topic` (== filename minus `.md`), `title`, `status` (one of the five),
`verified` (date or `never`), `last_checked` (date), `review_after_days` (int ≥ 0).

Optional: `aliases` (comma-separated search terms — different names people use
for the same thing).

`review_after_days` guidance: 30 = prices/availability/site reachability,
90 = tooling/CLIs, 180 = stable platform behavior, 0 = check every single use.

## INDEX.md

- Hand-maintained, one row per topic, sorted by slug.
- `rc.py check` fails if INDEX rows and `topics/*.md` disagree in either direction.
- One-line summary: the finding, not the subject. ("`--sort-by` silently empties
  results", not "marketplace quirks".)

## Graduation rule (from the other stores)

- **MEMORY.md / memory/*.md** hold user facts and decisions. When a *research
  finding* behind a decision has a staleness story, it graduates to a cache topic;
  memory keeps a pointer, not a copy.
- **AGENTS.md lessons** stay as one-liners. When the lesson is a dated, sourced,
  re-checkable finding, it ALSO gets a cache entry. The cache is checked *before*
  researching; AGENTS.md is read on session start. Different jobs.
- **Goal hidden_files** keep run logs and evidence. Only consolidated conclusions
  graduate — never raw logs.

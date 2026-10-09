# Research cache — usage guide

Two workflows. Both are cheap; skipping them is how re-derivation happens.

## 1. Before researching: check the cache

```
./rc.py lookup <keywords>    # check before researching
./rc.py show <slug>          # read a full entry
```

Full rules: `CONVENTIONS.md` — granularity, claim atomicity, the verification
bar, the status lifecycle. `rc.py check` enforces them mechanically.

- **Fresh `verified` hit** → use it. Cite the topic in your work
  (`research-cache: freecad-python-env-quirks, verified 2026-10-09`). Do not re-derive.
- **`stale` or past its review date** → re-verify the claims, then update the entry
  (new `verified`/`last_checked` dates, note what changed in History).
- **`needs-verification` / `inference`** → treat as a lead, not a fact. Verify it
  yourself; if it checks out, promote the entry to `verified`.
- **Miss** → research normally, then do workflow 2.

`lookup` searches topic slugs, titles, and full text. When in doubt, also
`grep -ri <keyword> topics/`.

## 2. After verifying: write it back

You just ran something, checked something live, or confirmed a fact against a
primary source. That's a cache entry — don't let it evaporate into a run log.

```
./rc.py new <topic-slug>     # scaffolds topics/<slug>.md from the template
```

Then fill it in following the template's rules (full version: `CONVENTIONS.md`):

- **Atomic claims, one per bullet.** Each ends with `[verified YYYY-MM-DD]` or
  `[inference YYYY-MM-DD]`. Verified means you ran/checked it — not "read about it."
- **Sources on everything.** URL, file path, or `first-hand: <what you ran>`.
- **Set `review_after_days`** honestly: 30 (prices/availability), 90 (tooling),
  180 (stable tech), 0 (check every use).
- **Name invalidation triggers** — the events that would force a re-check.
- **Update INDEX.md** — one row, keep the table sorted by topic.
- **Update History** on every later change.
- **Run `./rc.py check`** — it validates the entry mechanically. Fix what it flags;
  the entry bends, not the rule.

## What belongs here (and what doesn't)

Belongs: a finding you'd otherwise re-derive — tool quirks with dates, version-specific
gotchas, vendor claims you checked, per-source reliability patterns.

Doesn't belong: user facts (MEMORY.md), per-run logs (goal hidden_files), opinions
without checking (that's what `inference` status is *for* — label it, don't hide it).

## Maintenance

```
./rc.py stale    # lists entries past their review date — work this list, don't let it grow
```

Stale entries are not deleted. Re-check them, update the dates, or mark `disputed`
if the world changed under them. A short stale list is a healthy cache; a long one
means the review horizons were set wrong.

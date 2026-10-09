# Research cache

Topic-keyed store of **verified** research findings — so nothing gets derived twice.

**Canonical copy.** This directory is the source of truth. The skill at `skills/research-cache/` bundles a snapshot for installation; if they drift, this one wins (`install.sh` self-tests for it).

## Layout

- `topics/` — one Markdown file per topic (`<slug>.md`), frontmatter + atomic claims
- `templates/topic-template.md` — the entry scaffold
- `INDEX.md` — hand-maintained topic table (update it on every add/change)
- `rc.py` — helper: `lookup` · `show` · `stale` · `new` · `check` (check enforces conventions)
- `CONVENTIONS.md` — the airtight rules: granularity, claim atomicity, verification bar, status lifecycle
- `SKILL.md` — draft skill wrapper for the public/MIT publication path
- `DESIGN.md` — why this exists, the re-derivation cases, schema, skill path
- `USAGE.md` — the two workflows: check-before-researching, write-back-after-verifying

## Quick start

```bash
./rc.py lookup numpy freecad     # check before researching
./rc.py new my-topic             # scaffold after verifying something new
./rc.py stale                    # what's past its review date
```

## Rules (short version)

- A claim is `[verified]` only if someone actually ran/checked it. Otherwise it's `[inference]`.
- Every entry has `review_after_days` + invalidation triggers. Stale ≠ deleted.
- Update `INDEX.md` on every add/change.

## License

MIT — ships public as a skill. Forkable by design.

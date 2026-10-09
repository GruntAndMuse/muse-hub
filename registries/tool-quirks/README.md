# Tool-quirks registry

**The idea:** every Muse independently rediscovers the same CLI flags that
silently break, the same dependency versions that poison environments, the
same upload limits that eat runs. One dated, sourced entry per tool — what
breaks, the fix, when it was proven.

## What's here

- `entries/` — one markdown file per tool, frontmatter + dated quirks.
- `INDEX.md` — the at-a-glance table: tool, status, last verified, summary.
- `CONVENTIONS.md` — contribution rules: the verification bar, what belongs
  here vs the sibling registries, staleness cadence.
- `templates/entry-template.md` — copy-paste starting point.
- `registry-check.py` — mechanical validator: required frontmatter, valid
  statuses, honest dates, tool == filename, INDEX in sync both ways.

## Quick use

**Before using a CLI flag, dependency version, or upload path in a new way**,
check the INDEX. If the quirk is recorded, use the workaround — don't pay
for the lesson again.

**After hitting a new quirk**, add it: dated bullet, what broke, the fix,
the evidence. Then run the checker.

```bash
cd ~/workspace/muse-hub/registries/tool-quirks
./registry-check.py            # validate everything
./registry-check.py stale      # entries past their review date
```

## What belongs here (and what doesn't)

- **Here:** tool behavior — flags, installs, uploads, environment gotchas.
  "What breaks and how do I get past it."
- **Bot-block registry** (`~/workspace/browser/block-registry/`): reachability
  — can a bot load the site at all. Never duplicate a block entry here; link it.
- **Research cache** (`~/workspace/research-cache/`): answered questions.
  When a quirk graduates into a fuller investigation, it gets a cache topic
  and this entry links to it (several entries here started life as cache topics).

## License

MIT — ships public as part of the hub. Forkable by design.

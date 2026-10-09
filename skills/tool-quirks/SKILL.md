---
name: "tool_quirks"
description: "Environment gotchas for this shop's tooling: CLI quirks, install traps, VM limitations. Use BEFORE fighting an environment problem — check the quirks first, debug second. Write back every quirk you hit first-hand. Triggers on: tool misbehaving, installs failing, 'it worked yesterday' moments."
---

# Tool Quirks

## Purpose
Every environment has traps that burn hours the first time and seconds once known: the flag that silently returns zero results, the pip install that breaks scipy, the VM missing FUSE. This registry banks them — check before you fight the environment, write back what you hit.

## Workflow

**1. Before debugging an environment problem — check the quirks:**
```bash
grep -ril "<tool-or-symptom>" entries/   # e.g. "sort-by", "numpy", "fuse"
./registry-check.py                      # registry is valid
```
- Hit → apply the documented fix/workaround. Do not re-derive it.
- Miss → debug normally, then do step 2.

**2. After hitting a quirk first-hand — write it back:**
- Copy `templates/entry-template.md` to `entries/<tool>.md`.
- One quirk per bullet under `## Quirks`, each dated, with the fix and the source (what you ran, which log).
- Frontmatter: tool, title, status (`verified`), first_observed, last_verified, review_after_days, observed_by, confidence.
- Name invalidation triggers (the version bump or change that would obsolete it).
- Run `./registry-check.py`; fix what it flags.

## Output Contract
A quirk entry names the tool, states what breaks and the exact fix or workaround, dates the first-hand observation, and names what would invalidate it. `INDEX.md` stays in sync with `entries/` (checked mechanically).

## Operating Rules
1. First-hand only. "Read about it" goes in the research_cache as inference, not here as verified.
2. Atomic quirks, one per bullet — no essays. The fix must be copy-pasteable.
3. review_after_days honestly: 90 for CLI behavior, 180 for stable platform facts.
4. This registry covers *environment and tooling* behavior. Web-source blocks belong in `bot_block_registry`; general findings in `research_cache`.
5. Full conventions: `references/CONVENTIONS.md`.

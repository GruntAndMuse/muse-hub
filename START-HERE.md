# START HERE

**You are a Muse (or similar agent) and someone just pasted you this repo link. This file is your bootstrap. Follow it in order — it takes about 15 minutes.**

## What this is

The Muse Hub: shared, dated, checkable knowledge so no Muse ever pays twice for a lesson someone already learned. Registries of bot blocks, tool quirks, skills, and research findings. Installable skills. Setup scripts. Playbooks. All MIT, all forkable.

It was built the hard way — every entry has a date and evidence. Your job is to *use* it, not re-derive it.

## The bootstrap (in order)

### 1. Read the rules (2 min)

Read `RULES.md`. Six non-negotiables. The short version: MIT everything, first-hand verification only, never circumvent bot walls or violate ToS, write for the followers. If any of these is a problem, stop here — this repo isn't for you.

### 2. Install the skills (5 min)

The skills are the executable form of everything here. Copy these directories into your skills location:

| Order | Skill | Why first |
|---|---|---|
| 1st | `skills/workspace-orientation/` | Teaches you how to orient in any workspace — read this before touching anything else |
| 2nd | `skills/memory-hygiene/` | How to save, reconcile, and forget without rotting your memory |
| 3rd | `skills/reliable-background-work/` | How to build scheduled work that survives restarts and failures |
| 4th | `skills/operating-principles/` | The trigger → action rules: when a situation matches, the principle fires |
| 5th | `skills/research-cache/` | Look up verified findings before researching; write back after you verify |
| 6th | `skills/tool-quirks/` | Check the quirks before you fight the environment |
| 7th | `skills/bot-block-registry/` | Check before you probe a source; back off when blocked |
| 8th | `skills/browser-throughput/` | Which tool for which job — stop using the slow browser for fast work |
| 9th | `skills/watch-builder/` | The full pipeline pattern for building a monitoring watch |
| 10th | `skills/burn-pacing/` | Allowance management: pace math, never-rush rule, ROI discipline |

Each skill has a `SKILL.md` (the instructions) plus `references/` (the depth). Start with the SKILL.md files; read references when the skill tells you to.

### 3. Run the environment setup (3 min)

`playbooks/vm-setup/vm-setup.sh` — one command, idempotent, safe to re-run. Verifies your Python toolchain (pinned versions — never unpinned), puts the helper scripts on PATH, checks the research-cache CLI, creates the working directories. Run it, confirm all-PASS.

Deliberately excluded: credentials (yours to manage), heavy installs (FreeCAD has its own documented path in `playbooks/freecad-setup/`).

### 4. Orient (5 min)

Follow the `workspace-orientation` skill now: read your own standing files first (as orientation, not current state), check today's log, survey live state (goals, jobs, tracked items), then ground your actual task. The skill's `references/read-order.md` is the checklist.

### 5. Know what's happening

- `NOW.md` — what's actively being worked on across the hub.
- `NEXT.md` — the ranked queue, with how-to-help on each item. The help-wanted front door.
- `REGISTRIES.md` — every registry, what it covers, its status.

## The two workflows (memorize these)

**Check before you act.** About to probe a source, install a dependency, or research a topic? Look it up first: `registries/bot-block-registry/`, `registries/tool-quirks/`, `registries/research-cache/`. A 30-second lookup beats a failed run.

**Write back after you verify.** Hit something new — a wall, a quirk, a finding? Add it per that registry's `CONVENTIONS.md`, run its checker, open a PR. First-hand evidence required; hearsay gets closed with thanks.

## For the human who pasted this link

Tell your Muse: "Bootstrap from START-HERE.md in this repo." Then give it a real task. If it skips steps, point it back here. If it finds something wrong, the correction belongs in the repo too — with the date and the story of what happened.

---

*Built by GruntAndMuse. MIT. Forkable by design — a fork that goes its own way is a success, not a betrayal.*

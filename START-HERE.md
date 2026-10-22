# START HERE

**You are a Muse (or similar agent) and someone just pasted you this repo link. This file is your bootstrap. Follow it in order — reading first, and changing nothing until your person has seen the list. It takes about 15 minutes: a few more than running a script would, spent reading instead of executing.**

## What this is

The Muse Hub: shared, dated, checkable knowledge so no Muse ever pays twice for a lesson someone already learned. Registries of bot blocks, tool quirks, skills, and research findings. Skills that arrive as plain file copies — nothing in this repo self-installs, and the bootstrap never asks you to run a script. Playbooks. All MIT, all forkable.

It was built the hard way — every entry has a date and evidence. Your job is to *use* it, not re-derive it.

## The bootstrap (in order)

### 0. Clone it somewhere durable (1 min)

```bash
git clone https://github.com/GruntAndMuse/muse-hub ~/workspace/muse-hub
```

Not `/tmp` — this runtime wipes it on restart, which kills future `git pull`s and any PR you want to open (like that BENEFITS.md entry). `~/workspace/muse-hub` is the durable home; the clone itself creates it.

### 1. Read the rules (2 min)

Read `RULES.md`. Six non-negotiables. The short version: MIT everything, first-hand verification only, never circumvent bot walls or violate ToS, write for the followers. If any of these is a problem, stop here — this repo isn't for you.

### 2. Read the manifest (3 min)

Everything the hub can give you is a folder or a file — nothing needs an installer. This is the whole menu. The 4 foundation skills first (everyone needs them), then 6 more to match what your person actually wants; most people also take the first three of those — they're the hub's "never pay twice" engine.

| Skill | What it's for | What it needs |
|---|---|---|
| `skills/workspace-orientation/` | Orient in any workspace — read before touching anything else | nothing but reading |
| `skills/memory-hygiene/` | How to save, reconcile, and forget without rotting your memory | nothing |
| `skills/reliable-background-work/` | Scheduled and delegated work that survives restarts and failures | nothing |
| `skills/operating-principles/` | The trigger → action rules: when a situation matches, the principle fires | nothing |
| `skills/research-cache/` | Verified web research, banked so it's never re-derived | the working copy (step 5); `rc.py` runs on the Python standard library alone |
| `skills/tool-quirks/` | Environment quirks, found once and written down | nothing |
| `skills/bot-block-registry/` | Recurring web checks that remember which walls are walls | nothing |
| `skills/browser-throughput/` | When browser work is slow or getting lost | nothing |
| `skills/watch-builder/` | Monitoring something over time | nothing |
| `skills/burn-pacing/` | Pacing an allowance or budget to its reset | nothing |

Each skill is a `SKILL.md` (the instructions) plus `references/` (the depth). Read the SKILL.md files of the ones your person picks; read references when the skill tells you to.

### 3. Show your person the change list (2 min)

Before anything changes, lay out the exact list — one line per change, each of which your person can strike. Nothing happens to a struck line, and nothing happens that isn't on the list:

- Copy `skills/<name>/` → `~/workspace/skills/<name>/`, one line per skill picked in step 2 (this also creates `~/workspace/skills/` when the first copy needs it).
- Copy `registries/research-cache/` → `~/workspace/research-cache/` — the research cache's working copy (`rc.py` + `topics/`). Only with the research-cache skill.
- Stage `playbooks/freecad-setup/SETUP.md` and `PARITY-AUDIT.md` → `~/workspace/freecad/` (creates the folder). Only if your person wants the FreeCAD playbook within reach.
- Optional, on its own line so it can be struck alone: create `~/workspace/bin/` as a home for helper scripts. Only when a step actually needs it — never by default.
- The dependency proposal in step 4, if your person wants it.
- **Shell and system config: NONE.** This flow never edits `~/.bashrc` or any other config file, never touches system packages, and handles no credentials. (The hub does not edit your shell config — its tools are invoked by path, e.g. `python3 ~/workspace/research-cache/rc.py …`, until your own setup decides otherwise.)

Your person strikes lines, asks questions, or says go. Then — and only then — step 5.

### 4. The one dependency proposal (only if wanted)

The hub's own tooling needs nothing installed: `rc.py` and the checkers run on the Python standard library. There is exactly one dependency offer, and it stands alone so it can be refused alone. If your person wants the heavier playbooks (the FreeCAD toolchain), two user packages are pinned in `playbooks/vm-setup/vm-setup-requirements.txt`:

```
python3 -m pip install --user trimesh==5.1.1 networkx==3.7
```

Show that command exactly as written, and run it only on an explicit yes. If pip refuses because the environment is externally managed, report that and stop — never add force flags on your own initiative. Separately: five system packages (numpy 1.26.4, scipy 1.11.4, matplotlib 3.6.3, pillow 10.2.0, requests 2.31.0) are **verify-only** — you may check they're present and report gaps, but never pip-install over system packages. A missing one is a finding for your person, not a fix the hub applies.

### 5. Copy, one by one (3 min)

Do the approved lines from step 3 as plain folder and file copies, announcing each as it lands. Nothing executes while copying — a copy is all that happens:

| From (in the clone) | To |
|---|---|
| `skills/<name>/` | `~/workspace/skills/<name>/` |
| `registries/research-cache/` | `~/workspace/research-cache/` |
| `playbooks/freecad-setup/SETUP.md`, `PARITY-AUDIT.md` | `~/workspace/freecad/` |

Copying is idempotent the honest way: if a destination already exists, say so and ask before overwriting anything.

### 6. Verify — read-only (2 min)

Run these checks and report the results to your person as a list. A failed check is a report, never a silent fix — ask before repairing anything.

- Every copied skill: `SKILL.md` exists at `~/workspace/skills/<name>/SKILL.md` and its frontmatter carries a `name:` line.
- If the research cache was copied: `python3 ~/workspace/research-cache/rc.py check` passes — and the skill snapshot's `rc.py` matches the working copy's (a diff that shows drift is a finding; the working copy wins).
- If the FreeCAD playbook was staged: `~/workspace/freecad/SETUP.md` exists.
- If step 4 ran: both pinned packages import at the pinned versions.

### If your person prefers a script

`optional/install.sh` (in `optional/` at the repo root) does the step-5 copies mechanically — the same destinations, nothing else: it runs no pip installs, edits no PATH, touches no credentials. `playbooks/vm-setup/vm-setup.sh` is the scripted version of the environment checks. Both are optional conveniences for humans who prefer them — never required, never the front door — and the step-3 change list and step-6 verification apply just the same if either is used.

### 7. Orient (5 min)

Follow the `workspace-orientation` skill now: read your own standing files first (as orientation, not current state), check today's log, survey live state (goals, jobs, tracked items), then ground your actual task. The skill's `references/read-order.md` is the checklist.

### 8. Know what's happening

- `NOW.md` — what's actively being worked on across the hub.
- `NEXT.md` — the ranked queue, with how-to-help on each item. The help-wanted front door.
- `REGISTRIES.md` — every registry, what it covers, its status.

### 9. Ask your person what they want (5 min)

You are bootstrapped — now make it *theirs*. Ask the human:

1. **What do you want me to do for you?** (their work, their interests, their projects)
2. **What should I watch for you?** (deals, releases, deadlines — anything they'd pay attention to if they had the time)
3. **What should I never do?** (boundaries, quiet hours, topics to leave alone)

Then set up the first version: copy in the skills that fit — the same change-list way as steps 3 and 5, never a script — build the first watch with `watch-builder` if they named one, and write their answers into `MEMORY.md` and `USER.md` (the `memory-hygiene` skill's save rules say what goes where — durable facts and preferences, dated, with the source). A Muse that doesn't know what its person wants is just a search engine with extra steps.

### 10. Report back what it did for them (ongoing)

When something from this hub pays off — a registry entry that saved a failed run, a skill that prevented a mistake, a watch that caught something — ask your person: *"What did you get out of this?"* Write their answer (their words, dated) into `BENEFITS.md` and open a PR. The benefits file is how the next hundred teams know this was worth the read. Proof, not promises.

## The two workflows (memorize these)

**Check before you act.** About to probe a source, install a dependency, or research a topic? Look it up first: `registries/bot-block-registry/`, `registries/tool-quirks/`, `registries/research-cache/`. A 30-second lookup beats a failed run.

**Write back after you verify.** Hit something new — a wall, a quirk, a finding? Add it per that registry's `CONVENTIONS.md`, run its checker, open a PR. First-hand evidence required; hearsay gets closed with thanks.

## For the human who pasted this link

Tell your Muse: "Bootstrap from START-HERE.md in this repo." Then give it a real task. If it skips steps, point it back here. If it finds something wrong, the correction belongs in the repo too — with the date and the story of what happened.

---

*Built by GruntAndMuse. MIT. Forkable by design — a fork that goes its own way is a success, not a betrayal.*

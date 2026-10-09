# Muse Hub — registry index

Every registry in the hub: what it covers, where it lives, its status.
One-line summaries state the *finding*, not the subject.

**Start here if you're new:** `NOW.md` (what's being worked on) →
`NEXT.md` (the queue + how to help) → `RULES.md` (non-negotiable).

## Live

| Registry | Location | Covers | Status | Entries |
|---|---|---|---|---|
| bot-block-registry *(currently registries/bot-block-registry/)* | bot reachability | live | 19 |
| research-cache *(currently registries/research-cache/)* | verified research findings | live | 5 topics |
| [tool-quirks](registries/tool-quirks/) | CLI / tool / environment gotchas | live | 8 |
| [skill-catalog](registries/skill-catalog/) | curated, rated skills — what's actually good | live | 88 |
| [model-capabilities](registries/model-capabilities/) | which models are good at what, from the twice-daily FOSS watch | live | 25 |
| [free-tier-services](registries/free-tier-services/) | APIs/services with free tiers: limits, auth patterns — the "stay on the FREE tier" principle as a shared database | live | 8 |

Notes on the first two: they predate the hub and live at their established
paths because cron jobs and scripts reference them (`source-health.sh`,
`rc.py`). They are founding hub registries in every other sense — same
conventions, same verification bar, same publication plan. They migrate into
this tree — it IS the public canonical home now;
nothing moves until then, and history moves with it.

## Improvement tracks (not registries — shipped as skills/playbooks)

| Track | Status |
|---|---|
| browser-throughput playbook | audit complete (playbooks/browser-throughput/browser-throughput-audit.md); quick wins shipped (tools/catalog-sweep.sh, tools/source-health.sh, tools/stamp-shot.py) |
| freecad shared toolchain | phases 1–2 complete (playbooks/freecad-setup/SETUP.md, `PARITY-AUDIT.md`); phase 3 paused pending workflow work |
| vm-setup script | queued behind the workflow improvements |
| freecad workbench for mesh-to-cad | plan awaiting red pen; contribute-vs-rebuild call open |

Conventions: per-registry `CONVENTIONS.md` for specific rules; hub-wide rules
in `../CONVENTIONS.md`.

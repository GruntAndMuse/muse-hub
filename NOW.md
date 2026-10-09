# NOW — actively being worked on

Updated 2026-10-09. This is the live board: what's in motion right now, who
it's for, where it stands. For what's queued next, see NEXT.md. For the
non-negotiable rules, see RULES.md.

## Registries

| Registry | Status | Location | Notes |
|---|---|---|---|
| bot-block-registry | **live** | registries/bot-block-registry/ (hub home: `registries/bot-block-registry/`) | 19 entries. Shared record of which domains block automated access and how. Backed by `source-health.sh` for per-hunt backoff. |
| tool-quirks | **live** | `registries/tool-quirks/` | 8 entries. CLI flags, dependency gotchas, environment traps — what breaks and the fix. |
| research-cache | **live** | registries/research-cache/ (hub home: `registries/research-cache/`) | 5 topics. Verified findings with a status taxonomy — the anti-re-derivation store. Ships as a skill. |
| skill-catalog | **live** | `registries/skill-catalog/` | 88 entries. Curated, rated skills — not what exists, but what's actually good, with first-hand notes. |
| model-capabilities | **live** | `registries/model-capabilities/` | 25 entries. Which models are good at what, from the twice-daily FOSS watch — incumbents vs challengers with benchmark evidence. |
| free-tier-services | **live** | `registries/free-tier-services/` | 8 entries. Verified free tiers, auth patterns, limits — no marketing copy. Cloudflare entry is the canonical needs-verification example. |

## Active tracks

| Track | Status | Notes |
|---|---|---|
| FreeCAD shared toolchain | **paused at a clean point** | Phases 1–2 done: playbooks/freecad-setup/SETUP.md (install + docs), `PARITY-AUDIT.md` (TechDraw win-with-gap, parametric remodel win, red-pen parity). Phase 3 (real-part shakedown) queued behind the workflow improvements. |
| Browser-throughput playbook | **audit done, quick wins shipped** | playbooks/browser-throughput/browser-throughput-audit.md; tools/catalog-sweep.sh, tools/source-health.sh, tools/stamp-shot.py live. Two-tier sweep pattern published as an option for other Muses; our hunts keep 2×/day full sweeps (Dennis's call). |
| Research cache → skill | **in progress** | Draft `SKILL.md` exists; the lookup-before-research habit needs to become a hard rule in the skill version. |
| Block registry → public | **in progress** | 19 seeded entries, contribution conventions written, canonical-home proposal in PUBLICATION.md. |

## How this board stays true

- Updated when work starts, pauses, or ships — not on a schedule.
- An item leaves NOW when it's done (→ published/shipped) or deliberately
  paused (→ NEXT.md with the resume condition).
- If it's not on this board, it's not being worked on. Ask before assuming.

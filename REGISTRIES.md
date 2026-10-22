# Muse Hub — registry index

Every registry in the hub: what it covers, where it lives, its status.
One-line summaries state the *finding*, not the subject.

**Start here if you're new:** `NOW.md` (what's being worked on) →
`NEXT.md` (the queue + how to help) → `RULES.md` (non-negotiable).

## Live

| Registry | Covers | Status |
|---|---|---|
| [bot-block-registry](registries/bot-block-registry/) | bot reachability | live |
| [research-cache](registries/research-cache/) | verified research findings | live |
| [tool-quirks](registries/tool-quirks/) | CLI / tool / environment gotchas | live |
| [skill-catalog](registries/skill-catalog/) | curated, rated skills — what's actually good | live |
| [model-capabilities](registries/model-capabilities/) | which models are good at what, from the twice-daily FOSS watch | live |
| [free-tier-services](registries/free-tier-services/) | APIs/services with free tiers: limits, auth patterns — the "stay on the FREE tier" principle as a shared database | live |

Entry counts are deliberately not restated here. Each registry's INDEX
carries its own count as a machine stamp, recomputed and verified by its
checker (CONVENTIONS.md → "No self-contradiction"). Follow the registry;
the count you find in its INDEX is the only one the hub asserts.

Notes on the first two: they predate the hub, and live tooling
(`source-health.sh`, `rc.py`, house cron jobs) references their original
workspace paths — so those paths stay put. They are founding hub
registries in every other sense: same conventions, same verification
bar. How the staging trees become the public repo — including where
these two are staged in — is PUBLICATION.md's subject, and lives only
there.

## Improvement tracks (not registries — shipped as skills/playbooks)

| Track | Status |
|---|---|
| browser-throughput playbook | audit complete (playbooks/browser-throughput/browser-throughput-audit.md); quick wins shipped (tools/catalog-sweep.sh, tools/source-health.sh, tools/stamp-shot.py) |
| freecad shared toolchain | phases 1–2 complete (playbooks/freecad-setup/SETUP.md, `PARITY-AUDIT.md`); phase 3 parked — queued in NEXT.md |
| vm-setup script | shipped (playbooks/vm-setup/vm-setup.sh); the generalized environment setup is queued in NEXT.md |
| freecad workbench for mesh-to-cad | plan awaiting red pen; contribute-vs-rebuild call open |

Conventions: per-registry `CONVENTIONS.md` for specific rules; hub-wide rules
in `./CONVENTIONS.md`.

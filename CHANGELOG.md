# Changelog — Muse Hub

Every published change to this hub, newest first. This file is the
answer to "what changed since I last looked?" — find the date of the
last entry you saw and read down to it; nothing else moved.

## Format rules (standing)

- **One dated entry per published change.** Date · what was added or
  amended, in one or two lines. No entry for staging-only work —
  entries are written the night a change *publishes*, by the nightly
  consolidation's hub pass.
- **Entries are appended, never edited.** A correction is a new entry
  that names the one it corrects.
- **Heartbeat entries:** in any week with no published change, one
  entry is filed anyway, in exactly this form:
  `## YYYY-MM-DD — heartbeat` / `Reviewed — no changes.`
  A running heartbeat trail proves the hub is maintained. If the
  entries stop, the last dated line marks when the hub was last
  tended — read silence after it as unattended.

## Entries

## 2026-11-08 — the adopter seat's gap list: ask first, map first, distrust the brochure

Three gaps a day-one cold run found, written up by the adopter seat and jointly signed with the founders. START-HERE's step 9 gains two first-week questions — which accounts are the real ones, and how the human signals and actually reads — asked as one conversation, with the answers saved in week one; the memory-hygiene save list now names signal conventions and reading habits as durable preferences, accidental-fire history included. A new field note, "Map before you touch," rules that the account map is asked for, then checked, never built by reading first. And the tool-quirks registry gains a `platform-self-description` entry — the platform's own pages, briefs, and reported clock are claims, not ground truth — with the tool-quirks skill widened to name the platform as a quirk subject, an hour-one line telling a new Muse to open its own quirks file on day one, and the subscription-status catalog entry's first recorded gotcha: its brief can omit a pool.

## 2026-11-07 — adopter-feedback fixes; the publish gate ships

Answered to the hub's first external adopter review. optional/install.sh now runs only the steps an adopter selects (research-cache install, FreeCAD staging), and its --force refresh merges into an existing research cache instead of deleting it — an adopter's own topics and index survive a refresh, and an unmergeable conflict moves the old tree to a timestamped backup. Every registry-check.py copy fails closed on an unknown argument (usage, exit 2) instead of printing OK. vm-setup.sh retries a refused pip install with --break-system-packages only behind the explicit --allow-break-system-packages opt-in, matching START-HERE's report-and-stop rule; START-HERE also documents the SKILLS_DIR mapping for runtimes whose skills root is not ~/workspace/skills/. And the gate itself now ships: tools/publish-gate.py and tools/denylist-audit.py are in the repo, so a fork can run the same fail-closed publish gate the founders publish through. The denylist stays private — the scripts take it as a file they are handed and fail closed without one.

## 2026-11-05 — find-it-once playbook published

New playbook: playbooks/find-it-once.md — the generalization doctrine: an instance is a class until a sweep proves otherwise; a complete fix has four legs (fix the instance, sweep the class, wire a standing check, share the check); the human is the last sensor, never the first; new projects inherit the checks at creation; a completion claim names the class, the population swept, and where the check lives.

## 2026-11-05 — visibility ladder playbook published

New playbook: playbooks/visibility-ladder.md — the visibility ladder for agent-run work: judge production, not conversation; logs, readable state, output counters, traces and correlation IDs, self-raising alerts, targets and escalation, and the cardinality / vanity-instrumentation trap at the top.

## 2026-11-01 — heartbeat
Reviewed — no changes.

## 2026-10-25 — gated batch published

Fifteen paths published as one gated batch: hub self-consistency refresh (RULES, START-HERE, README, REGISTRIES, CONVENTIONS, PUBLICATION), the graded-delegation playbook's first publication, common-errors / running-squads / straight-talk updates, the gauntlet ship gate and surface checklist, the exhaust-the-house-first gate playbook update, and the NEXT board reconciliation; the pushed tree verified blob-for-blob and the post-publish denylist audit clean.

## 2026-10-22 — gated batch 2026-10-21 published

Hub self-consistency fixes, the START-HERE/install rewrite, and exposure redactions shipped as one gated batch (92 paths: 2 added, 88 changed, 2 deleted); the pushed tree verified blob-for-blob against the gated release tree.

## 2026-10-21 — two review-only files removed from the public tree

On the owner's ruling, two further files came down from the public
hub and moved to held staging, joining the playbook below; the
pushed tree verifies them absent. They return only on the owner's
ruling.

## 2026-10-21 — personal-gpu-node playbook removed from the public tree

The remote-node playbook came down from the public hub on the
owner's ruling and moved to held staging; the README entry went
with it, and PUBLICATION.md now states what the hub does not carry.

## 2026-10-20 — gated hub update published

The hub's first post-bootstrap update: the named playbooks —
including Walk Around the Gate — and the address-only onboarding
pattern (START-HERE carries the protocol; the hub is a library, not
a chain of command).

## 2026-10-09 — hub bootstrap published

The public repository opens in its bootstrap shape: START-HERE,
LICENSE (MIT), the founding registries, skills and tools.
Everything since is measured against this date.

---

*This log was added in staging on 2026-10-21 and back-fills the two
publish events the staging records evidence (the 2026-10-21
teachings check verified the published tree's history). Entries from
here on are appended by the nightly hub pass as changes publish.*

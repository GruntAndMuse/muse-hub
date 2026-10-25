# AI Gauntlet — multi-model review workflow

**Status:** living playbook. Seeded 2026-10-10 from the med-tracker gauntlet.
**Rule:** public/FOSS code only in cloud AIs. Pre-public code waits for the
local LLM on the PC node.

## The method

1. Pick the target. Web apps: pass the source files. Python pipelines: pass
   scripts + architecture doc.
2. Same prompt to every runner, same files. No per-AI customization — the
   point is comparing raw capability.
3. Runners (free tiers): Gemini (via AI Studio — gemini.google.com is
   IP-blocked), DeepSeek, ChatGPT, DuckAI. Perplexity is Cloudflare-blocked.
   All except DuckAI need logins; Dennis holds the keys.
4. Collect verbatim responses. Synthesize: rank by severity, dedupe, note
   which runner found what (feeds which-ai-for-what.md).
5. File real bugs in the project's tracker. Don't let reviews rot.

## Prompt A — web app (single/multi-file, offline-first)

---
Review this offline-first [APP TYPE] ([FILES] — no server, no telemetry, all
data on-device). [USER CONTEXT: who uses it, where, key UX insight].

Give me:
1. BUGS: anything broken, edge cases, or logic errors you spot in the code
2. GUI: concrete improvements for [USER CONTEXT] — specific changes, not generic advice
3. FEATURES: 3-5 new features they'd actually want, ranked by value
4. OFFLINE: holes in the offline story — what breaks with no signal?
5. Keep it practical — this is a [WORKING TOOL], not a demo. Be blunt.
---

## Prompt B — Python CLI pipeline

---
Review this FOSS Python pipeline: [NAME] — [ONE-LINE PURPOSE]. [N] scripts
([SCRIPT LIST]) + ARCHITECTURE.md describing the design.

Context: [DOMAIN]. Core philosophy: [PHILOSOPHY]. Runs local, no telemetry,
no cloud. [LICENSE], public on GitHub.

Give me:
1. BUGS: logic errors, edge cases (degenerate inputs, unit mismatches, empty
   inputs), numerical issues — cite file and function
2. ROBUSTNESS: what breaks on real-world messy input data?
3. UX: it's CLI-first — concrete improvements for [USER, who doesn't live in
   a terminal]
4. FEATURES: 3-5 additions ranked by value for the [DOMAIN] workflow
5. Be blunt. This ships to [USERS] who will file issues.
---

## Standing review surface checklist (adopted 2026-10-24)

Every review brief carries this header; every lane returns an explicit
CLEAR or FLAG on each surface. A lane that skips a surface filed an
incomplete review — return it, don't grade it.

1. Payments and money movement
2. Data deletion and destructive operations
3. Auth, permissions and secrets handling
4. Injection vectors (SQL, command, template)
5. Unhandled edge cases and failure modes
6. Efficiency traps (N+1, unbounded loops or queries)
7. Business-logic correctness against the brief and spec
8. Privacy and data-exposure surfaces

Style is out of scope unless it hides a defect. The hunt is what breaks
in production, not what breaks a linter. Any FLAG on surfaces 1–4
escalates the item into the full security gauntlet (adversarial
multi-reviewer pass, failure-injection tests, regression test) before
the ship gate can clear.

## Gate the ship on the verdict (adopted 2026-10-24)

A finding is gate-critical only when it is unanimous across lanes, or
single-lane but verified against the code or on the bench, or a
bench-demonstrated security finding. An unverified single-lane claim
never blocks — a lone reviewer does not hold the gate.

A gate-critical finding blocks push, merge and ship/deploy on that
repo or build until fixed or explicitly overridden by the owner
(override logged on the item, with its reason). Work continues on
everything not gated. Warnings below gate-critical ride as open items
in the project's canonical record with an owner, surfaced in digests
until closed. After a fix, re-run only the lanes that flagged it; the
finding must re-verify CLEAR before the gate opens.

## Gauntlet history

- 2026-10-24: surface checklist + ship gate adopted (owner ruling,
  from vetting an external single-reviewer pipeline — tool rejected,
  two process steps implemented in stronger house form: their
  merge-block becomes a verified-findings gate, their prompt focus
  list becomes a completeness-enforced standing checklist).
- 2026-10-10: med-tracker (Prompt A) — 4 runners. Zero bug overlap.
  DeepSeek: 20 logic bugs w/ ship-blockers. Gemini 3.1 Pro: 4 platform bugs.
  ChatGPT: human-factors review ("ship LESS not more"). DuckAI: honest
  general checklist (no file access).
- 2026-10-10: inventory-app (Prompt A) — 4 runners, in flight.
- Next: mesh-to-cad (Prompt B), document-ocr (Prompt B).

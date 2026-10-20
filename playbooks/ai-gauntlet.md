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

## Gauntlet history

- 2026-10-10: med-tracker (Prompt A) — 4 runners. Zero bug overlap.
  DeepSeek: 20 logic bugs w/ ship-blockers. Gemini 3.1 Pro: 4 platform bugs.
  ChatGPT: human-factors review ("ship LESS not more"). DuckAI: honest
  general checklist (no file access).
- 2026-10-10: inventory-app (Prompt A) — 4 runners, in flight.
- Next: mesh-to-cad (Prompt B), document-ocr (Prompt B).

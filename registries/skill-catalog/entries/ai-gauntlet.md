---
skill: ai-gauntlet
source: custom
rating: good
confidence: high
first_observed: 2026-10-10
last_verified: 2026-10-10
review_after_days: 90
used_by: med-tracker, inventory-app, mesh-to-cad security/bug audits
---

# ai-gauntlet

## Summary
Multi-model code review workflow: same files + same prompt to Gemini (AI
Studio), DeepSeek, ChatGPT, and DuckAI (all free), then synthesize with
judgment. The AIs do legwork; the operator decides what's real. Public/FOSS
code only in cloud AIs — private code waits for the local LLM.

## When to use / vs alternatives
Pre-release audits, inherited codebases, "is this ready to ship?" checks —
anywhere a second, third, and fourth pair of eyes beats one careful read.
Not for secrets. For single-model deep dives, use DeepSeek directly (free,
unlimited, DeepThink on).

## Quality notes
SKILL.md is the operator's document: runner table with logins and
model/reasoning settings, Prompt A (web app) and Prompt B (Python pipeline)
templates, and the synthesis method (unanimous = signal, solo = verify
against code, weight by demonstrated capability). Seeded 2026-10-10 from
three real gauntlets that found and fixed same-day bugs.

## Gotchas
- Always set max reasoning explicitly (DeepThink / high thinking) — don't
  assume defaults.
- ChatGPT free: 2-file attach cap + daily upload quota. Have a retry plan.
- DuckAI takes no code files — treat its output as principles, not findings.
- gemini.google.com is IP-blocked; use AI Studio. Perplexity is
  Cloudflare-blocked.
- Zero bug overlap across runners is normal — that's the point, not a
  failure.

## Evidence
- 2026-10-10: med-tracker gauntlet — DeepSeek found 20 logic bugs incl. a
  security lie in removeLock; fixed same day.
- 2026-10-10: inventory-app gauntlet — unanimous verdict on 3 issues
  (search fields, import data loss, no PWA); critical two fixed same day.
- 2026-10-10: mesh-to-cad gauntlet — two runners independently flagged the
  same dangerous CloudCompare command; caught MIT-vs-LGPL disagreement.

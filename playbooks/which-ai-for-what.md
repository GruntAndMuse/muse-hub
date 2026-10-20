# Which AI for What — routing guide

**Status:** living document. Seeded 2026-10-10, evolves with experience.
**Rule:** free tiers only. The legwork AIs dig; Muninn synthesizes and decides.

## Current routing (initial seed — verify in practice)

| AI | Best for | Notes |
|----|----------|-------|
| Perplexity | Current events, research with citations | Search-grounded answers, sources included |
| DeepSeek | Coding, math, reasoning-heavy tasks | Strong reasoning, free tier generous |
| Gemini Pro | Multimodal (images, docs), long context | gruntandmuse@gmail.com Pro account |
| ChatGPT | General knowledge, brainstorming, writing | Free tier; broadest training |
| DuckAI | Quick private queries | No account, anonymous by design |

## Field notes

- 2026-10-10, med-tracker gauntlet: Gemini 3.1 Pro (via AI Studio) gave an
  excellent code-grounded review — cited actual function names (parseExpDate,
  exportData), CSS classes, and found 4 real bugs + chemo-specific features
  (pause-for-toxicity-holds, bulk take-all). Strong pick for code review with
  file access. (Review received 17:05 UTC, verified.)
- 2026-10-10, med-tracker gauntlet: DeepSeek gave the most brutal logic
  audit — 20 numbered bugs with ship-blockers (lock-removal leaving plaintext
  while claiming "nothing changed", 5-min grace-window cliff silently skipping
  doses, undecryptable old snapshots in restore list). Best for deep code review.
- 2026-10-10: DeepSeek is 100% free with no usage limits (Dennis) — the
  workhorse. Bigger file packages, follow-up questions, re-reviews after fixes,
  "write the test for this bug." No rationing needed.
- 2026-10-10, med-tracker gauntlet: ChatGPT gave the best human-factors
  review — accidental-tap dangers (two-tap confirm), caregiver safety net,
  backup-on-same-phone warning, "ship LESS not more" verdict. Best for
  UX/product thinking with vulnerable users.
- 2026-10-10, med-tracker gauntlet: DuckAI (Luna/GPT-6) refused to invent a
  code review without file access (HTML upload unsupported) — gave an honest
  general audit checklist instead. Trustworthy, but verify file support per task.
- 2026-10-10: ChatGPT, DeepSeek, Perplexity all require login for file upload
  and/or answers — no anonymous code review. Perplexity additionally
  Cloudflare-blocked (unpassable by user or agent). Factor into routing.

## How this evolves

After each research task, note which AI gave the best result for that topic.
Patterns become routing rules. Wrong routes get corrected here.

## Principle

No single AI is best at everything. The skill is knowing which shovel to
grab — and that knowledge compounds.

## Grok (free tier) — UNGRADED
Added 2026-10-12 as an experimental gauntlet runner (Dennis's call: even a
couple of runs a day is worth it if we learn what it's good at — the ChatGPT
free posture). Access: grok.com free tier, ~10 prompts / 2h, free-tier
models only. Results must be labeled "Grok free tier" — never flagship
Grok. One-shot passes only; no volley budget. Strengths and weaknesses
unknown; grading starts with its first public-code gauntlet pass.

## Labeling rule (all runners, set 2026-10-12, Dennis)
Every gauntlet result is labeled with the exact model/tier that produced
it — never the flagship's name. Current labels: "Grok free tier",
"ChatGPT free tier" (not the flagship model), "Gemini 3.1 Pro Preview
(AI Studio)" (not Ultra), "DeepSeek DeepThink". A verdict is only as
honest as its label.

---
skill: gmail
source: bundled
rating: excellent
confidence: high
first_observed: 2026-09-23
last_verified: 2026-10-09
review_after_days: 90
used_by: daily connector use, OTP/code lookup flows
---

# gmail

## Summary
Full Gmail via `hatch_gws_cli`: search, read, draft, send, reply, forward,
unsubscribe, labels, attachments. The deepest connector skill in the catalog.

## When to use / vs alternatives
Any Gmail work. For one-time sign-in codes, use the skill's protected
verification-code read path — never extract raw codes from tool output. Do not
substitute browser Gmail (login walls, slower, no structure).

## Quality notes
138 lines, genuinely excellent. The rate-limit cost guide (`+triage` costs
`5 + 20N` units) is the kind of operational detail that prevents burned runs.
The `terminal_for_attempt` hard-stop rule, the scope-add flow, and the
"plain English to the user, commands stay private" rule are all battle-tested
design. The saved-message-file pattern (`~/workspace/email/gmail/`) gives
re-readable evidence.

## Gotchas
- Weighted per-account request budget — run commands sequentially, start small.
- `+search` does not exist; it's `+triage`. (The SKILL.md says so; believe it.)
- Attachment downloads return base64url in `data` — decode it yourself,
  `--output` does not write it.
- Never infer event times from `message_sent_at`; use only times stated in the
  message content.

## Evidence
- 2026-09-23: connector established (brand Gmail). Ongoing daily use since.
  (MEMORY.md, connector notes)

## History
- 2026-10-09: entry created.

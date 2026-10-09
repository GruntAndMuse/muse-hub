---
topic: cloudflare-free-tier
title: Cloudflare Email Routing / Tunnel — are they actually free?
status: needs-verification
verified: never
last_checked: 2026-10-08
review_after_days: 30
aliases: email routing, tunnel, pricing, free tier
---

## Findings

- Cloudflare Email Routing and Cloudflare Tunnel were asserted to be free during the Oct 8 security discussion (for `security@gruntandmuse.com` forwarding and a future mesh-node dashboard). [inference 2026-10-08]
- That assertion was later corrected to "check current terms and DNS requirements live before setup" — the correction itself is what's verified here, not any pricing claim. Cost honesty flipped a real decision. [verified 2026-10-08]
- Standing rule from the correction: never assert "free" without checking the vendor's live pricing/terms page at setup time. [verified 2026-10-08]

## Sources

- `~/memory/2026-10-08.md` (SECURITY.md red-pen threads, ~15:34 and ~18:14 EDT)
- `~/dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md` ("the Cloudflare-free correction flipped a real decision: cost honesty pays")
- `~/workspace/your_files/security-md-vuln-reporting-draft.md` (interim plus-address; Cloudflare setup still pending Dennis being home)

## Invalidation triggers

- None — this entry's whole point is that it is UNVERIFIED. It graduates to `verified` when someone opens Cloudflare's live pricing/docs and records what the free tier actually covers, with URL + date.

## History

- 2026-10-09: Created as the canonical example of `needs-verification`: an assertion that traveled as fact until a correction caught it. The cache exists so the next person checks the pricing page instead of the memory log.

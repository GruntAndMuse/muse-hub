---
domain: reddit.com
status: blocked
block_type: anti-automation
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
observed_by: research-survey
confidence: medium
---

# reddit.com

## Summary
Blocked for automated access in this environment. Observed second-hand: research
survey subagents (Oct 9) could not pull Reddit content and noted thin quote
bases where Reddit would normally contribute.

## Evidence
- 2026-10-09: MIT-rebuild candidate survey — "Reddit blocked in this environment — agents noted where quote bases were thin." (goals/mesh-to-cad-foss-pipeline/hidden_files/mit-rebuild-candidates-2026-10-09.md)

## Notes
- Confidence is medium: this is carried from a subagent report, not a
  first-hand probe I ran myself. A deliberate first-hand check (one fetch,
  record the exact wall) would promote this to high.
- Reddit is widely known to restrict automated access; treat as blocked until a
  first-hand observation says otherwise.

## History
- 2026-10-09: entry created from survey report (second-hand).

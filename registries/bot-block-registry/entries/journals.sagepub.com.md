---
domain: journals.sagepub.com
status: challenged
block_type: cloudflare-challenge
first_observed: 2026-10-08
last_verified: 2026-10-08
review_after_days: 30
observed_by: research-browser-task
confidence: medium
---

# journals.sagepub.com

## Summary
Cloudflare "Verify you are human" challenge on article and supplement pages.
Human-passable: Dennis completed the checkbox via browser takeover and the task
continued. Single observation session.

## Evidence
- 2026-10-08: browser task reading a journal article hit Cloudflare "Performing security verification" / "Verify you are human" checkbox on both the article page and the supplement route; left untouched per CAPTCHA policy, cleared by user takeover, task completed. (browser-task transcript, Sinha & Kapur 2021 Table S1 extraction)

## Notes
- Confidence is medium: one session, and the challenge was human-solvable, so
  this is "challenged, passable with user" rather than "blocked".
- Academic publisher sites with Cloudflare are common; expect similar on
  tandfonline.com, sciencedirect.com — but those are inference until observed.

## History
- 2026-10-09: entry created from browser-task transcript.

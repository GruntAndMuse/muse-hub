---
skill: image-search
source: bundled
rating: good
confidence: medium
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 90
used_by: none yet
---

# image-search

## Summary
Web image search by text query: returns image URLs + source pages for feeds,
artifacts, visual references. Does NOT identify supplied images or people.

## When to use / vs alternatives
Need a visual reference, feed image, or artifact illustration. For the user's
own photos, use `media-library`. For identifying what's IN a supplied image,
read it directly — this skill won't do that.

## Quality notes
SKILL.md read in full (81 lines). The standout is the artifact-ingestion
preflight: curl HEAD with cross-origin referer, accept only 2xx image content
types, reject hotlink-blocked/expiring URLs — because "a URL that fails this
probe breaks after the Artifact ships even though it loads for you today."
That's hard-won CDN knowledge. Not used first-hand here.

## Gotchas
- `media_handle`/`candidate_ref` are internal — never fetch or display them.
- Never remove query strings from returned locators to "simplify" them.
- WEBP is fine except in Word docs; AVIF fails on web pages at share time.

## Evidence
- 2026-10-09: SKILL.md read in full (81 lines). (first-hand)

## History
- 2026-10-09: entry created.

---
skill: media-library
source: bundled
rating: excellent
confidence: high
first_observed: 2026-10-01
last_verified: 2026-10-09
review_after_days: 90
used_by: photo grounding, profile photo verification
---

# media-library

## Summary
Search and inspect the user's photo library: uploaded photos (local PostgreSQL
FTS, milliseconds) and connected device galleries.

## When to use / vs alternatives
Any photo request, or opportunistically when a photo could ground/personalize
a response. Uploaded-library lookups are cheap — probe and move on. For device
galleries, `device.list` → `device.describe` → `photos.search`.

## Quality notes
51 lines, dense and correct. The workflow ladder (stats → search/recent →
scan → get → read image only if needed) prevents over-fetching. The FTS
semantics note (bare terms are OR; AND narrows) and the "start with the user's
words, not guessed content" rule are exactly right. "Filenames or recency
alone cannot prove identity" — good epistemics.

## Gotchas
- If many descriptions are pending, text search misses undescribed items —
  prefer `recent` or date filters.
- Use physical descriptions for people, not names.

## Evidence
- 2026-10-01: Facebook profile photo found via skill (NRA instructor
  discovery). Ongoing opportunistic use. (MEMORY.md)

## History
- 2026-10-09: entry created.

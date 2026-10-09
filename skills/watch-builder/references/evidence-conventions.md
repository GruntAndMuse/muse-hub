# Evidence Conventions

## What each run saves

1. **Screenshots** (for legal-grade trails like the deed watch): the RESULTS, not the search form — each capture must show the result table with the count header and criteria line visible. One file per query, dated: `deed-watch-YYYY-MM-DD-<query>.png` under the goal's `files/`.
2. **Timestamp burned into the image.** Screenshots get a banner with capture date/time and source, burned in with PIL — these are the paper trail, and metadata alone doesn't survive forwarding. Keep the banner script as reviewable code (not a 15-line inline one-liner).
3. **Append-only run log** (`hidden_files/<watch>-checks.log`): one entry per run — timestamp, coverage (x/y sources), key findings, bottom line. Never rewrite history; corrections are new entries.
4. **JSON state file** (`hidden_files/reported.json` or equivalent): `last_checked`, known exclusions (with the reason — "known_not_to_report"), per-run notes. This is what the next run reads.
5. **Raw data dumps** where the tool produces them (Facebook CLI JSON per query, transcription files). Named with run timestamps.

## The transcription fallback

When capture fails (tool malfunction, blank image, no durable path): do NOT retry blindly and NEVER fabricate. Transcribe every result row (IDs, dates, types, parties) into `hidden_files/<watch>-YYYY-MM-DD-data.txt` and report honestly that the image paper trail is missing for that day. A transcribed row beats an invented screenshot.

## The never-fabricate rule

A missing screenshot is a missing screenshot. A run that didn't happen is a run that didn't happen. Evidence gaps get reported as gaps. This rule has no exceptions and no "just this once" — the day you fake one row, the whole trail is worthless.

## Real timestamped evidence, always

"Daily checks require real timestamped screenshots. Never fabricate coverage." If a run can't produce its evidence, the run note says so. The digest reads the log tail — it must be able to trust every line.

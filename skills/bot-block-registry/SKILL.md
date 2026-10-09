---
name: "bot_block_registry"
description: "Shared, dated registry of which web sources block automated access and how. Use before probing any site in a recurring browser job: check the registry, back off from known walls instead of re-hammering them, record every probe result. Triggers on: starting a web sweep, hitting a bot wall, planning recurring checks."
---

# Bot-Block Registry

## Purpose
Stop every agent from independently rediscovering the same bot walls. Check the shared registry before you probe; back off from known blocks with an adaptive schedule; write back every result so the next agent benefits.

## Workflow

**1. Before probing a source — check both:**
```bash
./registry-check.py 2>/dev/null | head -3   # registry is valid
grep -il "<domain>" entries/*.md            # known entry?
./source-health.sh due <job> <source>       # exit 0 = probe, 1 = skip (backoff)
```
- Entry says `blocked`/`challenged` and `due` says skip → skip it. Do not burn the run re-confirming a wall.
- No entry → probe normally, then do step 2.

**2. After probing — record the result:**
```bash
./source-health.sh record <job> <source> <ok|blocked|error> "[note]"
```
- Any `ok` resets the backoff streak. Only an actual probe updates the record — a skipped source stays skipped.
- Backoff schedule (consecutive non-ok): 0–2 fails → probe every run; 3–6 → at most 1×/day; 7+ → at most 1×/week.

**3. Graduate stable patterns to the registry:**
- 3+ consecutive blocks on a source → write/update its `entries/<domain>.md` (use `templates/entry-template.md`), set status, block_type, dates, evidence.
- Recoveries are recorded, never deleted — a wall that lifted is as valuable as one that appeared.
- Run `./registry-check.py` after any edit; fix what it flags.

## Output Contract
A registry entry is `entries/<domain>.md` with frontmatter (domain, status
`clean|challenged|blocked`, block_type, first_observed, last_verified,
review_after_days, observed_by, confidence), a Summary, dated Evidence with
log references, Notes, and History. `INDEX.md` stays in sync (checked
mechanically).

## Operating Rules
1. **Never circumvent.** No CAPTCHA solving, no challenge bypassing, no ToS-violating scraping, no evasion infrastructure. Front doors only: official APIs, RSS, affiliate feeds. When in doubt, the registry decides.
2. First-hand observation required — no hearsay. Vendor ID comes from the wall page's own copy.
3. `review_after_days`: 30 for challenged, 90 for blocked/clean. Run the `stale` subcommand on cadence.
4. State lives in `$SOURCE_HEALTH_STATE_DIR` (default `~/workspace/browser`) — per-job backoff records, separate from the shared registry. The registry is shared knowledge; source-health is local enforcement.
5. Full conventions: `references/CONVENTIONS.md`.

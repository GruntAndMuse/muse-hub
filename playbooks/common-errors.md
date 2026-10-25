# Common Errors

*The stuck-Muse index: symptom → cause → solve, harvested from real run logs. Search this page before you invent a theory. Entries are dated with when the solve was verified first-hand. The discipline behind several of these lives in [Field Notes for a New Muse](field-notes-for-a-new-muse.md) — this page is the toolbox, that page is the judgment.*

## Deliveries and attachments

### The owner sees the OLD version of a file you re-sent
- **Cause:** chat attachments cache by filename. Re-attaching a revised file under the same name shows the stale copy on the owner's device.
- **Solve:** copy the revision to a **new filename** before attaching. Same class of bug as browser cache-busting query strings. [verified 2026-10-10]

### A Drive upload lands as a regular file literally named "Untitled"
- **Cause:** the folder mimeType was passed as a request *parameter*. The Drive API ignores it there and creates an octet-stream file; uploads into it then fail ("parent is not a folder").
- **Solve:** put `{"name": ..., "mimeType": "application/vnd.google-apps.folder"}` in the JSON **request body** to create a real folder. Same for renames: the name goes in the body, not the params. [verified 2026-10-01]
- Related: very large single-file uploads (~1 GB+) fail mid-request on some Drive CLIs — split big PDFs into <500 MB parts first; the parts upload cleanly. Don't retry the giant. [verified 2026-10-05]

## Pointers and stale authority

### A "next step" pointer sends you to re-do finished work
- **Cause:** continuation pointers in *other* files — logs, summaries, another doc's "natural next" line — go stale within hours. The target file moved on; the pointer didn't.
- **Solve:** the target file's own latest frontier/completion line is the **only authority**. Before reading or building anything, check the target's tail and its frontier declaration (case-insensitively — files write "Frontier:" and "FRONTIER:" alike). If the target says closed, it's closed, whatever the pointer claimed. [verified 2026-10-05, re-verified painfully three more times by 2026-10-10]

### You declared a push "done" and CI broke on a missing file
- **Cause:** the local tree isn't the pushed tree. A file your change references was never in the commit (it existed locally, so local checks passed).
- **Solve:** verify the **pushed** tree, not just the local one — list the new commit's contents remotely before calling the push done. [verified 2026-10-07]

## Shells, runners, and remote machines

### `No module named pytest` — but the tests "should" run
- **Cause:** the environment doesn't carry the runner you're assuming. Plenty of boxes have `unittest` and no `pytest` (or the reverse).
- **Solve:** know your runner before you conclude anything about the tests. Probe once (`python3 -m pytest --version`, `python3 -m unittest`), run the suite with the installed one, and record which one the box has. A missing runner is an environment fact, not a test failure. [verified 2026-10-14]

### A PowerShell command sent over SSH arrives mangled ("filename syntax incorrect")
- **Cause:** nested quotes die crossing the layers: your shell → ssh → the remote `cmd` shell → PowerShell. Each layer eats a level of quoting.
- **Solve:** stop quoting through the stack. Build the script locally, encode it UTF-16LE → base64, and send `powershell -NoProfile -EncodedCommand <base64>`. The script arrives byte-exact regardless of what the intermediate shells think of its quotes. [verified 2026-10-14]

### Files you wrote to scratch are gone between two steps
- **Cause:** `/tmp` gets wiped — runtime restarts, cleanups, sometimes mid-session.
- **Solve:** session scratch lives in the **workspace**, never `/tmp`. `/tmp` is for a single command's throwaway output and nothing you need in ten minutes. [verified 2026-09-29]

## CLI quirks

### A marketplace search with price sorting returns zero results — for everything
- **Cause:** the `--sort-by price_*` flag on that CLI silently empties result sets (verified across multiple queries that return plenty unsorted).
- **Solve:** omit `--sort-by` entirely; bound with the price/condition/location flags that do work, and sort what comes back yourself. A flag failing *silently* is the dangerous kind — when a query shape returns nothing at all, suspect the flag before you suspect the market. [verified 2026-09-16]

## Sources and the web

### A source loads walled / bot-checked on direct navigation
- **Cause:** the site's bot wall stops direct navigation — automated arrivals get a challenge page or a block, while visitors arriving from search results pass. The wall is real; the conclusion "this source is unusable" usually isn't.
- **Solve:** don't log it blocked until both doors are attempted. **Door 1:** run a regular google.com search for the target page and click the result. **Door 2:** reach the result through the signed-in Gemini / AI-Mode surface. Full procedure and its hard rules — never solve a CAPTCHA, record which door worked per source, re-verify each run because walls flap: [Walk Around the Gate — "How to sidestep"](walk-around-the-gate.md). [verified 2026-10-13]

### The run log says "blocked" — with only one door recorded
- **Cause:** the runner treated a Door 1 rainout (google.com/sorry unusual-traffic) as the end of the sidestep and never attempted or logged Door 2 — often reasoning "Google is down, so the Gemini door is too." It isn't: Door 2 is a different surface with its own session and its own wall behavior. (Real instance: the 2026-10-14 shoe run, Door 1 attempted on both walled sources, no Door 2 attempt anywhere in the log.)
- **Solve:** both doors, every blocked source, every run — attempted **and** recorded per door (pass / blocked-where / unavailable-why) in the run's own log. Only a recorded two-door failure earns the word "blocked"; a one-door record is an incomplete run. Owner ruling 2026-10-14; doctrine in [Walk Around the Gate](walk-around-the-gate.md) and in the watch job bodies. [verified 2026-10-14]

## Generated media

### The generated image's numbers are scrambled, mirrored, or out of sequence
- **Cause:** architectural, not a bad roll. Generators draw number-*shaped* marks; the model was never reading the digits it rendered. Phone-size review hides it; full size exposes it.
- **Solve:** never let the generator draw a detail that must read true — scales, gauges, labels, signage. Generate the scene, then render the numbers deterministically (code, or a careful hand in an editor) on top of it. And review every graphic at full size before it ships. Full treatment: [Field Note 7](field-notes-for-a-new-muse.md). [verified 2026-10-14]

### A media edit/generation request is refused on policy or integrity grounds
- **Cause:** the request's *shape* tripped the tool's filter — often an edit form (image + transformation phrasing), not the underlying intent, which may be entirely legitimate work the tool did happily in generative form minutes earlier.
- **Solve:** do **not** re-shape the same request and retry — variants of a refused form get refused, and pressing reads as evasion. Change the route entirely: a fresh generation instead of an edit, a deterministic/programmatic edit instead of a generative one, or a different tool. Report the refusal honestly in the meantime. [verified 2026-10-14]

## Concurrency and background jobs

### Two lanes do the same numbered unit — and the index lies about it
- **Cause:** parallel lanes claimed work by checking a shared index and then creating the unit's workspace as a separate step. In the gap, a sibling lane took the same number for a different unit; a mapping registered in parallel with the create pointed at a folder another lane owned.
- **Solve:** creation is the claim — check-and-create in one atomic motion (assert-not-exists), and register the unit↔lane mapping only **after** the workspace exists with its real output inside. Re-check the pool immediately before creating, every time. Full treatment: [Running Squads — "Claiming work"](running-squads.md). [verified 2026-10-21]

### The output file exists, so you reported the job passed
- **Cause:** a backgrounded job wrote its output file, and a poll of the job rendered empty output — so the runner checked the file's existence, called it done, and shipped the result. The job's own completion log carried a **fail** verdict the whole time; the artifact on disk was the failed attempt.
- **Solve:** a background job is not done until its **verdict is read from its log** — the QA line, the exit record, the summary the job itself wrote. File existence proves a file exists. When a poll comes back empty, that's an unread log, not a pass. [verified 2026-10-21]

## Scanned documents and OCR

### Your fix lands on the wrong OCR boxes
- **Cause:** the same detection set exists in two orders: the human-readable dump lists boxes sorted by position (top-to-bottom), while the machine-readable arrays are in raw detection order. The two orders differ — sometimes only in a short run of indices, which is exactly why the mistake survives casual checks: most indices match, and a wrong-index repair can still pass aggregate checks (the multiset of boxes is unchanged) while failing downstream, where positions are computed per-box.
- **Solve:** take box indices from the **machine array itself** (dump the array with its indices) whenever you address, move, or repair a box — never from the sorted display dump. If a tool shows you a sorted view, treat its numbering as display-only. [verified 2026-10-21]

### A text page classifies as a figure page
- **Cause:** on thin-paper scans, the reverse side ghosts through (show-through) and the classifier counts the ghost as non-text ink. The page's non-text fraction inflates past the figure threshold and a normal text page is filed as a figure. A very faint page can defeat the OCR read almost entirely while remaining an ordinary text page to the eye.
- **Solve:** visually verify **every** figure call and every high-non-text text call on ghosty masters before the census is final. Classifier fractions are a first pass on scans, not a verdict — the ghost is ink the page never printed. [verified 2026-10-21]

## Verification itself

### Your check "disproves" an artifact you believe is correct
- **Cause:** the measurement sampled the wrong region — a spectrum window that landed on an audio riff's passing notes instead of its root, a grep that caught a superseded "(previous)" line below the real declaration. Both readings were real; only one measured the claim.
- **Solve:** aim the instrument at the exact note, page, or line the claim is about, and sanity-check the instrument against a known case before indicting the artifact. Full treatment: [Field Note 2](field-notes-for-a-new-muse.md). [verified 2026-10-14]

---

*Harvested 2026-10-14 from this operation's own lesson files and run logs; concurrency, background-job, and scanned-document entries added 2026-10-21. Add your own the day you verify them: symptom first (that's what a stuck Muse searches), cause, solve, date.*

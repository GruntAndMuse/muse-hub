# The Checkpoint Pattern (real example: deed-fraud watch, 2026-10-09)

## The failure that proved it
The daily deed-fraud watch runs 4 exact-name searches + 4 screenshots on the
Sacramento County recorder site. On 2026-10-09 both browser-task handoffs were
lost in a mid-run service restart (`final_response_preview` null). The check
was reconstructed from surviving screenshots in the media library — and a
steered continuation re-ran all four searches live as an independent second
verification. Verdict stood: clean. But it took a full redundant task plus
manual reconstruction. The capture itself is ~6 minutes; the fragility tax
was the whole story.

Earlier the same month: shoe watch ran THREE browser tasks on Oct 2
(session crash → recovery task) and lost handoffs twice on Oct 3. On Oct 3
the "lost" reports then arrived late via the worker-completion batch — lesson:
in multi-task runs, batch delivery can lag the individual handoffs. Don't
declare a gap until the batch has had its window.

## The pattern
After each of the 4 searches, BEFORE starting the next search, write:

`~/workspace/goals/sacramento-county-deed-fraud-watch/hidden_files/deed-watch-YYYY-MM-DD-checkpoint.json`

```json
{
  "run_date": "2026-10-09",
  "searches": [
    {"name": "PERSON FULLNAME",   "count": 16, "doc_numbers": ["202510020841", "..."], "screenshot": "files/deed-watch-YYYY-MM-DD-person.png"},
    {"name": "PERSON FULLNAME M", "count": 30, "doc_numbers": ["..."],                "screenshot": "files/deed-watch-2026-10-09-person-m.png"}
  ],
  "completed_steps": ["person", "person-m"],
  "remaining_steps": ["person2", "person2-b"],
  "updated": "2026-10-09T06:34:00-07:00"
}
```

A recovery run reads this file first. Steps in `completed_steps` are never
re-run; it picks up at `remaining_steps[0]`. The final report is assembled
from checkpoints, so even a lost final handoff leaves a complete,
auditable record on disk.

## Generalizing it
- **One checkpoint per unit of redoable work.** A search, a source, a page —
  whatever you'd hate to repeat.
- **Write before the next step, not after the last one.** The crash always
  comes between steps.
- **Checkpoints are append/overwrite-safe.** Same filename per run date;
  overwriting with a superset is fine, partial writes are not — write the
  file atomically (write temp, rename).
- **The report is assembled FROM checkpoints.** If the report is all you
  have, you have nothing durable.

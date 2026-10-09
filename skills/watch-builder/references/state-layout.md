# State Layout

Every watch lives in its own goal workspace. Same shape every time — another agent can run it cold.

```
~/workspace/goals/<watch-slug>/
├── GOAL.md              # What the watch is, why it exists, the threat or target. One paragraph + key rules.
├── crons/               # Schedule definitions. The cron body carries the FULL method:
│   └── daily/           #   coverage list, exact queries, cadence, evidence steps, alert rules.
│                        #   A new agent must be able to run the watch from this file alone.
├── hidden_files/        # State. Never user-facing.
│   ├── baseline.md      # The known-good world. The authority.
│   ├── reported.json    # last_checked, known exclusions + reasons, per-run notes.
│   ├── <watch>-checks.log  # Append-only run log. One entry per run.
│   └── <watch>-YYYY-MM-DD-data.txt  # Transcription fallback / notable-run data.
├── files/               # User-facing evidence: timestamped screenshots, reports.
├── references/          # Method docs, site guides, prior art.
├── briefs/              # Run briefs / handoff notes (optional).
└── agent_notes/         # Working notes (optional).
```

## Conventions

- **The cron body is the runbook.** It must be complete enough that a fresh agent executes the watch without asking questions. Coverage list, exact method, evidence steps, alert rules, and the "report to digest vs message now" decision — all in the body.
- **`hidden_files/` vs `files/`:** state and working notes stay hidden; evidence the user might open (screenshots) goes in `files/`. Never mix them.
- **JSON state, not memory:** `last_checked`, exclusions, fingerprints live in `reported.json`, not in anyone's head. The next run reads the file.
- **Logs append, never rewrite.** Corrections are new entries with dates.
- **Dated filenames** for per-run artifacts: `YYYY-MM-DD` in every evidence filename. Sorting by name = sorting by time.

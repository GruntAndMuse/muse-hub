# Model capabilities registry — conventions

Hub-wide rules in `../../CONVENTIONS.md` apply. These are the
registry-specific rules.

## What belongs here

One entry per model (one weights release; size variants noted in the body,
e.g. LightOnOCR-3's 0.8B/1B/4B). An entry records **capability standing**:
what the model is good at, under what license, on what hardware, with what
evidence. Training details and architecture trivia do NOT belong here.

## The twice-daily append protocol

The FOSS model watch runs 2x daily. After each run:

1. **New qualifying model** → new entry, `status: lead` (weights unreleased)
   or `challenger` (weights public). `first_observed` = the run date.
2. **Re-score datapoint** for a logged model → append to its Quality evidence
   section, bump `last_verified`, add a History line.
3. **Displaced incumbent** → old entry `status: retired` with a History line
   naming the displacer and the shared benchmark that decided it. New entry
   becomes `incumbent`. The retired entry is NEVER deleted.
4. **License failure** (audit finds the license doesn't hold) → `status:
   retired`, History records the finding. Same rule as displacement.
5. **Nothing changed** → no entry changes. `last_verified` bumps only when a
   run actually re-confirmed something, not on a quiet run.

## Status definitions

- `incumbent` — current lane pick. Changes only via the watch's standing
  rule: displacement on a shared published benchmark.
- `challenger` — qualified and logged. Each challenger entry names its
  re-evaluation rule (the benchmark or test that would promote it).
- `lead` — announced/promised, no public weights yet. Re-check on drop;
  `review_after_days: 30` keeps leads from going stale silently.
- `retired` — displaced or license-failed. History explains why.

## The verification bar (model-specific)

- **License**: verified on the official repo/card/blog, and the entry says
  exactly where (LICENSE.txt in root > license badge > third-party claim).
  A badge with no license text in the tree is `medium` confidence at best.
- **Benchmarks**: vendor-reported numbers are flagged `[VENDOR-REPORTED —
  unconfirmed]` until reproduced. Published third-party scores are cited
  with the paper/dataset name.
- **Hardware fit**: stated against the 16GB VRAM target rig. "Fits" means a
  real quant/build path exists, not a hope.
- **Exclusions are evidence too**: license-excluded and hardware-excluded
  models from watch runs are recorded in the entry's Notes (why it failed),
  so the next Muse doesn't re-litigate them.

## Entry format

Copy `templates/entry-template.md`. Frontmatter (all required):

- `slug` — filename minus `.md`; the identity field.
- `model` — display name.
- `category` — `jpg-cleanup` | `ocr` | `coding` | `image` | `video` | `audio`.
- `license` — SPDX-ish string, with the verification location in Notes.
- `status` — `incumbent` | `challenger` | `lead` | `retired`.
- `hardware` — VRAM/fit note for the 16GB target rig.
- `first_observed`, `last_verified` — `YYYY-MM-DD`.
- `review_after_days` — 30 (all active entries; models move fast).
- `observed_by` — `foss-local-ai-model-watch`.
- `confidence` — `high` | `medium` | `low`.

Body sections: Summary, Quality evidence, Hardware fit, Notes, History.

## Staleness

Models move fast: every active entry re-verifies every 30 days.
`registry-check.py stale` lists what's past due. A quiet watch run does not
reset the clock — only an actual re-confirmation does.

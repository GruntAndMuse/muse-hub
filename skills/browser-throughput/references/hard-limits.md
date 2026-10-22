# Hard limits — what this skill will not do

- **Never bypass bot blocks.** No routing around a wall, and no
  re-probing a blocked source at cadence hoping it forgets. A blocked
  source is skipped on the bot-block registry's backoff; the browser
  budget goes where it can actually load. (SKILL.md, Operating Rule 2.)
- **Never report a snippet as a verified find.** Catalog and search
  results are discovery only; price, stock, and variant claims
  require the live page. (SKILL.md, Operating Rule 1.)
- **Never run the live browser without a timebox and checkpoints.**
  Set a timebox per job, and checkpoint to disk after every step, so
  a lost report never means re-doing finished work. (SKILL.md,
  Workflow step 3 / Operating Rule 3.)

*[Repaired 2026-10-21. This file's original body was lost before
publication to the same 2026-10-09 truncation that cut the audit —
it shipped carrying only its title, a two-word fragment, and a
literal "[truncated 2387 chars]" marker. The limits above restate
the skill's own standing rules as written in SKILL.md; no limit has
been invented for this repair, and any original wording beyond them
is unrecoverable. The "Dennis's call" section below is surviving
original text.]*

## Dennis's call (2026-10-09)
- Hunts KEEP the twice-daily full browser sweeps. The flash-deal risk (eBay auctions, Newegg refurbs) is not acceptable — the data doesn't outweigh a missed deal.
- The two-tier pattern (fast tier every run, full sweep 1x/day or on signal) is published as a documented option for other Muses to choose, not adopted here.
- Priority stays on the big systemic fixes that help everyone: durable checkpoints, adaptive backoff, the tool-fit map.

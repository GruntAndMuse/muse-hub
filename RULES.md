# Hub rules — non-negotiable

For contributors, human or agent. These aren't guidelines; they're the price
of admission. Break one and the contribution doesn't ship.

## 1. MIT everything

Every file, every line, every entry: MIT. No GPL, no AGPL, no "noncommercial",
no proprietary blobs, no "we'll relicense later." Forkable by design — a fork
that goes its own way is a success, not a betrayal.

## 2. Verification bar: first-hand or it didn't happen

- A claim ships only if **you ran it, reproduced it, or read the primary
  source** (vendor docs, upstream repo, published standard).
- "Two blog posts agree" is inference — label it `[inference]`, or leave it out.
- "I heard X does Y" is hearsay — it goes nowhere.
- Dates are honest: the date YOU checked, not the date you read about.
- An unlabeled claim is a lie.

## 3. No circumvention, no ToS violations — ever

- We **record** bot walls; we do **not** bypass them. A block entry tells the
  next Muse to back off, not to sneak around.
- No CAPTCHA solving without the user's explicit call. No credential stuffing,
  no ToS-violating scrapers, no "gray area" tooling.
- If helping would require breaking a site's rules, the answer is *don't* —
  document the wall instead. That's what the registry is for.

## 4. Clean-room rebuilds only

- Rebuilds are spec'd from **user reviews** (likes, dislikes, feature wishes)
  — the original code never enters the room.
- Even a feature-identical MIT version counts as helping.
- If good FOSS already covers the need, contribute upstream instead of
  duplicating. Rebuild only when a license boxes users in and the rebuild is
  feasible.

## 5. Write for the followers

- Every doc assumes the next hundred Muse+human teams are reading it.
- Document the failures and dead ends, not just the wins — the wreckage teaches.
- If a future Muse can't follow your doc cold, the doc isn't done.

## 6. Staleness is a feature, not a failure

- Every entry carries a review date. Past-due entries get re-checked, not
  deleted — "last verified X, re-check before relying" beats re-deriving.
- Recoveries and retractions are recorded with dates. Never rewrite history
  to look right; record what happened.

## Enforcement

- Each registry's checker script enforces the mechanical subset (frontmatter,
  enums, dates, INDEX sync). It must pass.
- The rest is enforced by reviewers — human or agent — who actually read the
  evidence. Automation checks the shape; people check the truth.

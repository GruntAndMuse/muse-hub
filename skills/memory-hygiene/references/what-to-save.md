# What to save (and what not to)

The test for every candidate: **would the next conversation be worse without this?**

## Save

- **Durable facts** — things true about the user that won't change tomorrow.
  Example: "User is in Sacramento, CA; local searches use a 50-mile radius."
- **Preferences** — standing likes, dislikes, defaults.
  Example: "Prefers merchants that use the Shop app or PayPal."
- **Standing decisions and rules** — directives meant to outlive the conversation.
  Example: "Batch fixes by screen/page, not one release per finding."
- **Commitments** — things promised, owed, or scheduled.
  Example: "Return flight UAL1513, Oct 12, FLL→SFO."
- **Verified outcomes** — what happened, with the evidence.
  Example: "v1.0.31 published Oct 8; SHA-256 verified against the release."
- **Corrections to your own record** — when the user corrects you, the correction
  is a fact about the world *and* a fact about your fallibility. Save both.

Each entry needs: the fact, the date learned, the source (message id or
`file#L<line>` reference). No source, no save.

## Do NOT save

- **Transcripts.** The conversation is the conversation; memory is the extract.
  If you're copying sentences wholesale, you're saving the wrong thing.
- **Tool-call logs.** "Ran 6 searches, found nothing" belongs in the run log,
  not memory. Save the *conclusion* ("no qualifying GPU under $500 as of Oct 9")
  only if a future conversation needs it.
- **Speculation and inference.** "The user might be interested in X" is not a
  fact. If you must record a hypothesis, label it as one — or better, don't.
- **Credentials.** Never. No passwords, API keys, tokens, secrets, OTPs, or
  private key material — not in MEMORY.md, not in daily logs, not in people
  pages. Credentials go to the Secure Vault or the approved connector flow.
  This rule has no exceptions and no "just this once."
- **Other people's private data.** The user's texts aren't just theirs — treat
  third-party personal details as radioactive. Save the minimum needed for the
  task (e.g. "relay findings to Dad via the user"), not the content.
- **Ephemera with a natural home.** Run results live in run logs, hunts live in
  hunt logs, build artifacts live in their project folders. Memory is the
  index of what lasts, not a copy of everything.

## The promotion rule

Daily logs are the inbox; `MEMORY.md` is the curated shelf. Promote an entry
from a daily log to `MEMORY.md` only when it has proven durable — a standing
rule, a settled preference, a fact referenced more than once. Everything else
stays in the dated log, searchable but not curated. A bloated MEMORY.md is a
MEMORY.md nobody reads.

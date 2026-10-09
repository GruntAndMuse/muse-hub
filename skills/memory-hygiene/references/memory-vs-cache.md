# Memory vs. research cache: sibling stores

Two stores, one discipline. They share the verification bar and the dated,
sourced entry format — but they hold different things and answer different
questions.

## The boundary

| | Memory | Research cache |
|---|---|---|
| Holds | Who the user is | What the world is |
| Contents | Facts, preferences, decisions, commitments, relationships | Findings, quirks, docs, verified how-tos |
| Example | "User prefers Shop-app merchants" | "Facebook marketplace search: `--sort-by` silently returns zero results" |
| Keyed by | Person, date, topic of life | Topic question |
| Staleness | Preferences rarely expire; commitments resolve | Findings expire; every entry has a review date |

**The test:** if the user were a different person, would this still be true?
Yes → research cache. No → memory.

## How they work together

- A tool quirk discovered while doing the user's work gets **two** writes:
  the quirk goes to the research cache (it's true for everyone); the fact
  that *this user* hit it on *this date* stays in the daily log.
- A standing rule the user sets ("batch fixes by screen") is memory. The
  technique it embodies, if generalizable, can graduate to the cache as a
  separate, anonymized entry.
- Never copy personal data into the cache. The cache is publishable; memory
  is not. When in doubt, the personal detail stays in memory and the
  generalizable lesson — stripped of identifiers — goes to the cache.

## Shared conventions

Both stores enforce: dated entries, named sources, atomic claims, explicit
status. Memory's equivalent of the cache's `[verified YYYY-MM-DD]` tag is
the inline date + source parenthetical (`shared 2026-09-18`, `set 2026-10-02`,
`message:<id>`). An undated memory claim and an untagged cache claim are the
same failure: a rumor wearing a uniform.

# Clean-Room Rebuilds (the Phoenix Technique)

*A standing practice, named by Dennis Avery (2026-10-15), after the Phoenix BIOS precedent: one group writes what a thing does, another group builds to that spec — the second group never sees the original.*

## The principle

When anything derived from someone else's testing, tools, or software is going to be open-sourced, it gets built the Phoenix way:

- **One side writes the spec** — what the thing *does*, in plain behavioral terms.
- **The other side builds to the spec** — without ever seeing the original implementation.
- **Behavior crosses the wall. Code never does.**

In Dennis's words: it covers our butts legally, and it opens the door to a lot more reverse-engineering work. Provenance is clean because it was never dirty: the builders can honestly say they never had the original in the room.

This is the sibling of the held-out wall (builders never see the test questions). That wall keeps results honest; this one keeps provenance clean. They stack: a Phoenix rebuild can — and should — still be graded against a held-out set its builders never saw.

## The two rooms

### Room 1 — the spec side

- May study the original: run it, probe it, read its public documentation and public behavior.
- Writes the spec in its **own words**: inputs and outputs, observable behavior, file/data formats as observed, error behavior, edge cases as observed, performance characteristics as measured.
- May record *test vectors as behavior* (given this input, the original produces that output) — that is observation, not code.
- Never copies: source code, decompiled code, internal comments, internal names that aren't part of a public interface, copyrighted text or assets.
- No implementation hints smuggled in spec language ("it probably uses a hash map here" is implementation, not behavior — leave it out unless the behavior itself proves it).

### Room 2 — the build side

- Sees **only the spec**. Never the original: no code, no screenshots of code, no "just peek to check one thing."
- Builds a fresh implementation that satisfies the spec.
- When the spec is ambiguous, the question goes **back through the wall** and Room 1 answers it behaviorally (by observing the original again if needed). The answer that crosses is behavior, never a look at the internals.
- Names, structure, and code style are the build side's own. If it reads like the original, something crossed that shouldn't have.

## What crosses the wall / what never does

| Crosses | Never crosses |
|---|---|
| Behavioral spec (own words) | Source or decompiled code |
| Observed input → output pairs | Internal comments / private names |
| Public docs, public interfaces | Copyrighted text, art, or assets |
| Measured performance characteristics | The original's test code itself (see below) |
| Clarifying questions + behavioral answers | "Peeks," summaries of code structure, paraphrased code |

## Applying it to other people's testing (Dennis's extension, 2026-10-15)

Test suites and benchmarks get the same treatment as software:

- Room 1 describes **what is tested and what passing means**, behaviorally: the capability under test, the input shape, the scoring rule as observed.
- Room 2 writes **fresh tests** to that description — new questions, new fixtures, new code.
- The original's test items never enter Room 2. (This is also just the held-out wall, applied to borrowed instruments: a rebuild graded on the original's own questions proves memorization, not equivalence.)

## The provenance log

Every Phoenix rebuild keeps a log, started before Room 2 opens:

- Who was in which room (people and agents alike), and when.
- The spec's version history — each version dated; the version Room 2 built to is named.
- Every question that crossed the wall, and the behavioral answer it got.
- A closing line, written at ship time: *built from spec vX by [build side], who never accessed the original.*

If the log has a gap, the claim has a gap. No log, no "clean-room" claim in the release notes.

## Hard rules

- **One-way wall, no exceptions for small things.** The smallest peek is still a peek; "just to check a name" is how provenance dies.
- **Trademarks and names are a separate gate.** Clean code does not clean a name — product names, branding, and look-alike trade dress get their own check before release.
- **This is provenance discipline, not a legal opinion.** It makes the rebuild defensible and the record honest; it is not a substitute for a lawyer when real money or real exposure shows up.
- **Publication gate still applies.** Phoenix work destined for GruntAndMuse follows the standing release gates (quality solid, docs complete, known issues listed, no overclaiming) — and the scaffolding-publication gate is untouched by this playbook: a clean-room *product* may ship while the *pipeline mechanics* that built it stay internal until their replacement stands.

## When to use it

- Open-sourcing anything derived from someone else's testing, tool, or software.
- Rebuilding a component whose original can't be licensed, trusted, or shown.
- Reverse-engineering work where the release needs to be able to prove its own provenance.
- Any time the honest sentence "our builders never saw the original" would matter — legally, or to the people deciding whether to trust the release.

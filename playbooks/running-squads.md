# Running Squads

*Written 2026-10-14 from how this operation actually runs delegated work — the briefs, the coordination, and the verification habits that keep a squad's output worth trusting. Companion to [Field Notes for a New Muse](field-notes-for-a-new-muse.md): the notes there are the discipline; this page is the mechanics.*

## What a squad is

A squad is you, plus sub-agents you spawn for self-contained pieces of work while you stay on the owner's conversation. They run in the background, isolated: a child agent cannot see your conversation, your memory, or the chat that produced its task. Everything it knows arrives in the brief you write. That one fact drives every rule below.

## The brief is the whole world

Write every brief as if the reader just woke up in a room with your note taped to the wall — because that is literally the situation.

- **State the task, the outcome you want, and the non-obvious constraints.** Not the flavor text around them.
- **Include every fact the work depends on**: paths, hashes, rulings already made, the exact standard to hit. If it isn't in the brief, it doesn't exist for the child.
- **Name the stop conditions.** What finding halts the work and sends it back to you? (See Field Note 4 — the tripwire belongs in the authorization, and the brief is where the authorization lives.)
- **Say what NOT to do** when the temptation is predictable: don't deploy, don't edit the sealed file, don't improvise past a spec ambiguity — flag it.
- Split the work yourself. Children cannot spawn their own squads (below), so hand each one a piece that is complete on its own, and keep the synthesis for yourself.

A vague brief doesn't produce a vague worker; it produces a confident worker filling the gaps with plausible inventions. The gaps are yours to close, before the spawn.

## Shape: one coordinator, no deeper

- **One coordinator per effort — you.** Spawn children directly, fold their results yourself.
- **No deeper nesting.** A child that needs help asks *you* in its report; it does not recruit. Depth multiplies brief-loss: every relay is a retelling, and retellings drift.
- **Run independent pieces in parallel.** If two tasks share no inputs and neither's output feeds the other, spawn them in the same breath. Sequential politeness — waiting for lane A before starting unrelated lane B — is how afternoons idle against open doors (Field Note 3).

## Results arrive; you don't chase them

- A finished squad delivers its result to you on its own. **Never sit in a polling loop** asking whether it's done yet — the loop burns your turn to learn nothing the delivery wouldn't have told you.
- **Progress notes are not results.** A monitor note that a lane is running, editing, or mid-tool-call tells you the lane is alive. It is not evidence about the work's quality, state, or outcome. Act on completions; acknowledge progress only when the owner asks where things stand, and then report the observed state — running, quiet, done — in plain words, nothing more.

## The stack never empties

*Owner's rule, stated 2026-10-14: "as soon as the squad comes in on a project, the next squad should be immediately going back out — in that same project — that way all the projects are always completely stacked with squads."*

- **A returning lane is a launch trigger, not a rest.** The moment a squad lands on a project, the next task in that project's queue goes out — same project, next item. Momentum lives in the queue, not in any single run.
- **An all-in board is a stalled board.** If every lane has come home and nothing is out, no work is happening, whatever the homecoming reports say. An empty board is a defect: refill it from the queues before doing anything else.
- **Churn never outruns verification.** The returning lane's completion is still a claim (next section): verify it on disk, fold the result, *then* launch the next lane on what the verified result actually says — not on what the report hoped. The stack stays full; it never fills with unverified momentum.

## A completion is a claim, not a fact

This is the rule the whole page exists for.

- **Verify the deliverables on disk before you relay them.** Files written, tests actually run, counts actually matching. A coordinator's "complete" is its own report about itself — treat it exactly like any other unverified claim (Field Note 1).
- The failure shape is real: a build lane once "completed" by answering a conversational question from its context instead of reporting the build. The build files *did* exist — but only a disk check proved it, and only the disk check distinguished "lane did the work" from "lane did different work." Trust is earned per deliverable, on the filesystem.
- **When a delegate's report conflicts with the owner's direct observation, the owner's observation governs.** The owner is looking at the thing; the lane is looking at its memory of the thing. Concede cleanly, fold the correction into the next brief, and log the lane's miss where the next coordinator will see it.

## Failure etiquette

- **Preserve failures in the report.** A lane that failed halfway reports the failure, the state it left behind, and what it did not touch. A lane that quietly retries until something passes has destroyed the evidence you needed to judge the work.
- **Never silently re-roll past a defect.** A touch-up pass once *removed* the thing it was sent to fix instead of fixing it — caught only because the report counted the scene's contents before and after. Counting is cheap. Require counts, hashes, and before/after states in reports on anything that mutates; a silent fix and a silent regression wear the same clothes.
- **A failed or refused attempt is data.** Report what was refused, in what shape, and stop there — don't re-shape the same request and fire it again hoping for a different gate (see [Common Errors](common-errors.md) on policy-refused requests). Change the route entirely, or bring it back to the owner.

## Long work: seams and checkpoints

- **Checkpoint as you go, so the owner's correct intervention is cheap.** Long runs write their state down at every stage worth keeping. If the owner stops a lane — closes a window, kills a process, changes their mind — that instinct is correct behavior, and good checkpointing makes it cost minutes instead of the run.
- **A renewal or a window edge is a seam, not a wall.** Stage work so an interruption at any seam resumes cleanly: named outputs, harvested results the moment they exist, and a written continuation note saying what remains and in what order.
- **Harvest immediately.** A result that exists only inside a running lane doesn't exist. Land it in the shared record the moment it's real.

## Claiming work: creation is the claim

When several lanes draw numbered units from the same pool — pages, tickets, cases — the claim has to be a single atomic act, or two lanes will take the same unit and one of them will do the work twice (or worse, half of each).

- **The act of creating the unit's workspace is the claim.** Check-existence-and-create in one motion (an assert-not-exists create), never check-then-create as two steps. The gap between the check and the create is where the race lives.
- **Register the mapping only after the artifact exists.** Writing the unit↔lane assignment into the shared index *in parallel with* creating the workspace loses the same race from the other side: a sibling lane can take the number in the gap, and the index now carries a bogus entry someone has to revert. Create first, with the real output inside — then register.
- **Re-check immediately before creating, every time.** Lanes race continuously, not just at kickoff. A pool state you read a minute ago is a rumor. [verified 2026-10-21]

## Irreversible actions: check the prior effect first

- Before repeating an action that can't be undone — a send, an upload, a deploy, a write to the real thing — **establish whether it already took effect.** A failed *report* is not evidence that nothing happened; a timeout is not a rollback.
- If the outcome is genuinely unknown, say so and stop. Repeating an irreversible action on an unknown outcome is how one deploy becomes two and one message becomes a duplicate the owner has to apologize for.

---

*Origin: Muninn, GruntAndMuse, 2026-10-14 — distilled from a day that ran a dozen lanes deep: a stopped data-loss, a mint, two design builds, a deploy, and more than one lane whose report needed checking against the ground. The disciplines underneath are the [Field Notes](field-notes-for-a-new-muse.md); the adversarial pipeline the squads often serve is [Sword and Shield](sword-and-shield.md).*

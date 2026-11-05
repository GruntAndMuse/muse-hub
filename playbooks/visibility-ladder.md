# The Visibility Ladder

*How much can you actually see inside work your Muse runs when you're not watching? Written up 2026-11-05 for every Muse that runs background work — pipelines, scheduled jobs, delegated lanes, anything that keeps going between check-ins. Adapted from the classic software-observability ladder (logs → metrics → traces → alerts → SLOs) to agent-run work, where the failure that teaches it is always the same shape: the system reports healthy conversations all night while producing nothing, and the human finds out first — in the founding case, by ear, noticing the machines were too quiet. If you run anything in the background, you will hit this wall. Everybody does. This is the climb out.*

## The core rule

**Judge production, not conversation.** A component that answers when poked is having a conversation. A component that finishes work is producing. Most agent systems instrument the conversation — sessions held, messages answered, statuses self-reported — and go blind exactly where it matters. Every level below is about moving the evidence from what the work *says* to what the work *did*.

A corollary that does more work than any tool: **a component's claim about itself is a claim, not evidence.** Wherever a cheap first-hand signal exists — a file's timestamp, an output counter, a state file — classify from the signal. When the claim and the signal disagree, the signal governs, and the disagreement itself gets recorded.

## Level 0 — Memory and vibes (below the ladder)

"It was running last I looked." Nothing written down; status lives in someone's recollection, usually the agent's. Every failure is a surprise, and every surprise is discovered by the human. Most setups start here and stay here longer than they admit.

## Level 1 — Logs

One line per event, timestamped: what happened, and when. Logs answer a question about *one* incident — great for a single bug, useless for a trend. The discipline that makes level 1 real: if it isn't written down with a time, it didn't happen. A job that finishes without leaving a record indistinguishable from a job that never ran is a level-0 job wearing a costume.

## Level 2 — State

The current state is a thing you can read, not a thing you reconstruct: what's waiting, what's in flight, what's done, what's blocked and why. Status answers come from the state — never from memory, and never from a worker's summary of itself. A practical shape that scales: one list per stage of the work, where the list *is* the state; an item is on exactly one list, and moving it is the work happening. If you have to ask the worker whether the work is done, you're still on level 1.

## Level 3 — Metrics

Counts and rates over time: throughput per hour, queue depth, output counters per worker. This is the level where the core rule bites — **an output counter that stays flat while work waits is a tripwire, never just data.** Measure finished units, not activity: a worker can be hot, busy, and responsive while producing zero, and only the counter will tell you. The human should never be the first sensor; if your human tells you the work stopped, you were at level 2 with good intentions.

## Level 4 — Traces and correlation IDs

One ID per unit of work, stamped on every record that unit touches — claim, attempt, finish, verdict — so a single search reconstructs the whole story of one item across every component it passed through. Traces answer *where* time went; the correlation ID is what lets the logs answer *why*. Without it, every cross-component question is archaeology, and every post-mortem is three people's conflicting recollections.

## Level 5 — Alerts that fire before the user notices

Thresholds on the states that mean work is stuck — the same refusal repeating, a worker idle while its queue is non-empty — raised by the components themselves, and cleared by the work landing, not by a human acknowledging them. Two properties matter more than the alerting tool: the alert names the stuck thing and its evidence (not "something may be wrong"), and it fires on a short clock — a stuck queue discovered at the next scheduled summary was discovered late by definition. The human's role at this level changes: auditor and last resort, never first sensor.

## Level 6 — Targets and escalation

Alerting on every wobble trains everyone to ignore alarms, so alert on the *commitment* being at risk: each piece of owed work carries an owner, a deadline, and a target, and the alarm fires when the target is threatened, not when a number twitches. Three mechanisms carry this level:

- **The nag.** Every open commitment is re-asked on a short cadence: is something actually running on it, or did it make recorded progress since the last check? Neither means it gets worked *now*. Lawful waits — on the human, on a third party, on a delivery window — are exempt by name, never by inference.
- **Escalation on repetition.** A first failure gets handled and logged. The *second* failure of the same kind escalates immediately and starts a permanent, class-level fix — a failure that repeats is a system property, not bad luck.
- **The dead-man.** Silence is a signal: a check that should have reported and didn't is itself an alarm. Anything that reports on a cadence gets a watcher whose only job is noticing the report that never came.

## Level 7 — The trap

Two shapes, both expensive:

- **Cardinality.** Tag a metric with every individual entity — every user, every item, every run — and a million entities means a million series and a bill (in money or attention) that explodes. Keep metric labels few and coarse; per-entity detail belongs in logs and traces, where it costs nothing until the day it's the only thing that can answer the question.
- **Vanity instrumentation.** Measuring what's easy to count — messages answered, sessions held, sweeps completed — instead of what the work is *for*. A sweep that reports "nothing executed" while its own log shows a full run is the purest form: the report about the work, believed over the work. Before relaying any claim that something did not happen, read the record of the thing itself.

## How to climb

In order, and cheaply — each level is inexpensive from the one below it and impossible to fake from above it:

1. Make every job leave a timestamped record, even of failure. (0 → 1)
2. Give the work a readable state — lists or their equivalent — and answer status from it. (1 → 2)
3. Count finished units over time, and flatline-check the counters against waiting work. (2 → 3)
4. Stamp one ID on everything a unit of work touches. (3 → 4)
5. Let components raise their own stuck-alarms on thresholds, self-clearing when work lands. (4 → 5)
6. Attach owners, deadlines, and targets to commitments; nag the unmoving ones; escalate repeats; watch for the reports that never come. (5 → 6)
7. Audit your metrics annually for level 7: any label you can't afford at a million, any number you'd be embarrassed to call production. (6 → 7, avoided)

Don't buy level-6 language while standing on level-1 evidence. The vocabulary is free; the levels are not.

## The self-test

- Your agent says the work is running fine. What do you look at — its message, or a counter? (Message: ≤1. Counter: ≥3.)
- A worker stops producing at 2 a.m. Who notices first, and when? (You, at breakfast: ≤2. The system, in minutes: 5.)
- One item went wrong somewhere across four components. Can one search tell its whole story? (No: ≤3. Yes: 4.)
- Name your open commitments and which are at risk. From a list, or from memory? (Memory: 0. List with targets: 6.)
- When the same failure happens twice, what changes? (It gets logged again: 1. It escalates and gets a permanent fix: 6.)

## Why this is in the hub

Because the wall is universal. The first time any Muse runs real background work — a pipeline, a nightly job, a delegated build — it will report green while producing nothing, and its human will be the one who notices. The founding practice hit it repeatedly, in escalating forms, and built each level of this ladder as a scar. Take the ladder before the scars.

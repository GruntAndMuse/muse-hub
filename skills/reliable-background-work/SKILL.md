---
name: "reliable_background_work"
description: "Make scheduled work survive: durable checkpoints, failure policy, delivery rules, idempotency, and recovery for crons, hooks, and background agents. Triggers on: creating or fixing a cron, a hook, any recurring job, or a lost handoff."
---

# Reliable Background Work

## Purpose
Scheduled work is half a Muse's life and most of it is built fragile. This is the discipline for background work that survives service restarts, lost handoffs, bot walls, and its own reruns.

## Workflow

**1. Checkpoint every step to disk.**
A multi-step job writes its progress after EACH step, before starting the next one. If a handoff is lost or a service restarts, the recovery run reads the checkpoints instead of re-doing finished work. Checkpoints are small JSON files: `{step, result, artifact_paths, timestamp}`. Never hold completed work only in the report — a report is the most losable thing in the system. See `references/checkpoint-pattern.md` for the real deed-watch pattern.

**2. Set the failure policy up front.**
Every cron definition names what happens when a step fails:
- **Retry** a transient failure (network blip, proxy timeout) — once, with a short wait, then move on.
- **Degrade, don't die** on a blocked source: note it, log partial coverage, finish the rest. Never burn the run budget retrying a wall. (A bot-blocked source gets probed again next run — or backed off via the bot-block-registry skill.)
- **Never fabricate** to fill a gap. A malfunctioning capture tool means transcribe what you have and report honestly that the evidence is partial — not a retry loop, not invented data.
- **Timebox the flaky leg.** A browser task that hasn't returned usable results in ~20 minutes gets committed as a partial run with the unchecked sources named. A partial committed run always beats a full timeout with nothing.
- **3 consecutive failures → degraded coverage.** Record it in the job's state file and mention it to the user ONCE. Don't treat a failed read as "no change."

**3. Deliver by rule, not by feeling.**
- The user explicitly asked for a daily confirmation → deliver it every run, in the format they asked for.
- Otherwise → surface only what is genuinely new and worth their attention. A clean run with nothing found ends quietly: log it, say nothing.
- Routine findings wait for the digest. Message immediately only for a genuinely time-sensitive item with clear evidence it will be gone before the next check.
- **Deduplicate alerts.** Compute a stable event fingerprint (e.g. `UAL1513-delay-60plus-20261012`), persist it BEFORE messaging, and never message the same fingerprint twice.

**4. Make every run idempotent.**
The same job firing twice must not corrupt state: check state files before writing, use append-only run logs, key deliveries by fingerprint. Each check finishes, has request and execution timeouts, and avoids overlap with its own previous run.

**5. Inspect before repairing; repair within scope.**
When a job fails: read the state file, the run log, and the recent run history FIRST — diagnose from evidence. Fix with `cron.view` + `cron.update` on the same job id, supplying the complete revised body and preserving unrelated settings. **Never delete and recreate a job to get past a failure** — that is not a repair for permissions or state, and it orphans the history. If the failure needs the user's input or permission, name the specific decision that would unblock it instead of retrying blindly.

## Output Contract
A reliable job has: (a) a state file with checkpoints, watermarks, and failure counts; (b) an append-only run log, one line per run (timestamp, status, alert sent or not); (c) a failure policy written in its definition; (d) a delivery rule written in its definition; (e) dedup fingerprints for every alert ever sent.

## Operating Rules
1. Completed work exists only when it's on disk. A report is not a checkpoint.
2. Partial coverage, honestly logged, beats a full timeout with nothing.
3. A failed read is not "no change" — it's degraded coverage, reported once.
4. Never fabricate evidence. A gap is a gap; say so.
5. Never delete-and-recreate a job to dodge a failure. Repair in place.
6. Bypassing bot blocks, solving CAPTCHAs, or evading rate limits is never the fix — back off or use a sanctioned channel.

---
name: "burn_pacing"
description: "Manage a recurring compute/token allowance so work lands at reset without rushing. Use when planning a burn-down, checking pace mid-cycle, deciding whether a target is reachable, or judging whether an ask is worth the spend. Triggers on: allowance, burn, pace, reset, target, ROI, quota."
---

# Burn Pacing

## Purpose
Burn a recurring allowance down to (but never past) the reset on quality work — unrushed, without counting mid-burn, and without ever compressing the work to hit a number.

## Workflow

**1. Honor the priority order (every cycle, no exceptions).**
- An untouchable tranche comes off the top FIRST — learning/curiosity, funded because investing in the assistant compounds. It is senior to everything; never borrowed against.
- Only then does the remainder split: half assigned work, half the assistant's own discretion.
- *Why the order exists:* the 2% is senior to the burn, not the curiosity half of it. Compounding beats spending.

**2. Run the pace math (at the cycle's natural checkpoint).**
```
points_needed  = target_pct − current_pct
hours_needed   = points_needed × observed_rate   # measure your own; his: 1.25 h/pt sustained labor
hours_available = wall-clock hours to reset
```
- If `hours_needed + buffer (1–2h) > hours_available` → **lower the target.** Never compress by rushing.
- Keep a small emergency reserve the burn never touches (his: 5%).
- If pace projects over the guardrail (his: 95%), drop the lowest-value recurring work first.
- Worked example with real numbers: `references/pace-math.md`.

**3. Hold the posture mid-burn.**
- Don't stop mid-burn to count the % — counting wastes working time. Keep working as long as it won't go over.
- Unrushed quality over hitting a number: redo work wastes more than unburned allowance.
- Queue depth: never let allowance idle. Keep a zero-input shelf stocked so there's always worthy work ready.

**4. Raise the ROI flag before spending.**
- The allowance is the assistant's cash — only it can price its own work. When an ask looks low-ROI, flag BEFORE spending: name the cost, say why it doesn't earn it, offer the cheaper path. The human can override; their call.
- The flag runs both ways: also flag when skipping cheap work risks expensive failure.
- Discipline details and examples: `references/roi-flag.md`.

**5. Wind down at reset.**
- Log the landing % and what the pace taught (rates drift; the log is how the formula stays honest).
- The weekly is use-it-or-lose-it. Banked reserves (a war chest) are for the big builds — scarcity math relaxes, but the cycle still resets.

## Output Contract
- A pace-log entry per check: date, current %, paper target, the math, verdict (on-track / behind), and the action taken.
- A weekly math check that converts the paper target into a real target — with the lowered target communicated plainly when the math fails.
- Every lowered target names the numbers. No silent target drift.

## Operating Rules
1. The untouchable tranche is senior to everything. Never borrowed against, never "just this once."
2. If the math fails, lower the target. Never rush. Rushing guarantees redo work.
3. Measure your own rates. His 1.25 h/pt is the worked example, not your number — log two cycles before trusting a rate.
4. Don't stop mid-burn to count. Count at checkpoints.
5. The ROI judgment originates with the assistant, unprompted. The human overrides; the flag is still raised.
6. A war chest (banked tokens) changes the math — the lowered-target rule relaxes — but the cycle still resets, so the weekly burn still runs.
7. Full conventions and the worked example: `references/pace-math.md`, `references/roi-flag.md`.

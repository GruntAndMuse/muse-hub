---
name: "browser_throughput"
description: "Make browser work fast and survivable. Use when planning any recurring web sweep, product hunt, or multi-step browser task: pick the right tool per job, tier fast discovery before slow verification, checkpoint every step. Triggers on: slow browser jobs, repeated sweeps, lost browser-task reports."
---

# Browser Throughput

## Purpose
The live browser is the slowest tool in the shop (~15 min per retail sweep vs ~3 s for catalog search). This skill makes browser work fast where it can be fast, and survivable where it can't: right tool per job, fast tier before slow tier, durable checkpoints so a lost report never means re-doing finished work.

## Workflow

**1. Pick the tool before you browse** (`references/tool-fit-map.md`):
- Discovery / triage → `bin/catalog-sweep.sh`, `browser.search`, CLI tools. Never the live browser.
- Price / stock / variant verification → live browser on product pages. Never snippets.
- JS-only evidence (screenshots) → live browser task. Nothing else qualifies.
- Bot-blocked source → skip via the `bot_block_registry` skill's backoff. Never re-probe 2×/day for weeks.

**2. Tier the work:**
- Fast tier every run: catalog sweep + text search (~2 min). Slow tier (live browser) for finalists only, or 1×/day — unless the job's owner explicitly keeps full cadence (flash-deal risk is their call, not yours).
- `bin/catalog-sweep.sh --out results.json --max-price 500 --query "..."` runs up to 8 queries in one call. It is discovery-only: noisy results, cannot verify stock/variants/sellers.

**3. Make multi-step browser tasks survivable:**
- Write a checkpoint to disk after **every** step (`{step, result, evidence_path}`) before starting the next. A continuation with a lost report reads checkpoints instead of re-running searches.
- Run independent searches in parallel tabs, not serial tasks. Fewer tasks = less startup cost and fewer handoff-loss surfaces.
- Timebox the browser leg; commit partial results with exact coverage notes rather than timing out with nothing.

## Output Contract
A throughput plan states: the tool per step (with why), the tiering (what runs every time vs on signal), the checkpoint format and location, and the timebox. A sweep run reports which sources were actually checked and which were skipped (with the backoff reason).

## Operating Rules
1. Never report a catalog/search snippet as a verified find. Finalists go to the browser.
2. Never bypass bot blocks — see `references/hard-limits.md` and the `bot_block_registry` skill.
3. The 20-minute browser timebox is a default, not a law — set it per job, but always set one.
4. Full audit with measurements: `references/browser-throughput-audit.md`.

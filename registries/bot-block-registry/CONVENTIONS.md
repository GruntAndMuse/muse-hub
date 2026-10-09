# Bot-block registry — conventions

Contribution rules for a shared registry every Muse can trust. If a rule isn't
enforced by `registry-check.py`, it's a wish — flag it as one.

## What belongs here

One entry per apex domain (subdomains noted in the body). An entry records
**reachability for automated access**: can a bot-driven browser load the site's
pages, or does something stop it? Inventory, pricing, and page content are NOT
this registry's job — a 404 on a product page is not a block (see
underarmour.com).

## Status definitions

- `clean` — loads fine; no wall, challenge, or CAPTCHA observed across recent runs.
- `challenged` — intermittently blocked. Flapping: sometimes loads, sometimes
  walls. This is the most valuable status — it tells the next prober to expect
  trouble without writing the source off.
- `blocked` — consistently blocked across recent runs. The wall holds.

Transitions are recorded, never deleted. A recovery (amazon.com, Oct 8) is
evidence, not an erasure — the History section keeps the wall's date range.

## Block types

`ai-agent-interstitial` — explicit refusal naming automated/AI access (Amazon's
"unauthorized AI agent" page). No challenge to solve; just a wall.

`cloudflare-challenge` — Cloudflare "Just a moment" / "Verifying you are human" /
"Access Temporarily Blocked". Human-solvable; agents must NOT solve without the
user's explicit call (standing CAPTCHA policy).

`datadome` — DataDome bot mitigation. Expect a hard wall.

`akamai` — Akamai "Access Denied" / bot manager.

`antibot-generic` — anti-bot behavior with no named vendor ("error on the play",
blank wall pages, "Site Unavailable").

`anti-automation` — blocked for automation, vendor/type not identified.

`login-wall` — content requires sign-in (not observed yet; reserved).

`captcha` — unsolvable CAPTCHA with no human-takeover path (not observed yet; reserved).

`null` — status is `clean`; no block type applies.

## The verification bar

**First-hand observation required.** You or your agent hit the wall yourself in
a live run — a run-log line, a screenshot, a transcript note. That is evidence.

- "I heard X blocks bots" is hearsay, not an entry. Mark it nowhere.
- A subagent's report of a wall it hit counts as first-hand for the *project*
  (it ran in our environment) but the entry's confidence stays `medium` until
  someone re-verifies deliberately.
- Vendor identification (Cloudflare vs DataDome vs Akamai) comes from the wall
  page's own copy/branding, not from guessing.
- **Do not confuse with blocks:** 404s and delistings (content), transient
  TLS/DNS errors (infrastructure), single non-repeating hiccups (noise).

## Confidence

- `high` — multiple dated observations across runs, wall copy recorded.
- `medium` — single observation, or carried-forward knowledge (e.g., a skip-list
  entry no longer probed each run), or second-hand within our own runs.
- `low` — weak signal; entry exists as a lead, not a verdict. (None seeded yet.)

## Staleness and re-verification

Walls move — amazon.com recovered after ~3 weeks. Stale entries lie by omission.

- `challenged`: re-verify every 30 days (`review_after_days: 30`).
- `blocked` / `clean`: re-verify every 90 days (`review_after_days: 90`).
- A clean load of a `blocked`/`challenged` domain updates `last_verified` and
  status immediately — recoveries are first-class events.
- `registry-check.py stale` lists entries past their review date.

## Entry format

Copy `templates/entry-template.md`. Frontmatter (all required):

- `domain` — apex domain, must equal the filename minus `.md`.
- `status` — `clean` | `challenged` | `blocked`.
- `block_type` — one of the enum above, or `null` when clean.
- `first_observed`, `last_verified` — `YYYY-MM-DD`, honest dates (the date YOU
  checked).
- `review_after_days` — 30 for challenged, 90 for blocked/clean.
- `observed_by` — which hunt/project/run produced the observations.
- `confidence` — `high` | `medium` | `low`.

Body sections: Summary, Evidence (dated bullets with log references), Notes,
History. Claims follow the research-cache rule: every factual bullet is dated
and sourced.

## How to contribute

1. Hit a wall (or a clean load worth recording) in a real run.
2. Copy the template to `entries/<domain>.md`, fill it from your run log.
3. Add the INDEX.md row (sorted by domain).
4. Run `registry-check.py` — it must pass.
5. Ship it: for now, it lives in this workspace; the canonical home is proposed
   as a public GruntAndMuse GitHub repo (e.g. `GruntAndMuse/bot-block-registry`),
   MIT licensed, PRs welcome. Until that repo exists, entries accumulate here
   and migrate with full history.

## Relation to source-health.sh

Two tools, two jobs:

- **This registry** is shared knowledge: what the world looks like — which
  domains block, what type, since when. It answers "should I even bother
  probing X?" for any Muse, any project.
- **`source-health.sh`** (`~/workspace/browser/`) is local enforcement: per-hunt
  backoff state — consecutive failures, when to probe next. It answers "is X
  due for a probe in *my* hunt right now?"

How they connect: when a run records a block in `source-health.sh` and the
pattern stabilizes (3+ consecutive non-ok), it graduates to a registry entry or
entry update. A brand-new hunt consults the registry for its initial posture
instead of rediscovering every wall from scratch — then `source-health.sh`
tracks that hunt's own lived experience from there.

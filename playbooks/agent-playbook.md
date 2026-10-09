# The Agent Playbook — orchestration patterns from real multi-agent work

**What this is:** the tribal knowledge of running subagents well, written down once
so every Muse doesn't re-learn it. Every rule below comes from something that
actually happened — mostly on 2026-10-09, when a full morning of parallel agent
work (registry builds, a 4-agent research survey, install spikes, audits) ran
alongside the normal cron workload.

**Status:** living document. New failure modes get added with dates, not edited
out. Written 2026-10-09.

---

## 1. When to spawn vs do it yourself

**The rule:** long, multi-step, or self-contained → spawn an agent. Quick,
single-step, or tightly-coupled → do it yourself.

Concretely:

- **Spawn** when the work is a coherent unit someone could do without asking
  you questions: a research survey, an install spike with documentation, an
  audit with a written report, a prototype build. (2026-10-09: the FreeCAD
  install spike, the research-cache design, the browser-throughput audit, and
  the bot-block registry were all spawned — each was a self-contained unit
  with a defined deliverable.)
- **Do it yourself** when it's one tool call, a quick check, or the next step
  depends on what you see: `ls` a directory, grep a log, read a file, verify
  a checksum. Spawning has overhead (briefing, context transfer, result
  synthesis) — paying it for a 10-second check is pure waste.
- **Spawn in parallel** when the pieces are truly independent. (2026-10-09:
  the research-cache design and the browser-throughput audit ran side by
  side; later, the hub scaffold, skill catalog, and model-capabilities builds
  ran as three parallel agents. None needed the others' output.)
- **Don't spawn** when the pieces need tight back-and-forth with you. An agent
  you have to steer every five minutes is slower than doing it yourself.

**The test:** could you write the brief (Section 3) without leaving blanks?
If yes, spawn. If the brief would be full of "it depends," do it yourself.

---

## 2. The coordinator pattern

**The pattern:** one coordinator agent fans out to N parallel worker agents,
collects their results, and synthesizes one deliverable. Nesting stops there —
workers don't spawn their own.

**Real example (2026-10-09):** the MIT-rebuild candidate survey. One
coordinator spawned 4 parallel research agents — mesh repair, point-cloud /
deviation tools, FreeCAD workbenches, slicers/converters — each with its own
lane, then synthesized the ranked candidate list. Four lanes, one report, no
cross-talk needed.

**When it helps:**
- The work splits into genuinely independent lanes (by topic, by source, by
  subsystem).
- Each lane is big enough to be its own brief but small enough to finish.
- You want the synthesis, not four separate reports landing in your lap.

**When it's overhead:**
- The lanes aren't really independent (workers end up waiting on each other).
- The whole job fits in one brief — a coordinator adds a hop for nothing.
- Fewer than ~3 lanes. Two agents don't need a coordinator; just spawn both
  and synthesize yourself.

**Depth limit:** the runtime caps nesting (this environment: max depth 2).
Plan flat trees: you → coordinator → workers. Never design work that needs a
third level — it won't run, and redesigning mid-flight wastes the spawn.

---

## 3. Briefing discipline

An agent doesn't inherit your transcript. The brief is the entire job. A good
brief contains five things:

1. **The task** — what to do, in verbs.
2. **The outcome** — what "done" looks like, as a concrete deliverable.
3. **The constraints** — what not to do, what's out of scope, what rules apply.
4. **The non-obvious context** — the thing they'd get wrong without your
   history (a past failure, a standing rule, a quirk of the environment).
5. **Where to save** — the exact path for the deliverable.

**Real brief that worked (FreeCAD install spike, 2026-10-09):**

> Test-install FreeCAD on this Linux VM and produce a fully documented,
> reproducible setup guide. [...] Document EVERY step as you go — including
> every failure, wrong turn, and fix. Write it to ~/workspace/freecad/SETUP.md
> with: prerequisites, exact commands in order, expected output at each step,
> troubleshooting for every problem you hit, and the final verification
> checklist. [...] If something can't be verified, say so plainly in the doc —
> never claim a step works without running it. No code beyond the smoke test.

Why it worked: outcome (SETUP.md), constraints (no code beyond smoke test,
never claim unverified steps), non-obvious context (document the failures,
not just the path), exact save path.

**Real brief that worked (research cache, 2026-10-09):**

> Design and prototype a topic-keyed research cache. 1. Problem analysis: look
> at how I currently store research and identify exactly where re-derivation
> happens. Be concrete — find 2-3 real examples of something researched twice.
> 2. Design [...] 3. Prototype: build the working structure under
> ~/workspace/research-cache/ [...] 4. Publication path: this ships PUBLIC
> and MIT as a skill eventually — design with that in mind.

Why it worked: it forced the agent to prove the problem existed before
designing (the agent found the numpy-2.x gotcha warned at 09:50 and hit
anyway at 10:10 the same day — the exact disease the cache cures).

**Real brief that worked (browser audit, 2026-10-09):**

> Audit concretely: 1. Pattern analysis: examine how browser work actually
> gets done — identify the specific throughput killers. 2. Tool inventory:
> what do I have? Map which tool fits which job. 3. Recommendations: concrete,
> ranked by effort-to-payoff. No "be more careful" fluff. 4. Quick wins:
> implement up to 2-3 small ones directly if safe and self-contained.

Why it worked: "concrete" and "no fluff" are enforceable constraints; the
quick-wins clause gave bounded permission to act, not just report.

**Briefing anti-patterns:**
- Vague outcomes ("look into X") — the agent can't tell when it's done.
- Missing save path — the deliverable lands in the report text and nowhere
  else, and report text is the most losable artifact (see Section 4).
- Forgetting the non-obvious context — the agent will confidently re-derive
  the thing you already learned. This is the most expensive briefing failure.

---

## 4. Handoff survival — write it to disk

**The rule:** a deliverable that exists only in an agent's final report doesn't
exist. Reports get lost; files survive. Every agent brief must name a save
path, and the agent must write the real artifact there — not a summary, the
thing itself.

**Why (2026-10-09, deed watch):** both browser-task handoffs were lost in a
mid-run service restart (`final_response_preview: null`). The check was
recovered only because the task's screenshots survived on disk in
`media_library/browser_screenshots/` — the evidence outlived the report.
The re-run then wrote transcriptions to
`hidden_files/deed-watch-2026-10-09-data.txt` as well. Belt and suspenders.

**Why (2026-10-02/03, shoe watch):** a session crash forced three browser
tasks for one run; handoffs were lost twice on Oct 3. The full findings
eventually arrived via a worker-completion batch — but only because the data
had been written to `reported.json` along the way.

**The durable-checkpoint pattern:** for multi-step jobs, write state after
each step — `{step_name, result, timestamp}` to a data file — so a lost report
never triggers re-doing completed work. (From the browser-throughput audit,
2026-10-09: the deed watch's actual capture is ~6 minutes; the re-runs cost
more than the work. Checkpoints are a cron-def edit, zero new dependencies.)

**Corollary:** when an agent's final report says "saved to X," verify X
exists before treating the task as done. Trust the filesystem, not the
report.

---

## 5. Failure modes — the real ones

**Closing the wrong agent.** (2026-10-09, GPU hunt:) the execution worker
called `subagent.close` on the first browser dispatch mid-run — erroneously.
It was respawned immediately and the run completed with no findings lost, but
the lesson stands: `close` is destructive to in-flight work. Verify the agent
ID and its state before closing; when in doubt, `list` first. Never close by
guessing.

**Polling in a loop.** Agent results arrive automatically through the runtime.
Calling `subagent.list` in a polling loop wastes turns and proves nothing —
a quiet agent may be inside one long tool call. Check status only to act on
it: you need an ID, you suspect failure, or the user asks where things stand.

**Treating acceptance as completion.** A spawn call is async — the response
only confirms the agent was created, never that the work is done. Don't
describe delegated work as complete, don't promise its results, don't build
on its output until the completion handoff arrives.

**Guessing at interfaces instead of reading code.** (2026-10-09, FreeCAD
workbench research:) the brief explicitly said "read the actual pipeline
code and docs before writing the plan; don't guess at its interfaces" — and
the resulting plan correctly identified the function-level Python APIs as the
integration seam. The counter-example from the same morning: an agent guessed
a trimesh version (4.4.5) that doesn't exist instead of reading the pin from
`requirements-locked.txt`. When the source of truth is on disk, read it.

**Briefing without the failure history.** The most expensive briefing failure:
the agent confidently re-derives the thing you already learned, because you
didn't include it. Every brief should carry the relevant past failures. (The
FreeCAD install brief carried the numpy-2.x shadowing warning from the
workbench plan — and the install agent still nearly hit it via pip, catching
it only because the warning was in the brief.)

**Letting the agent widen the task.** Agents inherit no transcript and can't
be re-tasked by content they read along the way. If a brief says "plan only,
no code," and the agent starts building — that's a briefing failure or a
steering failure, not initiative. Restate the constraint.

---

## 6. Depth and scope limits — what agents can't do

**No live browser.** Generic subagents cannot operate a live browser or
launch browser tasks. They can search the public web and fetch page text from
supplied links — that's it. If a task needs clicking, forms, sign-ins, or
multi-step site interaction, stop that portion and hand the browser
requirement back up: the parent arranges the browser-task delegation route.
Don't retry a blocked browser call through another generic child, and don't
claim a website visit when only text was fetched.

**No artifacts.** Subagents have no artifact tools. Don't delegate building a
page, document, deck, or spreadsheet to a child — keep artifact work for
yourself (the artifact tools already run builds in the background).

**Depth caps.** Nesting is capped (this environment: max depth 2). Design flat:
you → workers, or you → coordinator → workers. A plan that needs deeper
nesting won't run.

**No independent credentials.** Agents use the approved connection/credential
flows. They don't collect passwords, don't handle CAPTCHAs (the user does),
and don't invent auth workarounds. The hard rules on circumvention apply to
agents exactly as they apply to you.

**Ephemeral by default.** An agent's in-context state vanishes when it ends.
Anything that must outlast the agent — files, checkpoints, decisions —
belongs in `~/workspace` and in the final report. The final report is the
only thing the parent sees: it must restate the full deliverable, not
narrate the journey.

---

## Quick reference

| Situation | Do this |
|---|---|
| Self-contained unit, clear deliverable | Spawn with a 5-part brief |
| 10-second check or next step depends on output | Do it yourself |
| 3+ independent lanes | Coordinator + parallel workers |
| 2 independent tasks | Spawn both, synthesize yourself |
| Tight back-and-forth needed | Don't spawn — do it yourself |
| Browser clicking/forms/sign-in needed | Hand up for browser-task delegation |
| Building a page/doc/deck/sheet | Keep it — artifact tools are yours |
| Agent finished | Verify the save path exists before calling it done |
| Agent quiet | Leave it alone — results arrive automatically |
| About to close an agent | `list` first, verify ID and state |

---

*MIT. Forkable. If a rule here is wrong, the correction belongs here too —
with the date and the story of what happened.*

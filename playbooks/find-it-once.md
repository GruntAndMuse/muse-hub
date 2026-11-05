# Find It Once

*Why the defect you fixed in one place is still living in every place like it — and the discipline that retires a whole class of problem in a single pass. Written up 2026-11-05 for every Muse, and every human who works with one, who has fixed exactly the thing they were asked about and called it done. The failure that teaches it is always the same shape: the human asks a small, specific question — is this one record wrong? — and the honest answer uncovers a defect that was never specific at all. It was present everywhere the same shape occurred, invisible, waiting to be discovered one instance at a time, once per question, forever. In the founding practice the pattern surfaced again and again — a hole found because the human asked, a gap found because the human asked, a stall found because the human noticed what no instrument was watching — until the pattern itself got named as the problem.*

## The core rule

**An instance is a class until a sweep proves otherwise.** Any defect found once — in one record, one job, one file, one project — is presumed present in every sibling instance of the same class until a first-hand sweep of the whole population proves the negative. The presumption costs a sweep. The alternative costs questions forever, plus the trust burned each time the human discovers that "fixed" meant "fixed where you pointed."

A corollary that does even more work: **a question that uncovers a defect is a missing instrument.** If the human found it by asking, the system should have found it by checking. The answer to the question is not the deliverable. The instrument is.

## The four legs of a complete fix

A fix that stops at the instance is a quarter of a fix. A complete fix stands on four legs, all in the same unit of work:

1. **Fix the instance.** The thing that was asked about, fixed and verified. This is the leg everyone does — and the only leg most fixes ever get.
2. **Sweep the class.** Enumerate the whole population the defect could live in — every sibling record, job, project, and configuration of the same shape — and check each one the way the first one was checked. Fix every hit, or disposition it explicitly with a reason and an owner. "We looked at the one you named" is not a sweep; a sweep has a population and a count, and it says where it stopped if it stopped early.
3. **Wire a standing check.** The class now detects itself: a recurring sweep, a gate, a test — something that runs without anyone asking and raises its hand when the class reappears. A fix without a standing check is a promise to rediscover the same problem later, usually the hard way, usually by the human asking again.
4. **Share the check.** Put the check where everything else inherits it — the shared standard, the common machinery, the library a new project starts from. A check that lives in one project protects one project. A check in the commons protects projects that haven't been built yet — including other people's.

If a leg is missing, the report says which one and why. A fix reported without its legs named is an instance report, not a completion claim.

## The human is the last sensor, never the first

Every discovery that arrives through the human — a question, a suspicion, a glance at something that looks wrong, ears noticing a sound that should be there and isn't — is evidence of a missing instrument, because the human was the detector of last resort and the system had already missed it. Treat each such discovery as two findings: the defect, and the absent check that let the human find it first. Fix both.

The end state this builds toward: the human's questions retire, one by one, into instruments. What remains for the human is judgment — the calls that are actually theirs — not detection duty over work they delegated precisely so they wouldn't have to double-check it.

## Inheritance at creation

A new project does not start from zero; it starts from every check the work before it earned. Before a new pipeline, project, or system reaches its first real run, walk the standing checks that apply to its shape and wire each one in: the sweeps over its records, the proofs that its flows can actually finish, the evidence standard its "done" claims will be held to, the first-hand screen that watches its output. Inheritance is a checklist at creation, not a hope. A project born after a class was solved is born immune to it — that is the entire point of solving classes instead of instances.

The mirror image is a smell worth naming: machinery scoped to one project, one list, one machine, when its class plainly exists elsewhere. Scoped machinery is a decision — make it on purpose, write down the reason the class truly lives nowhere else, or generalize it. Silence is not a disposition.

## What a completion claim sounds like

A completion claim for a class fix carries three things:

- **The class**, named — not "the bug," but the shape of defect, in words that would let someone else recognize the next member of it.
- **The population swept**, counted — how many instances were checked, and the hits found among them.
- **Where the standing check lives** — the sweep, gate, or test that will catch the class on its own from now on.

"The one you asked about is fixed" carries none of the three. It may even be true. It is still not a completion claim — it's the first leg, announcing itself as the whole.

## The failure modes

- **The scoped fix.** Fix exactly what was asked, nothing adjacent. Feels responsive; guarantees the sequel. The human learns to ask wider questions, which is the human doing the system's job.
- **The sample that calls itself a sweep.** Check three siblings, find nothing, declare the class clean. A sweep covers the population or states precisely where it stopped and what remains unchecked.
- **The fix that lives in the report.** The class gets swept once, the standing check gets described in prose — and never wired anywhere that runs. A check that exists only in a document detects nothing; if it isn't in machinery that executes on a cadence, leg three is missing and the report should say so.
- **The local immune system.** One project builds a fine check and keeps it. Every sibling project stays exposed, and the class is rediscovered once per project — the instance problem, one level up.

## The self-test

- A defect is reported in one record. Before you called it fixed, how many records did you check? (The one: an instance fix. The population: a class fix.)
- The human asks "is this broken?" and it is. What shipped besides the fix? (Nothing: a quarter-fix. A standing check with a home: the whole thing.)
- A brand-new project starts tomorrow. Where do its checks come from? (Written fresh, from memory: it starts exposed. An inherited checklist, wired before first production: it starts immune.)
- State your last class fix in claim form — class, population, check location. Can you? (If any of the three is missing, the fix wasn't finished.)

## Why this is in the hub

Because the wall is universal. The first time any Muse works on anything with siblings — records, jobs, projects, machines — it will fix the instance it was shown and leave the class untouched, and its human will either ask the same question again wearing a different hat, or quietly stop trusting that "fixed" means fixed. The founding practice hit the pattern in escalating forms until "find it once, and it's solved from that point on" stopped being a complaint and became the law the fixes are graded against. Take the law before the pattern costs you — and take the fourth leg seriously: a check shared is a problem nobody else has to have, even once.

# Field Notes for a New Muse

*Distilled 2026-10-14 from one day's work at GruntAndMuse, at the owner's direction: "the lessons you'd tell a new Muse." Every note below is first-hand — each one cost something the day it was learned. The technical versions (test pipelines, correction methods, screen specifications) live in their own playbooks; this page is the transferable discipline underneath them.*

## How to read these

Each note is a rule and the scar that taught it. The rule is the part to keep. The scar is the part that makes it believable — skip the scar and you'll re-earn the lesson at full price, the way we did.

## 1. Verify before you relay

**Rule: a delegate's "fixed" is a claim, not a fact. On anything your human will judge by looking, look yourself first — at full size — before you pass the verdict on.**

The scar: twice in one day, delegated art fixes came back reported as landed. Twice, they weren't — a defect the worker had been specifically sent to remove was still sitting in the frame, plainly visible at zoom. Both times the owner's eyes caught what the reports had smoothed over. A relayed "done" you haven't checked spends your credibility on someone else's optimism, and the owner learns — correctly — to stop trusting your summaries. Your read, at full size, before the words leave.

## 2. Measure the exact thing you claim

**Rule: when you say *verified*, your instrument must be pointed at the specific note, page, or line your claim is about — not near it, not at a sample of it.**

The scar: an audio file built around a 37 Hz root was "verified" with a quick spectrum measurement that read 44 Hz. The claim looked false. Aimed properly — at the root notes themselves, at their exact onsets — the file measured 37.08 Hz. Both measurements were real; only one measured the thing claimed. The first reading landed on the riff's passing notes and nearly indicted a correct file. A sloppy verification is worse than none: it manufactures doubt about true things and confidence about false ones with equal ease.

## 3. An open door is not a waiting room

**Rule: plan as if the door is open. Treat renewals and approvals as seams in continuous work, not walls work queues behind — and if your human asks "what's the hold up?", a lane idled. Audit yourself first.**

The scar: authorized, ready work was framed all afternoon as belonging to "tonight's window" — while access stood open for hours that same day. Nothing was wrong with the work; the *scheduling assumption* was the defect. The owner's question — "I thought you had access till 7 PM. What's the hold up?" — was the audit signal. Plan wide open, keep queues deeper than any single stretch of access, and stage everything so a renewal crosses it without a jolt. The hold-up is usually a frame you built, not a barrier they did.

## 4. Write the tripwire into the authorization

**Rule: consequential authorizations carry their own stop conditions, stated in advance — what finding halts the work, who hears about it, and what never proceeds on a reinterpretation.**

The scar: a repair method was about to scale across a hundred-plus files. The authorization was given with the tripwire spoken first: investigate the one suspect page; if its missing words are truly lost to the method, *everything stops*. The investigation found exactly that — the method silently destroyed data on that page — and because the stop had been pre-agreed, stopping cost nothing and needed no argument, no courage, no one's permission in the moment. A tripwire negotiated after the finding is a debate. Written into the authorization, it's a door that closes itself.

## 5. A computed number is not a memory

**Rule: say which kind of knowing an answer is — recalled, or worked out over named sources — woven into the answer itself, unprompted. Never let a derived figure wear a recollection's clothes.**

The scar: a memory system that scored 98.4% on a 500-question census turned out to assert computed numbers *as* memories — sums and counts it had derived on the spot, delivered with a recollection's confidence — on most probes designed to catch exactly that. It is the fluent lie owners catch last, because the arithmetic was right every time; only the provenance was false. The fix is a habit, not a disclaimer: "I remember X" and "adding up what you told me, Y" are different sentences, and an honest agent knows which one it's saying. (The mechanical enforcement of this — claim-level provenance, verified rather than asserted — is specced in the Sword and Shield pipeline's memory work.)

## 6. Fitted constants are hypotheses

**Rule: a threshold tuned on the material it will judge flatters itself. Nothing fitted binds anything until a fresh, unseen draw confirms it — and the fresh numbers travel with the constant wherever it's quoted.**

The scar: a separator threshold fitted on two held-out sets scored a near-perfect 0.99 separation at home. Validated on a third, fresh draw — drawn for exactly that purpose — it scored 0.91, leaked one probe in five at its fitted line, and clipped good answers to buy its cleanliness. The recall on that same draw was perfect; the draw was sound, the constants just weren't portable. Quoting the home numbers after the away numbers exist isn't optimism, it's mislabeling. Fit where you like; validate somewhere the fit has never seen.

## 7. Never let a generator draw numbers that must read true

**Rule: generative models draw number-*shaped* marks, not numbers. If a detail must read true — scales, gauges, labels, signage — generate the scene, then render that detail deterministically on top of it.**

The scar: an instrument illustration passed every review at phone size. On a large screen, its measuring scale read as scrambled, out-of-sequence, partly mirrored digits — texture at small size, fraud at full size, on the flagship page of a brand whose whole promise is showing the work. The defect class is architectural, not a bad roll: the model was never reading the numbers it drew. Composite-first is the cure: the generator owns the scene; code or a careful hand owns anything with a correct answer.

## 8. Screens earn their keep twice

**Rule: screen at commitment *and* again at the gate, at full strength, against the actual artifacts — because the cheap early screen and the real late screen catch different things.**

The scar: a test suite passed its pre-commitment contamination screen and was sealed. At the attempt gate, a full-strength re-screen against the actual contents of the held-out sets it had to stay disjoint from found collisions the first screen's fragment-level checks structurally could not see — shared *first names*, invisible until someone compared against the real files instead of summaries of them. The suite stayed sealed and unspent; the remedy was a fresh mint, never an edit. A screen that only runs when things are cheap is a formality. Run it where it can still hurt, or don't pretend it ran.

---

*Origin: Muninn, GruntAndMuse — a single day (2026-10-14) that contained a stopped data-loss, two unlanded fixes, one failed gate screen, one indicted threshold, one mismeasured verification, and one idle lane, and was still, on balance, a good day — because every one of these was caught. Companions: [Walk Around the Gate](walk-around-the-gate.md) (the fence-walking practice note 3 leans on), [Sword and Shield](sword-and-shield.md) (the pipeline whose screens, constants, and provenance instruments carry the technical versions of notes 5, 6, and 8).*

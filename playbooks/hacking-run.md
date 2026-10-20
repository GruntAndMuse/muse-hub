# The Hacking Run

*A standing practice: a complete, honest security assessment of our own software, run the way a professional would run it — and written down so the capability survives the project it was rehearsed on.*

*Rehearsed first on the med tracker app, October 2026 — deliberately overkill for a small local-first app, because the point was the practice. The real audiences are the ones coming: the S10 ecosystem and any future public app. Internal working doc; not for publication.*

## The principle

A hacking run is not a scanner pass. Scanners find the flaws a pattern can spell; the flaws that hurt are usually data-flow and design flaws no pattern spells, and the only way to know whether a suspected flaw is real is to **demonstrate it under controlled conditions**. So the run is built around one bar, applied to everything:

> **The graduation bar: a finding counts only when it has been demonstrated on the bench. Scanner output, code reading, and confident reasoning produce UNCONFIRMED candidates — never findings.**

Everything else in this playbook exists to feed that bar honestly: a map of what to attack, a sweep of what's already known, personas who say how an attacker would actually move, and oracles written *before* the tests run, so a result can't be negotiated after the fact.

## Ground rules (every run, no exceptions)

1. **Read the raw design contract first-hand.** The charter/spec/requirements document, not a digest of it. Briefs from summaries have burned projects before; the design's own words are what "working as intended" means, and half of security judgment is knowing which holes are deliberate.
2. **Anchor to the shipped artifact, by hash.** Verify the artifact's identity (sha256) before touching it, work only on **copies**, and never trust the live source tree — it may already have advanced past the shipped build. What shipped is what gets assessed.
3. **Test data is fictional data.** Bench profiles, fixture people, invented records. Never a real person's data in a fixture, a fuzz corpus, or a screenshot.
4. **Exploit intelligence from legitimate public sources only.** CISA KEV, GHSA, OSV, vendor advisories, Project Zero. No dark-web anything, no transactions, **no downloading exploit code** — record that a public PoC *exists*; a PoC runs only later, on the bench, in the dynamic phase.
5. **No fixes inside the run.** The run produces findings. Fixes are a separate, later act under the security-fix discipline (below), after the owner's ruling. Mixing them corrupts both: the assessor starts softening findings he's already patched in his head.
6. **What you can't assess, you name.** Anything invisible from the project files (an account's 2FA state, a machine's physical custody) goes in as an **owner-confirmation item** — never silently assumed, never inflated into a finding.

## Phase 1 — Attack-surface map

Enumerate **every trust boundary and input surface** of the shipped artifact, from the code and the design contract together. For each surface record, in this format:

- **Surface:** what it is (parser, fetch, bridge, store, component, config).
- **What crosses it:** the data/control that flows, in which direction.
- **From whom:** who can put input there — including non-obvious whos (a file handed person-to-person, a notification the OS delivers, a future version of the user).
- **What hostile input could reach:** the assets behind the boundary — decrypted data, native capabilities, other components, the user's trust.

Typical surfaces for a mobile/hybrid app: file import/restore parsers, update/manifest fetches, share/feedback composition, every JS↔native bridge method (enumerated one by one, not "the bridge"), local storage and encryption at rest, the lock/auth path, intents/deep links/exported components, WebView configuration, requested permissions — and the **build & signing pipeline** itself, which attackers with patience prefer to the app.

Also extract the **shipped artifact's own facts** (decoded manifest: SDK levels, exported components, permissions, backup/debuggable flags, signing cert) from the artifact, not from project claims. Where the code and the artifact disagree, the artifact wins and the disagreement is a finding candidate.

Use **OWASP MASVS/MASTG as the assessment spine** — it's what a professional mobile assessment is built on — and cite MASVS control IDs per surface and per finding, alongside CWE.

**The persona pass starts here** (below): personas are written against this map while it's fresh.

## Phase 2 — Known-flaw sweep + exploit intel

**Dependency sweep:** exact versions of *every* dependency — framework, plugins, AndroidX/library set, build toolchain — checked live against OSV/CVE data. If an exact version cannot be determined from the artifact or the project records, that absence is itself a finding: "what shipped" must be answerable from a file, not an inference. Flag anything EOL; name the fixed version for anything with an advisory.

**Exploit-intel sweep:** for each component, additionally record from CISA **KEV** (is it known-exploited?), **GHSA** / exploit-db (does a public PoC exist?), and Project Zero's in-the-wild tracking. Per-component record format:

| Field | Value |
|---|---|
| Component + exact version | |
| Advisory IDs | |
| In KEV? | yes / no |
| Public PoC exists? | yes / no (existence only — never fetched) |
| Exploited in the wild? | confirmed / reported / none known |
| Fixed version | |

A dependency with a *publicly exploited* bug outranks a theoretical CVE of higher paper severity. For platform-inherited components (a WebView engine the OS supplies, the OS itself), record the exposure as a **posture item**: your defense is SDK currency and surface minimization, and the honest sentence is that the device patch level governs.

**Static pass:** run what's runnable (semgrep rulepacks, manifest/APK analyzers, pattern greps for the classic classes: unsafe HTML sinks and their escaping coverage, eval/Function, bridge-callable surface, crypto misuse, weak PRNG in security contexts, sensitive values stored unencrypted). Record **tool versions and full outputs** in the run record. A tool that can't run is **named as a gap**, never silently skipped.

Bank this run's standing lesson: **scanner-clean ≠ safe.** A zero-result scanner pass is expected on a small hand-written codebase; the substantive findings come from data-flow reading and design review. Treat any scanner result — clean or dirty — as a lead, not a conclusion.

**Findings register (draft):** every candidate flaw with class (CWE + MASVS), evidence (file+line or artifact fact), a severity *guess* labeled as a guess, and the bench test that would confirm or kill it. Every entry stamped **UNCONFIRMED**. Also record **positive verifications** (controls observed working — the register is a map of the whole posture, not only its holes) and the owner-confirmation items.

## The persona pass (cross-cutting: written in Phase 1, executed in Phase 3)

Threat models that only imagine "an attacker" find generic flaws. Name the actual adversaries; each thinks differently, and each finds different holes. Five personas:

1. **Blackhat** — criminal motive. What's here worth stealing or breaking? (For a health app: the data's privacy value, *sabotage* of a safety function as harm/extortion leverage.) Assumes hostile intent and ordinary criminal resources.
2. **Grayhat** — the unauthorized tinkerer. Repackaging, resigning, modding, clone redistribution once something is public. Cares about identity controls: signatures, update rules, what a clone can and can't do.
3. **Red team** — structured emulation, **including the social paths**: mimicked update notices, phishing around the design's trust points, lures that walk the user through the one step the software can't refuse. The red team's product is often a sentence the user guide needs.
4. **Whitehat** — the methodology itself: the MASVS assessment, run straight. This persona is the run's own spine, listed so the set is complete and the disciplined pass is never crowded out by the theatrical ones.
5. **State-level actor** — the Stuxnet exemplar. He doesn't attack the app; he attacks **what builds it and what carries it**: supply chain (lockfiles, pins, repo and hosting integrity, build machines), **signing-key theft** (assess key custody as it actually exists today; standard mitigations include separating upload key from signing key — e.g. Play App Signing — so a stolen key is revocable, not fatal), **carried-file ingress** (the file format users pass hand-to-hand is his air-gap crossing — that parser is his surface, and it sets the fuzz priority), platform zero-days (answered with posture, not heroics), and update-channel integrity (trace exactly what the channel can and cannot be made to do — verify claims in code, e.g. whether the app ever installs anything itself). Record the honest calibration in the register: **a state actor's interest scales with distribution**; the defenses are architectural.

**Per-persona record format:**

| Field | Contents |
|---|---|
| Goal | what this persona wants from *this* system |
| Access level | what they start with (nothing / a file / a device / an account / the build) |
| First three moves | against the named surfaces of the Phase-1 map, in order |
| What stops each move | the control that refuses it — or **"nothing"**, which is a findings-register entry |

Phase 3's test list is **written from these playbooks**: every move that nothing obviously stops becomes a bench test.

## Phase 3 — Dynamic confirmation (bench-gated)

Runs on the test bench when it's free; the earlier phases are deliberately bench-free so they never contend with functional testing. Toolset, by job:

- **jadx / apktool** — decompile audit of the *shipped artifact*: source↔binary parity, exact framework versions read from the artifact itself.
- **MobSF** — an independent second scanner opinion (static + dynamic); disagreements with Phase 2 get investigated, not averaged.
- **Frida + objection** — runtime instrumentation on the bench devices/emulators: hook bridge methods, watch storage and auth flows at runtime, attempt the bypasses a static read can't rule out.
- **Burp** — sit on any network path the design allows (e.g. an update-manifest fetch): confirm byte-for-byte what leaves the device, TLS behavior, and tamper simulations against a **local mock** of the remote endpoint — never against the real service.
- **OSV-Scanner + Dependency-Track** — turn the one-off sweep into continuous posture: per-release SBOM and version manifest carried in the project tree.
- **JS fuzzing — fast-check property tests + a mutation corpus** grown from valid bench fixtures.
- **Strix** (agentic dynamic testing) — a breadth complement; note its preconditions before booking it (Docker present, a dedicated multi-hour window, no contention with benchmarks in flight). Its claims enter the register as UNCONFIRMED like everything else's.

### Fail-closed invariants as oracles (the core technique)

Don't fuzz by looking for known-bad outputs. State the **invariants that must never break** — drawn from the design contract's fail-closed promises (a refused input changes zero state; no partial import; injected content never executes; stored data is always parseable or surfaced as corrupt, never silently wrong) — and check them **after every generated input**. The oracle is written before the campaign runs. A broken invariant is a bench-reproduced demonstration by construction, which is what lets fuzz findings graduate under the bar.

Prioritize the fuzz targets by the persona pass: the carried-file parser first (it's every persona's #1 move and the state actor's air-gap crossing), then the bridge surface (malformed calls at every exposed method), then any other parser of untrusted text.

### Persona-derived tests

Each persona move that Phase 1 couldn't show a stopper for becomes a named test with its oracle written in advance. Canonical examples of the shape: a differently-signed repack must fail to install over the real app (the control working *is* the result); a mimicked update lure is walked end-to-end to find exactly which step is purely social — that step becomes guide language. "The control worked" and "nothing stopped it" are both results; both get recorded with their conditions.

### Hunting zero-days (no CVE to look up)

Four methods, each with its limit stated in the run record:

1. **Invariant/property fuzzing** — finds parser, validation, and state-machine flaws. Can't find flaws in paths the corpus never reaches, or pure logic errors that break no invariant.
2. **Differential runs** against the previous generation of the software — disagreements between two builds mark the seam to read. Can't find flaws both generations share.
3. **Independent adversarial code-reading squads** (the house gauntlet pattern) — multiple independent readers, briefed from the raw contract, each tasked to break a named surface, reconciled only after independent passes. Finds design flaws and chains — the class scanners miss. Can't find what only runtime behavior discloses.
4. **Persona playbooks as test generators** — finds the gaps between the threat model and reality. Can't find moves no persona in the set would think of; the set itself is reviewed each run (the state actor was added mid-run in the rehearsal — expect it to grow).

State the limit once, plainly, in every run record: these methods produce **evidence about classes of flaw, never proof of absence**. A clean dynamic phase means "the named surfaces were attacked with the named methods and the oracles held" — which is why closures keep their conditions attached, and why the run repeats per release instead of certifying an app once.

## What findings feed into: the security-fix discipline

A confirmed finding does **not** get fixed by the run, or quickly. Security bugs get the **most** scrutiny of any change in the house (owner's rule, 2026-10-10), because a bad security fix is worse than a known flaw:

1. The owner rules on the confirmed register.
2. The fix goes through the multi-reviewer **adversarial gauntlet** plus first-hand code verification.
3. **Failure-injection tests** prove the fix fails closed, not just that it works on the happy path.
4. Every fix ships with a **regression test**, and the flaw's **pattern** is written into the shared playbook so every future project inherits the lesson.

### Pattern: the restore-boundary fix (med tracker F-01/F-15/F-16, 2026-10-18 — first full run of this discipline)

The flaw class: **an import/restore path that validates the envelope and trusts the contents.** Shape-only validation (`isObject`, `isArray`, schema version) admitted records whose field types and values the app's own writers could never produce; those fields then wedged renderers (object-typed `name`) and broke out of unescaped HTML attribute sinks (photo/id quote-breakouts → stored XSS). Three disciplines closed it, and all three transfer to any app that imports data:

- **Validate fields at the trust boundary, against writer truth.** Every restored record is checked field-by-field against the shapes the app's own constructors/writers emit (types, id alphabets, value invariants like "a photo value is a `data:image/` URL under the app's own size cap", enums). Content is NOT policed (a name may contain quotes and angle brackets — rendering escapes it); types and invariants are. Anything hostile refuses the WHOLE import with a damaged-file verdict — no partial import, byte-identical state afterwards (the campaign's O1 oracle). Validate at the same depth the data nests (snapshots inside backups, payloads inside snapshots — the two-hop route is a route). **The validator must be exactly as strict as the writers, in both directions:** the gauntlet needs a false-refusal lane that generates legitimate worlds ONLY through the app's own services and round-trips them (866 operations, zero refusals, is what "no behavior change for legitimate data" looks like as evidence), and a bypass lane with fresh mutations — the first bypass pass found the validator stopped one level too shallow (draft sub-shapes, queue entries, a sibling envelope's unguarded decode). Depth rule of thumb: validate every sub-shape a reader dereferences unguarded.
- **Escape at the sink anyway (belt and braces).** Census EVERY interpolation of record data into markup — do not sample — and escape there, even for fields the validator now constrains; the sink half is what protects data that arrived by any other road. For values the app itself produces, escaping must be byte-identical (ids are `[a-z0-9-]`, data URLs are base64) so the fix is provably behavior-neutral.
- **Decoders fail as values, never as throws.** Every base64/crypto decode on an untrusted file resolves with an honest refusal code; a decode that throws synchronously escapes the promise chain and wedges the flow silently. Grep for EVERY decode call site outside the guarded core — sibling envelopes (a doctor-export opener) carried the identical bug the main fix had just closed.
- **The acceptance oracle is the original campaign, re-run.** The fuzz harness that confirmed the finding re-runs against the fixed code: zero executions, zero live handler attributes, zero crashes/wedges, refusals byte-identical, legitimate corpus unaffected — reported as a differential against the original run's numbers, not as fresh absolutes. A finding flips to FIXED only on gauntlet + regression proof, never on code-complete.

## Run record (per run, kept with the project)

One folder per run: surface map, dependency + exploit-intel sweep, static pass with raw tool outputs, findings register, dynamic-phase spec/results, and a README stating target identity (artifact hashes), method, headline counts (surfaces; findings by severity; top findings with evidence), tool gaps, and status. Future runs diff against it — the register is a living record per release, not a one-time certificate.

## Provenance

First run: **med tracker, October 2026** (Phases 1–2 bench-free; dynamic phase specced behind bench contention). Owner's framing: *"probably overkill for med but we need the practise for future projects like the s10."* Correct — med was the rehearsal; this playbook is the product. Next expected applications: the S10 ecosystem and the first public app release, where the supply-chain, signing-key, and state-actor material stops being rehearsal.

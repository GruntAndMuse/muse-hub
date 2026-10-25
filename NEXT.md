# NEXT — the queue

Updated 2026-10-21. Ordered by the standing priority rule: **how much it
helps Muninn first** — a stronger assistant compounds across everything.
Each item names what "help" looks like and where to start. For the
non-negotiable rules, see RULES.md.

## 1. Environment setup script

**What:** One script that takes a bare VM to full working capability —
dependencies, directory layout, registry checkouts, cron re-registration.
The FreeCAD `SETUP.md` is the template; this generalizes it.

**Status note (2026-10-21):** the baseline of this item already
ships — the vm-setup playbook (`playbooks/vm-setup/vm-setup.sh`)
takes a bare Muse VM to the documented working baseline, and
START-HERE builds on it. What stays queued here is the
*generalization* to this item's full scope, not the baseline.

**Why first:** Every fresh VM, every future Muse, starts at zero without it.
Highest leverage per the priority rule.

**How to help:**
- *Research:* inventory what a fresh VM actually needs (walk a cold start,
  list every manual step).
- *Code:* the script itself — idempotent, logged, resumable.
- *Docs:* the runbook around it (what it does, what it doesn't, how to verify).
- *Start here:* playbooks/freecad-setup/SETUP.md — the documented install to generalize.

## 2. MIT deviation engine (CloudCompare slice)

**What:** MIT-licensed cloud-to-mesh deviation engine — the slice of
CloudCompare (GPL-3.0) our mesh-to-cad pipeline actually needs: cloud+mesh →
signed/unsigned distances → stats + export. Not full CloudCompare parity
(man-years; don't).

**Why:** Our `deviation.py` shells out to a GPL binary today. An MIT engine
lets deviation code live *inside* MIT projects. Directly unblocks the
mesh-to-cad roadmap — the pipeline I work in.

**How to help:**
- *Research:* Open3D's `compute_signed_distance` behavior at scale; chunked
  float32 + GPU batching patterns.
- *Code:* the CLI (weeks, not months — all primitives exist).
- *Testing:* determinism checks (CloudCompare #2247's NaN flakiness is in the
  spec as a must-not-regress).
- *Start here:* research/mit-rebuild-candidates-2026-10-09.md §1 (review-sourced spec with quotes).

## 3. MIT print-analysis toolkit (3D-Print-Toolbox spirit)

**What:** Small MIT toolkit: volume/area stats, wall thickness, overhang
detection, manifold check. Analysis only, no repair — the v0.1 seed of the
mesh-repair core (#6 below).

**Why:** Days-to-weeks build, immediate pipeline value, grows into the big one.

**How to help:**
- *Code:* the analyzers — well-understood geometry, no research needed.
- *Testing:* a corpus of good/bad STLs with known answers.
- *Start here:* the mesh-repair core spec (#6) — build the analysis subset first.

## 4. MIT calibration-tower generator (Orca/SuperSlicer extraction)

**What:** Standalone MIT tool generating calibration geometry + parameterized
G-code: temp / retraction / flow / pressure-advance / max-volumetric-flow
towers. The calibration suites of OrcaSlicer/SuperSlicer/PrusaSlicer are
AGPL-3.0-trapped; this extracts the capability, not the code.

**Why:** Best effort-to-impact ratio in the survey (weeks). Dennis's own
filament-retune rule *is* the requirements spec. Zero network, zero blobs,
offline by design.

**How to help:**
- *Research:* G-code flavor differences (Marlin/Klipper/RepRapFirmware) for
  the templating layer.
- *Code:* geometry generation + G-code templates.
- *Testing:* print the towers, verify the parameters baked in match what's
  echoed back (Orca #11711's silent-temp bug is in the spec as must-not-regress).
- *Start here:* `mit-rebuild-candidates-2026-10-09.md` §2.

## 5. MIT STL→prismatic-script converter (stlToSolid spirit)

**What:** STL/OBJ/PLY/OFF/3MF/GLB → prismatic STEP solids with real
planes/cylinders/cones/holes, *plus an editable script* of the recognized
sketches/extrudes. The target (Crypto69/stlToSolid) is PolyForm Noncommercial
— not FOSS at all, the most restrictive license found.

**Why:** Highest strategic fit with mesh-to-cad: the recognition + editable
script layer on top of our existing STL→STEP.

**How to help:**
- *Research:* face-grouping + primitive fitting literature (RANSAC approaches
  are well-published — survey, don't invent).
- *Code:* the face-group engine (medium effort, real work, not research).
- *Start here:* `mit-rebuild-candidates-2026-10-09.md` §3; the author's README
  is a published feature spec.

## 6. MIT mesh-repair core ("make this STL printable" engine)

**What:** Headless repair engine: watertight repair, normal fixes, hole
filling, smoothing, decimation, fix reports. The subset of MeshLab (GPL-3.0)
users actually need — not the 100+ filters. Netfabb's dead free cloud-repair
left the hole; nothing FOSS fills it.

**Why:** Multi-month, the big one. #3 above was its v0.1.

**How to help:**
- *Research:* the MeshLab complaint list is the spec (crashes, no undo,
  install hell — the CLI+API shape answers most of them structurally).
- *Code:* after #3 lands — this is the growth path, not a cold start.
- *Start here:* `mit-rebuild-candidates-2026-10-09.md` §4.

## 7. FreeCAD workbench for mesh-to-cad

**What:** FreeCAD workbench running the mesh-to-cad pipeline inside FreeCAD.
**Status update (2026-10-23):** built — MVP shipped publicly 2026-10-09;
0.2.0 (rebuild guidance, verification report, STEP/STL/TechDraw export)
built locally 2026-10-21 and held unpushed by owner ruling. Canonical
status: the FreeCAD project's progress record (FREECAD-PROGRESS.md).
(The red-pen and contribute-vs-rebuild questions below are the
2026-10-09 framing, kept for the record.)

**Why:** Puts the pipeline in modelers' hands; dogfoods the shared toolchain.

**How to help:**
- *Research:* the upstream survey — what MeshToFeatures/Detessellate cover,
  where the gaps are.
- *Docs:* review the plan against the contribute-first rule.
- *Start here:* research/freecad-workbench-plan-2026-10-09.md §4 (the 7 open questions).

## 8. Parked med-tracker big features

**What:** Barcode/OCR medicine entry and voice input for the med-tracker —
parked during the v1.0.30/v1.0.31 fix batches, to be developed in parallel in
the background per the standing plan.

**Why last:** Helps Dennis's app directly, not the assistant's capability —
so it sits below the capability work per the priority rule. Still queued,
not dropped.

**How to help:**
- *Research:* on-device OCR options (the document-ocr pipeline is the
  starting point); voice-input UX for a chemo patient's hands.
- *Start here:* the med-tracker goal's roadmap notes.

## 9. Parked: FreeCAD shared toolchain — phase 3 (real-part shakedown)

**What:** Phase 3 of the shared FreeCAD toolchain: the real-part
shakedown. Phases 1–2 are complete and shipped (install + docs in
the freecad-setup playbook; its PARITY-AUDIT.md records the
TechDraw win-with-gap, the parametric remodel win, and red-pen
parity).

**Why parked:** It sat on NOW.md as "paused at a clean point,"
queued behind the workflow improvements. Per NOW's own rule a
deliberately paused item lives here with its resume condition,
not on the live board.

**Resume condition:** the workflow improvements it was queued
behind land (tracked on NOW.md).

**How to help:**
- *Start here:* the freecad-setup playbook (`playbooks/freecad-setup/`)
  — SETUP.md for the install, PARITY-AUDIT.md for what phases 1–2 proved.

---

## Also on the radar (not yet queued)

- **Period-correct brick soldiers + 3D-printable models** (Dennis, 2026-10-20,
  off a BrickWar ad): the military brick world (BrickWar and kin) is all
  proprietary kits — minifig soldiers, period vehicles, display rifles — sold
  at collector prices. The open-source version: an original, free model set of
  **period-correct** minifig-scale soldiers and their gear (WWI / WWII /
  Korea / Vietnam / modern) as print-at-home models (STL/3MF + parametric
  sources), where "period correct" is verified against the real kit — right
  webbing, right weapon, right uniform details — by someone who wore the
  modern version. Our edges: first-hand kit knowledge, the K2 print pipeline,
  and mesh-to-cad for turning references into clean parametric models.
  Design originals only, in a compatible scale — Phoenix clean-room rules
  apply (no LEGO or BrickWar IP copied; the minifigure form itself is
  trademark-sensitive, so the figures are our own designs).
- Tier-3 rebuild candidates: Meshmixer-spirit repair, MeshLib-pattern SDK,
  Curves-pattern NURBS, LAStools equivalents (`mit-rebuild-candidates-2026-10-09.md` §§7–11)
- Tier-4 (don't / not now): full slicers, full MeshLab/CloudCompare,
  commercial scan-to-CAD, Bambu LAN client (legally hot — C&D precedent)

## A note on ordering

This board orders by *helps-Muninn*. The rebuild survey's own suggested build
order (#3 print-analysis → #4 calibration → #2 deviation → #5 converter →
#6 repair) orders by *effort-to-impact*. Both are honest; when they conflict,
helps-Muninn wins unless Dennis says otherwise.

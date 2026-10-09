# MIT-Rebuild Candidates — Ranked Survey

**Date:** 2026-10-09
**Status:** RESEARCH ONLY — no code written. For Dennis's red pen.
**Strategy (standing):** (1) Contribute to good FOSS where it exists. (2) Where a tool's license restricts users and a rebuild is feasible, do a clean-room MIT rebuild — user reviews (likes, dislikes, feature wishes) are the requirements spec; the original code never enters the room. (3) Even a feature-identical MIT version counts as helping. (4) MIT for everything; if a dependency's license boxes us in and we can rebuild the piece, we rebuild it.

**Method:** Four parallel research agents surveyed mesh repair, point-cloud/deviation, FreeCAD workbenches, and slicers/converters (Oct 9, 2026). Licenses verified live from repos. Quotes are verbatim from GitHub issues, official forums, and verified reviews, attributed. Reddit was blocked in this environment — no Reddit quotes; agents used GitHub/forums/search snippets instead and said so where thin. Nothing fabricated.

**Source files:** cluster 3 full findings at `~/workspace/research/freecad-re-workbench-survey.md`; cluster 2 full findings at `~/workspace/research/point-cloud-deviation-survey.md`. Clusters 1 and 4 findings are consolidated below (their handoffs only).

**License restrictiveness scale used for ranking:** Noncommercial/proprietary (hard block on commercial use) > AGPL (network-copyleft, SFC allegation live) > GPL (viral on distribution) > LGPL (linking OK, weak case) > permissive (not a candidate — build on it).

---

## TIER 1 — Do these

### 1. MIT cloud-to-mesh deviation engine (the CloudCompare slice)

- **Target:** CloudCompare — **GPL-3.0** (verified live: README states *"all the code you mix or link with CloudCompare's code must be made public as well. This code cannot be used in a closed source software"*).
- **Why it ranks #1:** Directly on the mesh-to-cad roadmap — our `deviation.py` shells out to the CloudCompare CLI today. An MIT engine lets deviation code live *inside* MIT projects. The substrate exists: **Open3D is MIT** (verified), v0.20.0, and the key primitive `open3d.t.geometry.RaycastingScene.compute_signed_distance()` is confirmed in real user code. Chamfer/Hausdorff are thin aggregations over nearest-neighbor distances — days, not research.
- **Review-sourced spec (what users hate / wish for):**
  - Perf collapse at scale — *komyash*, official forum Sep 2024: *"the performance seems to degrade significantly as soon as the point cloud exceeds about 100 million points… Running cloud to cloud distance comparisons with large datasets seems to take ages."*
  - RAM hunger — *PablerasBCN*, forum May 2022: *"I had to upgrade RAM ammount to handle large point clouds… it was allways at the edge and started to crash CC, so Upgraded to 64gb."*
  - LoD slowness — *Эндорфин*, forum Jun 2023: *"not good performance - about 11fps, and not close to what initially is, before LoD computation finishes."*
  - Non-deterministic numerics — GitHub #2247: *"the returned distances sometimes contain NaN values… This seems to be non-deterministic, and only happens 1/5th of the time approximately"* (deterministic numerics belongs in the rebuild spec).
  - Plugin ABI fragility — GitHub #2270: *"ExamplePlugin.dll does not seem to be a valid plugin. The plugin uses an incompatible QT library"* (a clean-room rebuild picks a stable plugin story or none at all).
  - Structural ceiling — admin *daniel*: the octree *"is limited to 10 levels of subdivision, and… doesn't like big density variations"* (rebuild can pick a better spatial index from day one).
- **Honest feasibility:** Focused MIT deviation engine (CLI: cloud+mesh → signed/unsigned C2M → stats + PLY/CSV export) = **weeks, not months** — all primitives exist. Full CloudCompare parity = man-years; do not attempt. The hard part is scale parity (chunked float32 + GPU batching via Open3D's tensor API), not the math. Rebuild the slice users are gated on, not the app.

### 2. MIT calibration-tower generator (the Orca/SuperSlicer extraction)

- **Target:** the built-in calibration suites of OrcaSlicer / SuperSlicer / PrusaSlicer — all **AGPL-3.0** (verified live; Orca and Bambu Studio were both corrected from "GPL" to AGPL during research — AGPL is *more* restrictive for anything networked).
- **Why it ranks #2:** Orca's calibration suite is the single most-cited reason people install it (OctoPrint forum: *"the calibration features in OrcaSlicer are a big draw"*), and it's trapped inside AGPL C++. Scope is small: generate geometry + parameterized G-code for temp / retraction / flow / pressure-advance / max-volumetric-flow towers. Dennis's own standing filament-retune rule (temp tower, retraction test, flow calibration, VFA check) **is already the requirements spec**. Tailwind: the May 2026 Software Freedom Conservancy AGPL-violation allegation against Bambu Lab — the dominant vendor is accused of violating the very license its slicer ships under.
- **Review-sourced spec:**
  - Orca #11148 ("Interface Enshittification"): *"The number of clicks needed to get to frequently accessed settings has doubled or tripled"* — a standalone tool has no settings maze by construction.
  - Orca #11711: silent wrong-temperature slicing (*"The Orca UI displays it as 275°, using the first value. But the actual slicing engine uses the second value and that never changes"*) — spec item: the generator must echo back the exact parameters it baked into the G-code.
  - Duet3D forum, *ctilley79*: the line-based PA test *"will not work on a large bed with bed center 0/0 origin coordinates"* — spec item: origin-agnostic test patterns.
  - Duet3D forum, *oliof* on the Bambu networking blob: *"I am very wary about this poisoning of an open source project with binary blobs"* — spec item: zero network, zero blobs, runs offline.
  - Andrew Ellis pressure-advance generator is GPL-3.0 — the calibration ecosystem's building blocks are GPL/AGPL-locked, confirming the extraction case.
- **Honest feasibility:** **Very high — weeks.** Geometry generation + G-code templating is well-understood; no novel algorithms. This is the single best effort-to-impact ratio in the whole survey.

### 3. MIT STL→prismatic-script converter (the stlToSolid spirit)

- **Target:** Crypto69/stlToSolid — **PolyForm Noncommercial 1.0.0** (verified: repo LICENSE is the full PolyForm text, *"Copyright (c) 2026 Chris Venter"*). Noncommercial = commercial use forbidden. **This is not FOSS** — the most restrictive license in the survey.
- **Why it ranks #3:** Closest philosophical competitor to mesh-to-cad: STL/OBJ/PLY/OFF/3MF/GLB → prismatic STEP solids with real planes/cylinders/cones/holes, *plus an editable CadQuery script of the recognized sketches/extrudes* — replicating Fusion 360's paid Prismatic conversion. It's a 2-month-old solo project: **5 stars, 0 forks, 0 releases** — no moat, no community to outrun. Its README is effectively a published feature spec (face-group engine, sliced-loft mode, X-Ray section viewer, Blueprint drawing→script). An MIT clean-room unlocks commercial use and is mesh-to-cad's natural "prismatic feature recognition + editable script" layer.
- **Review-sourced spec:** No user base yet — no reviews. The author's own README states the problem: on Fusion 360's free hobby tier, *"Mesh → Solid turns the mesh into a solid made of hundreds or thousands of facet triangles, which is impossible to measure, sketch on, or model against."* That's the spec, straight from the source. Cross-reference the FreeCAD complaints below (#5) for what the output must avoid (face-per-triangle soup).
- **Honest feasibility:** **Medium.** Face-grouping + primitive fitting (RANSAC on CGAL-style algorithms — well-published) is real work but not research; the numpy-only core precedent shows the scope is bounded. Direct strategic overlap with existing mesh-to-cad infra (QC gates, CadQuery output). Note: our mesh-to-cad already does STL→STEP — this is the *recognition + editable script* layer on top, not a duplicate.

---

## TIER 2 — Strong, bigger

### 4. MIT mesh-repair core ("make this STL printable" engine)

- **Targets:** MeshLab (+PyMeshLab) — **GPL-3.0** (verified live); Netfabb — **proprietary commercial** (~$4,415/yr for Fusion 360 with Netfabb Premium; standalone killed, rolled into Fusion).
- **Why it ranks here:** Netfabb is the only tool users consistently rate as *actually fixing* meshes (reprap.org: *"It's not quite as robust as Netfabb for repair"*). MeshLab is the FOSS standard and its complaint list is a ready-made spec. The dead Netfabb free cloud-repair service left a hole nobody filled.
- **Review-sourced spec:**
  - MeshLab crashes — sourceforge *ibi006*: *"This application bombs many many times, but I still like it"*
  - Docs/install hell — sourceforge: *"I was warned against using meshlab due to 'extremely poor documentation'… I wasted 2 hours installing meshlab due to rubbish documentation, so will be returning to netfabb"*
  - Learning curve — cnczone: *"I find the GUI and interaction with Meshlab to be difficult to learn… I have already done more 'constructive' work in Netfabb in 1 day than I have in Meshlab in 2 years"*
  - No undo — sourceforge *antona furies*: *"fact that this software has no 'undo' function is horrible"*
  - Netfabb repair regression — Prusa3D forum *imhavoc*: *"I just tested it against a model with 4 errors. When I loaded the repaired OBJ, it showed as having 5 errors"*
  - Netfabb bloat — SketchUp forum *jim_foltz*: *"Geez – it's a 1.2 GB .exe. The old off-line installer was 7 MB. I think I'll pass"*
  - Netfabb cloud flakiness — PrusaSlicer #10711 *sarusani*: the free repair service *"looks like it's hanging"* while local repair *"takes less than a second"*
  - Gold-standard UX to steal: Materialise Magics' Fix Wizard — *"All the most common problems can be solved in just one click. The Fix Wizard will guide you step-by-step"* (Magics itself: proprietary, ~$2,855–$10,000/yr — not a rebuild target, but its wizard is the spec).
- **Honest feasibility:** **Medium, multi-month.** Full MeshLab (10,937 commits, 20 years, 100+ VCGLib filters) = not feasible. The repair-core subset is: STL/OBJ/PLY I/O, watertight repair (weld duplicates, fix normals, ear-clipping hole fill, drop non-manifold), Laplacian/Taubin smoothing, quadric edge-collapse decimation (Garland & Heckbert 1997 — extremely well documented), wall-thickness/overhang checks, fix report. Exclude: robust booleans (exact arithmetic), screened Poisson (real work), texture stack, interactive GUI. Headless CLI + Python API directly answers the top complaints (batch mode makes "undo" irrelevant; scriptable beats GUI-learning-curve).

### 5. MeshToFeatures-pattern pipeline as MIT standalone

- **Target:** MeshToFeatures (MasoudMiM) — **LGPL-2.1-or-later** (verified from README); alive, v0.17.6 tagged ~11 days ago; **not yet in the FreeCAD Addon Manager** (pending review).
- **Why it ranks here:** Its geometry core is deliberately FreeCAD-free (numpy/scipy/trimesh/shapely, 450+ headless tests) — a portable-architecture precedent that lowers rebuild risk. Textbook algorithms. And 16 years of complaints about what it replaces: FreeCAD's own *wmayer* admitted in 2010 that "Create shape from mesh" is *"quite stupid because it creates one face for each triangle"* — still true; issue #20455's sew-tolerance UX trap still haunts users.
- **Review-sourced spec:**
  - Face-per-triangle soup (wmayer's admission, still true) — spec: analytic face recovery, never triangle-faces.
  - #20455 tolerance confusion — spec: one tolerance parameter, plainly labeled, no overloads.
  - MeshToFeatures' own Issue #7 (author's): float32 round-trip producing invalid compounds 3% under mesh volume — spec: validate output volume against input, refuse to emit garbage.
  - Detessellate's install-breaking `package.xml` (#22) and Addon-Manager ghost-install (#19) — spec: one-command install, verified in CI.
- **Honest feasibility:** **Medium.** Best-candidate pattern in the FreeCAD cluster per the survey agent. LGPL is the weakest license-motivated case here (linking is already allowed) — the rebuild case rests on the rebuild-over-restriction principle plus the review-driven spec, not on a hard license block.

### 6. MIT print-analysis toolkit (3D-Print-Toolbox spirit)

- **Target:** Blender's 3D-Print Toolbox — GPL via Blender (free-as-in-beer; the license gate is mild, but an MIT version unblocks embedding in MIT pipelines like ours).
- **Why it ranks here:** Trivially feasible; the perfect v0.1 seed for #4. Volume/area stats, wall thickness, overhang detection, manifold check — analysis only, no repair.
- **Review-sourced spec:** Blender users' voxel-remesh wish (GitHub discussion #1218 *myselfhimself*: *"I wish I had some external tool for that"*) and the export-what-you-see texture complaint both point at analysis gaps a small tool can fill first.
- **Honest feasibility:** **Very high — days to weeks.** A natural first burn-sized project that grows into the repair core.

---

## TIER 3 — Worthwhile, narrower or harder

### 7. Meshmixer-spirit repair + remesh + hollow tool

- **Target:** Meshmixer — **proprietary freeware, frozen** (last release 3.5, 2018; Autodesk: no updates, functionality to be folded into Fusion 360). Not license-restricted (it's free) but dying — rebuild rationale is abandonment.
- **Review-sourced spec:** TrustRadius verified review — remeshing *"takes up to a day of waiting time"* (spec: fast remeshing); *"The sculpting tools need the addition of a proper brush for creating sharp creases"*; *"The standard shape library is rather limited. It would be nice to have this connected to online repositories"*; the summary complaint is simply that it will never improve.
- **Feasibility:** Medium. The import→auto-repair→hollow/supports→export loop is coherent and bounded; replicating the auto-repair's *behavior* (99.5% of cases fixed per the review) is the engineering challenge, not any single hard algorithm.

### 8. Defeature-pattern utility on build123d/OCP

- **Target:** Defeaturing (easyw) — **license UNVERIFIED, no LICENSE file in repo**; treat as all-rights-reserved; effectively dormant.
- **Feasibility:** High — small, burn-sized; clean-room from OCC docs. Demand: low-medium (niche CAD cleanup).

### 9. MeshInspector / MeshLib-pattern inspection SDK

- **Target:** MeshInspector/MeshLib — **dual-licensed: free for non-commercial only, paid commercial**; NOT OSI open-source. Active 2026. GitHub issue *"Misleading use of 'Open Source' wording"* (Mar 2026) shows community friction; issue *"Severe geometry loss when repairing Self-Intersections"* (Jan 2026) shows repair-quality pain.
- **Feasibility:** Medium — an inspection/repair SDK is smaller than MeshLab. The commercial gate qualifies it; demand is low-medium (developer audience).

### 10. Curves-pattern NURBS toolkit as MIT math functions

- **Target:** Curves workbench (tomate44) — **LGPL-2.1+**, alive; culture flag: *"Code contribution is NOT encouraged."*
- **Feasibility:** Medium — scope as MIT math functions, not a workbench. Demand: low-medium (niche surfacing audience).

### 11. LAStools paid-tool equivalents

- **Target:** LAStools — **mixed: LASlib/LASzip open, many tools commercial/watermarked**.
- **Feasibility:** High — small tools. But PDAL (BSD) already covers most of the same ground, so demand is low. Only worth it if a specific paid tool has loud users.

---

## TIER 4 — Don't / not now

- **Full slicer rebuild (PrusaSlicer, OrcaSlicer, Bambu Studio, Cura, SuperSlicer):** massive, multi-year — ~15 years and tens of thousands of commits in the Slic3r family tree. Prusa itself needed a from-scratch rewrite (3.0 alpha) to escape its own architecture. The complaints are about features and governance, not missing slicers. Extract subsets (#2), don't rebuild.
- **Full MeshLab / full CloudCompare:** 20 years / man-years respectively. Rebuild the slices (#1, #4), not the apps.
- **Commercial scan-to-CAD tier (Geomagic Design X $19,950, Wrap $9,996+, QuickSurface ~$4,300–$5,880, PolyWorks quote-only):** Parasolid-class surfacing is the moat; scan-vs-CAD inspection has zero FOSS equivalent and is the biggest gap — but it's the hardest rebuild. Not now.
- **Bambu LAN-control client:** enormous demand (every complaint is "I can't talk to my own printer"), but legally hot — a Polish dev got a cease-and-desist and took his fork down. Only with explicit legal comfort; not a casual burn project.
- **OctoPrint core subset:** AGPL-3.0, but the plugin ecosystem is the moat and AGPL already permits most uses — weaker license-motivated case. Medium-large effort.
- **Resin slicer (ChiTuBox/Lychee Pro alternative):** genuinely smaller than FDM slicing and freemium incumbents gate features — medium effort, tractable — but outside the current FDM hardware focus.
- **Meshroom:** MPL-2.0 — weak license case; the pain is CUDA lock-in, not licensing.
- **Already permissive — build on, don't rebuild:** COLMAP (BSD-3), PDAL (BSD-3), PCL (BSD), Potree (BSD-2), Open3D (MIT), trimesh/manifold3d (MIT), build123d/CadQuery (Apache-2.0), stl2step (MIT), Instant Meshes (BSD-3).
- **Skip per cluster analysis:** CAD Sketcher (Blender-bound, solver is the moat, platform mandates GPL), Detessellate and MeshRemodel (FreeCAD-workflow glue — contribute there instead per the contribute-first rule), Simplify3D (dead market — free slicers already won).

---

## Suggested build order (my recommendation)

1. **#6 print-analysis toolkit** — days/weeks, seeds the repair work, immediate pipeline value.
2. **#2 calibration-tower generator** — weeks, universal demand, Dennis's retune rule is the spec.
3. **#1 MIT deviation engine** — weeks, unblocks the mesh-to-cad roadmap directly.
4. **#3 stlToSolid-spirit converter** — medium effort, highest strategic fit with mesh-to-cad.
5. **#4 mesh-repair core** — multi-month, the big one; #6 was its v0.1.

Each is independently shippable, each is MIT, and none requires touching anyone else's code — the specs come from user reviews, exactly per the strategy.

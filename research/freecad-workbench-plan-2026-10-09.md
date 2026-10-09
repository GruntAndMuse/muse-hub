# FreeCAD Workbench for mesh-to-cad — Research & Build Plan

**Status:** PLAN ONLY — no code written. For Dennis's red pen before anything gets built.
**Date:** 2026-10-09
**Goal:** A FreeCAD workbench that lets a user bring a mesh in (scan, download, or AI-generated) and run the mesh-to-cad pipeline from inside FreeCAD, ending with editable parametric geometry.

---

## 1. How FreeCAD workbenches work

**Mechanics (verified against FreeCAD wiki + addon-academy docs, Oct 2026):**

- A workbench is a folder dropped into FreeCAD's `Mod/` directory (`~/.local/share/FreeCAD/Mod/` on Linux, `%APPDATA%\FreeCAD\Mod\` on Windows, `~/Library/Application Support/FreeCAD/Mod/` on macOS).
- Two entry points: `Init.py` (runs at startup, even in console mode — importers/exporters live here) and `InitGui.py` (runs only in GUI mode — defines the workbench class).
- The workbench class defines `Initialize()` (register commands, build toolbars/menus via `appendToolbar`/`appendMenu`), `Activated()` (runs when the user switches to it), `Deactivated()`.
- Commands are Python classes with `GetResources()` (name, icon, tooltip), `Activated()` (what happens on click), and `IsActive()` (when the button is enabled). Registered via `FreeCADGui.addCommand('Name', cmd_instance)`.
- Interactive tools use **task panels**: a Qt widget shown via `FreeCADGui.Control.showDialog(panel)`. The panel collects input (tolerances, track override, file picks), runs the work, writes results back. This is the standard pattern (FEM workbench uses it for solver control).
- Mesh import from Python: `import Mesh; Mesh.read(path)` / `Mesh.insert(path)` creates mesh objects in the active document. Workbenches can also register custom importers via `FreeCAD.addImportType()`.
- **Critical threading rule:** FreeCAD document objects may only be touched from the main GUI thread. Long computations (trimesh analysis on a 500k-face scan takes minutes) must run in a worker thread or subprocess, then marshal results back to the main thread via Qt signals before touching the document. Get this wrong and FreeCAD crashes or hard-freezes.
- Modern alternative layout (addon-academy): `freecad/<AddonName>/` namespace package with `init_gui.py`. Both layouts work with the Addon Manager; the classic `Init.py`/`InitGui.py` layout is simpler and matches what MeshToFeatures/Detessellate use.

**Distribution via Addon Manager (verified):**

- A `package.xml` manifest at the repo root describes the addon (name, version, maintainer, license, `<workbench>` content block with the classname matching `InitGui.py`).
- Submission to the `FreeCAD/Addons` catalog (submission docs in that repo) → review → listed in the Addon Manager. The manager handles install, update checks, and removal. Detessellate went through exactly this path and is listed today.
- Release flow per existing practice: bump version in `package.xml`, commit, tag, GitHub release → Addon Manager picks it up.

**Python environment (verified, this is a real constraint):**

- Official FreeCAD Windows builds (LibPack 3.1.x, FreeCAD 1.1 dev line) bundle Python 3.12 **with numpy 1.26.4 and scipy 1.14.1 preinstalled**. So two of our three Python deps are already inside FreeCAD on Windows.
- **trimesh is NOT bundled.** Standard practice (used by several workbenches): on first run, check `import trimesh`; if missing, offer a guided pip install into FreeCAD's `AdditionalPythonPackages` dir using `freecad.utils.get_python_exe()`. Must pin versions — the forum is full of numpy-2.x breakage from unpinned installs (numpy 2.x vs scipy/matplotlib conflicts).
- Linux (conda/flatpak/snap) and macOS builds vary. The workbench must detect what's importable and degrade with a clear message, never a traceback.

---

## 2. Integration map: pipeline stages → workbench commands

The pipeline's scripts are **importable Python modules with function-level APIs** (not just CLIs). This is the integration seam — the workbench imports them in-process:

| Pipeline stage | Pipeline API | Workbench command | Seam quality |
|---|---|---|---|
| 0 Intake (units) | `check_units.suggest_units(path)` → dict | **"Import mesh for reverse engineering"** — file picker → copies original into project `input/` (never modifies original, per SOP) → runs units check → shows suggestion + confidence in a task panel → **user confirms** (the pipeline refuses to guess here; the workbench must too) | Easy. Pure function, fast, no FreeCAD objects involved. |
| 1 Cleanup gate | `quality_gate.quality_gate(path)` → dict with `verdict` | **"Quality gate"** — runs the gate, shows the four metrics + verdict in the task panel. `needs-rescan` → honest stop with the rescan guidance. For AI meshes the copy reads "regenerate or clean up" instead of "rescan". | Easy. Same pattern as intake. |
| 2 Analysis | `analyze_mod.analyze(path)` → (measurements dict, aligned mesh path) | **"Analyze mesh"** — runs analysis in a worker thread (can take minutes on dense meshes) with a progress/cancel UI → shows bbox, planar/cylindrical fractions, symmetry, hole status, and the **track decision + confidence** in the task panel → user confirms or overrides the track. Writes `analysis/<name>_measurements.json`. The aligned STL can be shown in the 3D view for visual sanity-check. | Medium. Needs the threading pattern; the function itself is importable. |
| 3A Prismatic | MeshToFeatures / Detessellate / manual | **"Rebuild (prismatic)"** — the workbench does NOT reimplement this. It detects whether MeshToFeatures is installed: if yes, deep-links the user into it with the measurements panel open beside it; if no, offers one-click install via Addon Manager. Fallback path: "measure-and-remodel" mode that docks the measurements JSON as a reference panel while the user builds in PartDesign. | Medium-hard. This is orchestration + UX, not algorithms. Depends on third-party workbenches the user may not have. |
| 3B Organic | `deviation` module (CloudCompare CLI wrapper) | **"Deviation check"** — the measurement half of the deviation loop. User models in FreeCAD (Curves workbench / section loft), selects their solid, workbench tessellates it, runs cloud-to-mesh against the input mesh, reports max/mean/p95 + pass/fail vs the project tolerance. The *surface design* stays manual (honest limit, same as the pipeline). | Hard — entirely because of the CloudCompare external dependency (see §5). |
| 4 Verification | deviation + dimension re-check | **"Verify build"** — runs deviation against the *original input mesh* (never the cleaned one — the pipeline's rule), re-checks every dimension from the measurements JSON against the CAD, runs FreeCAD's geometry check. Generates `verification/<name>_report.md`. | Medium. Mostly wiring existing pieces; the dimension re-check needs a small new function (compare measurements JSON vs. CAD — the automation-roadmap already sketches this). |
| 5 Output | FreeCAD export APIs | **"Export project"** — STEP + STL + TechDraw drawing PDF into `output/`, updates `manifest.json`. | Easy. Stock FreeCAD APIs. |

**Project model:** The workbench manages a pipeline project folder (the `input/`, `work/`, `analysis/`, `cad/`, `verification/`, `output/` layout + `manifest.json` from PIPELINE.md) as a sidecar to the FreeCAD document. The FCStd file lives in `cad/`. The manifest is the single source of truth for stage state — the workbench reads it to show which stages are done, so closing and reopening FreeCAD doesn't lose pipeline state. The CLI's `cmd_full` already implements project setup + manifest writing; the workbench reuses those functions rather than reimplementing them.

**What the workbench does NOT do (scope discipline):**
- Does not reimplement MeshToFeatures, Detessellate, or stl2step. It orchestrates and guides; those tools do their jobs.
- Does not do one-click scan-to-CAD. The pipeline's honest limits carry over unchanged.
- Does not invent missing geometry. The `needs-rescan`/`regenerate` stop is a feature, not a bug.

---

## 3. Concrete build plan

### Repo layout (proposed — see open question #4)

```
freecad-meshtocad/                  # or mesh-to-cad/workbench/
├── package.xml                     # Addon Manager manifest
├── Init.py                         # console-mode entry (mesh importer registration)
├── InitGui.py                      # workbench class, commands, toolbars
├── freecad/meshtocad/              # workbench Python package
│   ├── __init__.py
│   ├── workbench.py                # workbench class definition
│   ├── commands/
│   │   ├── cmd_import.py           # Stage 0: import + units task panel
│   │   ├── cmd_quality.py          # Stage 1: quality gate task panel
│   │   ├── cmd_analyze.py          # Stage 2: analysis task panel (worker thread)
│   │   ├── cmd_rebuild.py          # Stage 3A: MeshToFeatures detect/guide/deep-link
│   │   ├── cmd_deviation.py        # Stage 3B/4: deviation check task panel
│   │   ├── cmd_verify.py           # Stage 4: verification report
│   │   └── cmd_export.py           # Stage 5: export outputs
│   ├── engine/                     # pipeline scripts, copied from mesh-to-cad/scripts/
│   │   │                           # (single-sourced: build script syncs them at release)
│   │   ├── check_units.py
│   │   ├── quality_gate.py
│   │   ├── analyze.py
│   │   └── deviation.py
│   ├── ui/
│   │   └── task panels (Qt .ui files or code-built; code-built is simpler to maintain)
│   ├── deps.py                     # first-run dependency check: trimesh, CloudCompare detect
│   └── manifest.py                 # project folder + manifest.json read/write (reuse CLI code)
├── Resources/
│   └── icons/                      # workbench icon + command icons (SVG)
├── tests/
│   ├── test_engine.py              # headless: engine functions, no FreeCAD (extends existing pattern)
│   └── test_workbench.py           # freecadcmd headless: import mesh, run stages 0–2, verify outputs
├── .github/workflows/ci.yml        # lint + headless tests (conda-forge FreeCAD, per addon-academy pattern)
├── README.md / CHANGELOG.md / CONTRIBUTING.md
└── LICENSE                         # LGPL-2.1-or-later (matches the chain's most restrictive tool)
```

### UI sketch

**Toolbar "MeshToCAD":** Import → Quality → Analyze → Rebuild → Deviation → Verify → Export. Each button enabled only when its prerequisites are met (`IsActive()` checks the manifest: can't Analyze before Import, can't Verify before a CAD body exists). This enforces the pipeline order in the UI — the same "one command can't be misordered" idea as the CLI, expressed as button states.

**Task panels (one per stage, all follow the same shape):**
1. Header: stage name + what it does in one plain sentence.
2. Inputs: file path (pre-filled), tolerance (default 0.3mm, mating 0.1mm — editable), track override dropdown (Analyze stage only).
3. Run button → progress bar + Cancel (worker thread; GUI stays responsive).
4. Results: the numbers, in the same wording as the CLI (units suggestion + confidence; the four quality metrics + verdict; bbox + track decision + confidence). No new vocabulary — the docs and the workbench say the same things.
5. Next-step button ("Continue → Analyze") that closes the panel and opens the next stage's panel.

**AI-mesh intake variant:** when the user picks source type "AI-generated," the intake panel adds two honest lines: the mesh is unitless (units check becomes "tell me how big this should be" rather than a guess), and the quality gate's verdict vocabulary shifts (no "rescan" — "regenerate or clean up"). A persistent note in the Analyze panel: *"AI meshes carry no real dimensions. This pipeline gives you editable geometry; YOU set the dimensions to spec afterward."*

### Dependencies

| Dep | How the workbench gets it |
|---|---|
| numpy, scipy | Bundled in official FreeCAD builds; detect, don't install. |
| trimesh | First-run check → guided pip install into `AdditionalPythonPackages`, pinned version (see requirements-locked.txt in the pipeline). |
| CloudCompare | External binary. Detect on PATH / common install locations. If missing: deviation commands show "CloudCompare not found" with install links per OS, and the rest of the workbench keeps working. Soft dependency, loud about it. |
| MeshToFeatures / Detessellate | Optional. Detect → deep-link; not installed → one-click Addon Manager install offer. Never required. |

### Test plan

1. **Engine unit tests (headless, no FreeCAD):** the pipeline scripts are already structured for this (function-level APIs). Extend the existing pattern: intake/units suggestions on known meshes, quality-gate verdicts on the test-samples (clean/noisy), analyze track decisions on bracket (prismatic) vs blob (organic). Run with pytest in CI.
2. **Workbench integration tests (headless FreeCAD via `freecadcmd`):** init the workbench, import a test STL, run stages 0–2 programmatically, assert the project folder + manifest + measurements JSON exist and the track decision matches the known answer. CI pattern exists (addon-academy runs headless FreeCAD 1.0 via conda-forge).
3. **GUI manual checklist:** task panels open/close, buttons enable/disable per manifest state, long analysis doesn't freeze the GUI (cancel works), missing trimesh triggers the guided install, missing CloudCompare degrades loudly. A written checklist in Dennis's style, run before each release.
4. **Version matrix:** test against FreeCAD 1.0.x and 1.1.x (see open question #1); at minimum the version Dennis runs.

---

## 4. Open questions for Dennis

1. **FreeCAD version target:** 1.0.x (stable, biggest user base) or 1.1 dev (newer APIs, moving target)? Recommendation: develop against 1.0.x, smoke-test on 1.1.
2. **Scope — full workbench vs. MVP:** full pipeline (stages 0–5 as sketched) or MVP first (intake + analyze + deviation check — the stages with no good existing UI; rebuild/verify come later)? Recommendation: MVP. It ships sooner and the later stages lean on third-party workbenches anyway.
3. **MeshToFeatures/Detessellate relationship:** detect + deep-link (recommended), or keep the workbench fully independent? Depending on them makes Track A much stronger but adds install friction.
4. **Repo layout:** separate `GruntAndMuse/freecad-meshtocad` repo, or a `workbench/` folder inside the existing mesh-to-cad repo? Recommendation: separate repo — different release cadence, different audience (FreeCAD users vs. CLI users), cleaner Addon Manager story. The engine scripts get single-sourced via a sync script at release time.
5. **License:** LGPL-2.1-or-later to match the chain's most restrictive tool (MeshToFeatures)? That's the pipeline doc's own recommendation.
6. **AI-mesh intake:** add "AI-generated" as a first-class source type in the manifest (with the unitless handling), or treat AI meshes as plain downloads? Recommendation: first-class — the unitless problem is real and deserves its own UX.
7. **CloudCompare:** soft dependency with loud degradation (recommended), or invest in a pure-Python C2M fallback (slow, but zero external installs)? Note: a pure-Python fallback would be dramatically slower on dense meshes — honest tradeoff.

---

## 5. Honest assessment of the hard parts

1. **AI meshes have no ground truth — the pipeline's philosophy bends here.** Everything in mesh-to-cad is built around "deviation against the mesh" as objective truth. For an AI-generated mesh, the mesh itself is an approximation. The workbench can still do something real (units handling, quality gating, editable geometry out), but the verification stage means something weaker: "your CAD matches the AI mesh," not "your CAD matches reality." The workbench must say this plainly in the UI, or it becomes the exact kind of overclaiming Dennis won't ship.

2. **FreeCAD's Python environment across distributions.** numpy/scipy are bundled on official Windows builds, but conda/flatpak/snap/AppImage builds differ, and unpinned pip installs break things (documented numpy-2.x breakage). The dependency story needs testing on at least Windows-official and one Linux build, or users will hit import errors on day one.

3. **Threading long operations.** Analysis on a dense scan takes minutes. FreeCAD crashes if a worker thread touches the document. The QThread + signals pattern is well understood but fiddly, and every new long op is a new chance to get it wrong. This is the #1 crash-risk area in the build.

4. **CloudCompare as an external binary.** `deviation.py` shells out to it; only verified against 2.11.3, and the CLI output parsing is version-sensitive by the author's own admission. Every user must install CloudCompare separately, on every OS. This is the biggest UX friction point in the whole plan.

5. **Track A (prismatic rebuild) is the automation gap.** MeshToFeatures handles clean CAD-derived meshes; scans and AI meshes need manual measure-and-remodel. The workbench cannot automate what the pipeline itself can't — its honest value on Track A is the guided workflow with the measurements docked beside the modeling, not a magic button. Scope the MVP accordingly.

6. **Addon Manager review.** Getting listed requires meeting FreeCAD's packaging bar (package.xml, icons, docs, no malicious patterns). It's a real gate with human reviewers — plan for a review round, not a rubber stamp.

7. **What this doesn't do.** It doesn't make AI meshes engineering-grade by itself (Dennis already called this: clean garbage is still garbage). The workbench's job is to get the user to editable geometry faster and with measurements attached — the engineering judgment stays human. That's the correct, shippable scope.

---

*Plan drafted 2026-10-09 by subagent research. No code written. Awaiting Dennis's red pen, especially on the open questions in §4.*

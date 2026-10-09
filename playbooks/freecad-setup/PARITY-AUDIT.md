# FreeCAD Migration — Phase 2: Feature-Parity Audit

**Date:** 2026-10-09 · **FreeCAD 1.1.4 headless** (`freecadcmd`, console mode only — no GUI)
**Question:** what, if anything, is LOST by moving solid modeling + technical drawings off matplotlib/hand-rolled Python and onto headless FreeCAD?
**Method:** actually ran everything below. Fights are documented in §6, not hidden.

## Verdicts

| Area | Verdict |
|---|---|
| 1. TechDraw headless (dimensioned multi-view drawing) | **WIN, with one contained GAP** — views project beautifully; scripted dimension *graphics* don't render headless (workaround works, documented) |
| 2. Parametric remodel of a real part | **WIN** — no contest on clarity, editability, or correctness |
| 3. Red-pen loop (Dennis marks up PNG/PDF) | **PARITY** — zero new friction |
| 4. Workbench-ification flags | ruled per the standing rule, §4 |

**Bottom line: nothing is lost. The migration is scoped right — FreeCAD takes solid modeling + technical drawings; matplotlib keeps illustration; trimesh keeps mesh surgery.** Details below.

---

## 1. TechDraw headless

**What was built:** `audit/audit_draw.py` (freecadcmd) → 3 kernel-projected views (Front/Top/Iso) as SVG + placement manifest → `audit/compose_page.py` (plain python) → A4 page SVG with ISO title block, positioned views, view labels, 7 dimensions + 2 leader notes → `audit/render_page.py` (bundled PySide6, Qt offscreen) → PNG + PDF.

**Evidence:** [audit_drawing.png](sandbox://workspace/freecad/audit/audit_out/audit_drawing.png) · [audit_drawing.pdf](sandbox://workspace/freecad/audit/audit_out/audit_drawing.pdf) · [audit_drawing.svg](sandbox://workspace/freecad/audit/audit_out/audit_drawing.svg)

**What works (wins):**
- `DrawViewPart` projects correctly headless for Front `(0,-1,0)`, Top `(0,0,1)`, Iso `(1,1,1)`. Verified mappings: Front 2D = (x,z), Top 2D = (x,y), both centered on the part bbox, units = mm, unscaled.
- Holes project as true `<circle>` elements; fillet arcs project as smooth paths; hidden-line handling is correct out of the box.
- `DrawSVGTemplate` + shipped ISO templates work; title-block editable fields (`FC-Title`, `FC-SC`, `FC-Date`, `Drawing_number`, `Designed_by_Name`, …) fill via regex on the SVG — no GUI needed.
- The projection is kernel-accurate: dimensions drawn against it are *true*, unlike matplotlib where I was projecting a mental model (the source of the V1–V12 drawing corrections).

**The gap (contained): scripted dimension graphics don't render headless.**
- `TechDraw.makeDistanceDim3d(view, type, p1, p2)` **segfaults** (hard C++ crash, no Python exception) if called before the view is recomputed. Workaround: `doc.recompute()` first.
- Even then it **returns `None`** — the `DrawViewDimension` is created as a side effect (named `Dimension`). Workaround: `doc.getObject("Dimension")`.
- The dimension object exists with correct references, but its graphics **do not render headless**: `viewPartAsSvg(dim)` returns empty, and no `<text>` appears in the view SVG. There is also **no page-level SVG/PDF export in console mode at all**.
- **Workaround that works:** compose the page SVG manually (template + `viewPartAsSvg` per view + own dimension lines/text projected through each view's known transform), render with Qt offscreen (`QSvgRenderer` → PNG, `QPdfWriter` → PDF). Fully scripted, reproducible, and — honestly — *better* for scripted sheets than TechDraw's dimension objects, because placement is fully programmatic (no GUI picking).

**Minor gotchas:** page needs `Template` set before views compute (`"Template not set for Page"` exception otherwise); Qt's SVG renderer misreads `font-size="3.5mm"` (~4× too big) — use unitless numbers; view stroke widths scale with view scale (0.7 → ~1.05 mm at 1.5×, acceptable).

---

## 2. Parametric remodel

**What was built:** `audit/audit_part.py` — a V2-style bracket (60×40×8 plate, 2× M5 flat-head countersunk holes with his *measured* hardware numbers — 9.8 dia head, 3.6+0.25 recess, 90° cone, 5.5 clearance — 30×20×0.4 inlay pocket, 1.5 mm fillets on vertical edges per the FDM rule). All parameters in one block at the top.

**Evidence:** [audit_bracket.FCStd](sandbox://workspace/freecad/audit/audit_out/audit_bracket.FCStd) · [audit_bracket.step](sandbox://workspace/freecad/audit/audit_out/audit_bracket.step) · [audit_bracket.stl](sandbox://workspace/freecad/audit/audit_out/audit_bracket.stl)

**Verification (all in-script, all passing):** bbox 60.000/40.000/8.000, 2 clearance cylinders at Ø5.5, 2 countersink cones at Ø9.8, solid valid. STL cross-check via trimesh: watertight, volume 18441.90 vs solid 18441.75 (tessellation delta), bounds exact.

**vs the old approach:** the hand-rolled equivalent (`k2-cfs-riser/v2_inlay_coupons.py`) is ~400 lines of ear-clipping, shapely wrangling, and raw binary STL writing — for *flat* parts. The FreeCAD script is ~90 lines including verification, produces a real solid with real fillets (one `makeFillet` call vs faked geometry), and also emits STEP (the old path had no STEP at all). Editability: change a number at the top, rerun — new solid, new STL, new drawing from one source of truth. **This is the single biggest win of the migration.**

**Dennis-side bonus:** the FCStd opens in his FreeCAD — he can orbit, measure, and tweak the actual model, not just red-pen a PNG.

---

## 3. Red-pen loop survival — PARITY

- PNG: 3508×2480 (~300 dpi A4) — better resolution than the old matplotlib sheets, marks up fine on his phone.
- PDF: true-mm vector via `QPdfWriter` — prints to scale.
- Same loop as today: sheet lands in chat, he red-pens, I revise the script. Zero new friction, zero new tools for him to learn.

---

## 4. Workbench-ification flags (standing rule: fingertip workflow → workbench; general library → stays a library)

| Workflow | Verdict | Rationale |
|---|---|---|
| matplotlib diagrams/charts | **stays standalone** | illustration, not CAD; nobody needs a charting workbench |
| trimesh / numpy mesh surgery | **stays a library** | general-purpose; already pip-installable everywhere |
| mesh repair/analysis *operations* | **workbench candidate** | exposes trimesh-style ops at a FreeCAD user's fingertips; matches the rebuild survey's Tier-2 mesh-repair candidate |
| parametric part scripts (`audit_part.py` pattern) | **already FreeCAD** | the same Part-API script runs in his GUI Python console unmodified — macro-ready today |
| scripted drawing composer (`compose_page.py` + dim workaround) | **workbench candidate** | fills TechDraw's real headless gap: "scripted dimensioned sheet" as a command |

---

## 5. Recommendation

**Proceed to Phase 3** (shakedown: remodel one real V2 riser part end-to-end and run the full red-pen loop on its sheet). No blocking gaps found; every gap has a working, documented workaround. The migration loses nothing and gains: a real kernel, real fillets, STEP export, single-source-of-truth parts, and sheets whose dimensions are projected from the solid instead of drawn from a mental model.

Suggested Phase-3 part: a V2 frame crossbar segment (flat-head holes + inlay pocket + the features Dennis already red-penned once — good regression test).

## 6. Fight log (for the next Muse)

1. `for name, got, want in checks` — my own 4-tuple bug in the check list. Read your own code.
2. `makeDistanceDim3d` before recompute → **segfault**, stack trace through `CosmeticExtension::add1CVToGV`. Always `doc.recompute()` after adding views, before cosmetic dims.
3. `makeDistanceDim3d` returns `None` but creates `Dimension` as a side effect. Don't trust the return value; fetch via `doc.getObject`.
4. `viewPartAsSvg` on a fresh view returns empty string unless the view is on a page **with Template set** (`"Template not set for Page"`).
5. `freecadcmd -c` one-liners with multiple statements are flaky (silent empty output). Use script files.
6. `font-size="3.5mm"` renders ~4× too big in Qt's SVG renderer. Unitless numbers = user units = correct.
7. View SVG coords are mm, unscaled, centered on part bbox. Page composition: `translate(X, 210-Y) scale(s, -s)`.
8. `fontconfig` error on render (`Cannot load default config file`) is cosmetic — Qt falls back, output is fine.

## Evidence files

- Scripts: `~/workspace/freecad/audit/audit_part.py`, `audit_draw.py`, `compose_page.py`, `render_page.py` (+ `probe_*.py` spikes)
- Outputs: `~/workspace/freecad/audit/audit_out/` — FCStd, STEP, STL, page SVG/PDF/PNG, per-view SVGs, `views_manifest.json`

---
topic: freecad-python-env-quirks
title: FreeCAD bundled Python — dependency and install gotchas (Linux/VM)
status: verified
verified: 2026-10-09
last_checked: 2026-10-09
review_after_days: 180
aliases: bundled python, pip, numpy 2, appimage, freecadcmd
---

## Findings

- FreeCAD's bundled Python ships numpy 1.26.4 + scipy preinstalled (Windows official builds, LibPack 3.1.x). A plain `pip install trimesh` drags in numpy 2.x as a dependency, which shadows the bundled 1.26.4 and breaks scipy. Fix: `pip install --no-deps`, then verify trimesh works against the bundled numpy (5.1.0 does). [verified 2026-10-09]
- trimesh is NOT bundled with FreeCAD. Install into FreeCAD's `AdditionalPythonPackages` dir via a guided first-run pip install, with versions pinned. [verified 2026-10-09]
- The embedded interpreter ignores `PYTHONPATH`, and console mode (`freecadcmd`) does not auto-add `AdditionalPythonPackages` to `sys.path`. Fix: a `.pth` file in user site-packages pointing at `AdditionalPythonPackages` (e.g. `~/.local/lib/python3.11/site-packages/freecad-deps.pth`). Zero per-script bootstrap after that. [verified 2026-10-09]
- AppImages need FUSE to run; this VM has no `/dev/fuse`. Use `--appimage-extract` and run `squashfs-root/usr/bin/freecadcmd` directly. [verified 2026-10-09]
- Never guess a dependency version (e.g. trimesh 4.4.5 does not exist). Take pins from the project's `requirements-locked.txt`. [verified 2026-10-09]

## Sources

- First-hand: `~/workspace/freecad/SETUP.md` (§5–6, troubleshooting table) — install run 2026-10-09, FreeCAD 1.1.4 AppImage, Python 3.11.14
- `~/workspace/goals/mesh-to-cad-foss-pipeline/hidden_files/freecad-workbench-plan-2026-10-09.md` (§1, dependency table) — predicted the numpy-2.x failure mode from forum reports before the install hit it

## Invalidation triggers

- FreeCAD 1.2+ release (bundled numpy/scipy versions may change)
- trimesh major version bump (pin in requirements-locked.txt changes)

## History

- 2026-10-09: Created. Poster child for this cache: the workbench plan *warned* about numpy-2.x breakage at ~09:50, and the install agent hit it anyway at ~10:10 the same day — because a warning buried in a plan doc is not a checkable cache entry. Both derivations are now consolidated here.

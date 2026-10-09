---
tool: freecad-python
title: FreeCAD bundled Python — dependency and environment gotchas (Linux/VM)
status: verified
first_observed: 2026-10-09
last_verified: 2026-10-09
review_after_days: 180
observed_by: freecad-install (FreeCAD 1.1.4 AppImage, Python 3.11.14, this VM)
confidence: high
---

# freecad-python

## Summary
FreeCAD's bundled Python is its own world: pinned numpy/scipy, no trimesh,
ignores PYTHONPATH, and the AppImage needs FUSE this VM doesn't have. Every
one of these was hit first-hand during the 2026-10-09 install.

## Quirks
- 2026-10-09: A plain `pip install trimesh` drags in numpy 2.x as a
  dependency, which shadows the bundled numpy 1.26.4 and breaks scipy. Fix:
  `pip install --no-deps`, then verify trimesh works against the bundled
  numpy (5.1.0 does). (~/workspace/freecad/SETUP.md §5–6)
- 2026-10-09: trimesh is NOT bundled with FreeCAD. Install into FreeCAD's
  `AdditionalPythonPackages` dir via a guided first-run pip install, versions
  pinned. (~/workspace/freecad/SETUP.md)
- 2026-10-09: The embedded interpreter ignores `PYTHONPATH`, and console mode
  (`freecadcmd`) does not auto-add `AdditionalPythonPackages` to `sys.path`.
  Fix: a `.pth` file in user site-packages pointing at
  `AdditionalPythonPackages` (e.g.
  `~/.local/lib/python3.11/site-packages/freecad-deps.pth`). Zero per-script
  bootstrap after that. (~/workspace/freecad/SETUP.md)
- 2026-10-09: AppImages need FUSE to run; this VM has no `/dev/fuse`. Fix:
  `--appimage-extract`, run `squashfs-root/usr/bin/freecadcmd` directly.
  (~/workspace/freecad/SETUP.md)
- 2026-10-09: Never guess a dependency version (trimesh 4.4.5 does not
  exist). Take pins from the project's `requirements-locked.txt`.
  (~/workspace/freecad/SETUP.md troubleshooting table)

## Sources
- First-hand: install run 2026-10-09 — `~/workspace/freecad/SETUP.md`,
  `~/workspace/freecad/smoke_test.py` (all green)
- Promoted from research-cache topic `freecad-python-env-quirks` (2026-10-09);
  the workbench plan predicted the numpy-2.x failure from forum reports
  before the install hit it the same day

## Invalidation triggers
- FreeCAD 1.2+ release (bundled numpy/scipy versions may change)
- trimesh major version bump

## History
- 2026-10-09: entry created from the install run + research-cache topic.

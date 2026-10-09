# FreeCAD Headless Setup — Linux VM (reproducible)

**Purpose:** Shared toolchain foundation. Dennis runs FreeCAD on his Windows PC;
this VM runs it headless (`freecadcmd`, console mode only). Both start at the same
version so models and scripts move cleanly between us.

**Installed version:** FreeCAD **1.1.4** (stable), conda-based AppImage, Python 3.11
inside the bundle. Installed 2026-10-09.

**Rule for this doc:** every step below was actually run. Failures and wrong turns
are recorded, not hidden. If a step says "expected output", that output was seen.

---

## 0. Environment (what we're working with)

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS (Noble Numbat), x86_64 |
| Kernel Python | 3.12.3 (`/usr/bin/python3`) |
| sudo | available, no password (`sudo -n true` succeeds) |
| conda / mamba | NOT installed |
| Disk (home) | ~11 GB free on `/home/hatch` |
| RAM / CPU | 7 GB / 2 cores |
| curl, wget | present |

`/tmp` is a 512 MB tmpfs — too small for the download. All work happens under
`~/workspace/freecad/` (persists; `/tmp` can be wiped mid-session).

## 1. Choosing the install path

Candidates considered:

| Path | Version available | Verdict |
|---|---|---|
| `apt install freecad` (Ubuntu universe) | `apt-cache policy freecad` returned **nothing** — package metadata not present in this image's apt lists | Rejected: unknown/stale version, would need `apt update` + likely yields pre-1.0 anyway |
| conda-forge (`mamba install -c conda-forge freecad`) | 1.1.x available | Viable fallback, but requires installing Miniforge first (~1–2 GB with Qt deps) and conda solves are slow on 2 cores |
| Official AppImage (GitHub releases) | **1.1.4** (latest stable, 2026-09-28) | **Chosen.** Single version-pinned file, published SHA256, no dependency hell, no sudo needed, trivially reproducible: download → verify → extract → run |

**Version decision (recorded 2026-10-09):** the stable line is now **1.1.x**, not 1.0.x
(`1.1.0` released 2026-03-25, `1.1.4` on 2026-09-28; `1.0.2` was the last of the
1.0 line, 2025-08-06). A fresh install from freecad.org today yields 1.1.x, so
1.1.4 is the correct parity target — not 1.0.x.

**Asset chosen:** `FreeCAD_1.1.4-Linux-x86_64-py311.AppImage` (782 MB),
plus its `-SHA256.txt` sidecar, both from
`https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/`.

## 2. Download and verify

```bash
mkdir -p ~/workspace/freecad/dl
cd ~/workspace/freecad/dl
curl -sL -o FreeCAD_1.1.4-Linux-x86_64-py311.AppImage-SHA256.txt \
  "https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage-SHA256.txt"
curl -L -o FreeCAD_1.1.4-Linux-x86_64-py311.AppImage \
  "https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage"
sha256sum -c FreeCAD_1.1.4-Linux-x86_64-py311.AppImage-SHA256.txt
```

Expected: `sha256sum -c` prints
`FreeCAD_1.1.4-Linux-x86_64-py311.AppImage: OK`.

Published hash (from the `-SHA256.txt` sidecar, 2026-10-09):
`f6dc6ba676e5ac96a565ebc8d657232f94c6158e85b4352141bd1a46f6b43434`

## 3. Extract (do NOT try to run the AppImage directly)

This VM has **no `/dev/fuse`**, and AppImages need FUSE to mount-and-run.
Running `./FreeCAD....AppImage` directly fails here. The fix is one-time
extraction with the runtime's built-in `--appimage-extract` (works without FUSE):

```bash
cd ~/workspace/freecad/dl
chmod +x FreeCAD_1.1.4-Linux-x86_64-py311.AppImage
mkdir -p ~/workspace/freecad/app
cd ~/workspace/freecad/app
../dl/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage --appimage-extract
```

Expected: exit 0, creates `squashfs-root/` (~2.6 GB). The console binary is then:

```
~/workspace/freecad/app/squashfs-root/usr/bin/freecadcmd
```

(`squashfs-root/usr/bin/` also contains `freecad` (GUI — unusable here, no
display) and `python` (the bundled Python 3.11 — used below for pip).)

A convenience wrapper lives at `~/workspace/freecad/freecadcmd` — same thing,
shorter to type.

## 4. First run and smoke test

```bash
cd ~/workspace/freecad
./freecadcmd smoke_test.py
```

`smoke_test.py` (in this folder) creates a document, makes a `Part::Box`
10×20×30, asserts volume == 6000.0, and exports `smoke_out/testbox.stl` +
`smoke_out/testbox.step`.

Expected (2026-10-09 run):

```
FreeCAD version: ['1', '1', '4', '20260928 (Git shallow)', ...]
Box volume (expect 6000.0): 6000.0
WROTE .../smoke_out/testbox.stl (684 bytes)
WROTE .../smoke_out/testbox.step (6854 bytes)
SMOKE TEST PASSED
```

(The 684-byte STL is correct: a box tessellates to 12 triangles;
84-byte header + 12×50 bytes = 684.)

## 5. Python dependencies: numpy / scipy / trimesh

Bundled in the AppImage (verified 2026-10-09 via the bundled `python`):

| Package | Version | Source |
|---|---|---|
| Python | 3.11.14 | bundled |
| numpy | 1.26.4 | bundled |
| scipy | 1.16.3 | bundled |
| trimesh | **missing** | installed below → 5.1.0 |

trimesh install — **two gotchas found the hard way, read before running:**

**Gotcha 1 — pip drags in numpy 2.x.** `trimesh==5.1.0` (the version pinned by
the mesh-to-cad pipeline in `scripts/requirements-locked.txt`) declares a numpy
dependency, so a plain `pip install` also installed **numpy 2.4.6** into the
target dir — which would shadow the bundled 1.26.4 and break scipy. Fix: install
with `--no-deps`. trimesh 5.1.0 was then verified working against numpy 1.26.4
(volume/watertight/bounds all correct on the smoke-test STL).

**Gotcha 2 — my first version guess was wrong.** I tried `trimesh==4.4.5`
from memory; it doesn't exist (latest is 5.1.1). Don't guess versions —
take the pin from the pipeline's `requirements-locked.txt`.

Commands (run verbatim):

```bash
FC_PY=~/workspace/freecad/app/squashfs-root/usr/bin/python
DEPS="$HOME/.local/share/FreeCAD/AdditionalPythonPackages"
$FC_PY -m pip install --no-deps --target="$DEPS" "trimesh==5.1.0"
```

Expected: `Successfully installed trimesh-5.1.0` and **no** numpy line.
Verify the target dir contains only `trimesh/`, `trimesh-5.1.0.dist-info/`
(no `numpy*`).

## 6. Headless notes (quirks that cost time)

1. **The embedded interpreter ignores `PYTHONPATH`.** The env var is visible
   inside freecadcmd but never lands on `sys.path` (verified). Don't fight it.
2. **`AdditionalPythonPackages` is NOT auto-added in console mode.**
   (GUI mode adds it; `freecadcmd` does not — verified via `sys.path` dump.)
3. **The fix that works:** a `.pth` file in the user site-packages, which the
   embedded interpreter *does* honor (`site.ENABLE_USER_SITE` is True,
   usersite is `~/.local/lib/python3.11/site-packages`):
   ```bash
   mkdir -p ~/.local/lib/python3.11/site-packages
   echo "$HOME/.local/share/FreeCAD/AdditionalPythonPackages" \
     > ~/.local/lib/python3.11/site-packages/freecad-deps.pth
   ```
   After this, `import trimesh` works in bare `freecadcmd` with no per-script
   bootstrap (verified).
4. **User config dir is versioned:** `~/.local/share/FreeCAD/v1-1/`
   (macros, config). The unversioned dir holds only `AdditionalPythonPackages`.
5. **Scripts run with cwd = wherever you invoke from.** Use absolute paths
   in scripts (the smoke test writes next to itself via `__file__`).

## 7. Version parity — what Dennis needs on Windows

To stay in lockstep with this VM:

- Download **FreeCAD 1.1.4** for Windows from https://www.freecad.org/downloads.php
  (the `Windows-x86_64-py311` installer — same Python 3.11 line as here).
- Confirm via Help → About: `1.1.4`.
- trimesh on his side: same pin, `trimesh==5.1.0`, installed with the
  workbench's guided-install path (which must use the equivalent of
  `--no-deps` — see §5 Gotcha 1 — or it will break his bundled numpy too).
- FCStd / STEP / STL files and Python scripts move between us unchanged at
  the same version. Do NOT mix 1.0.x and 1.1.x on the two ends without
  re-verifying — the user config dir is versioned (`v1-1`) for a reason.

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `./FreeCAD....AppImage` → `dlopen(): error loading libfuse.so.2` (or similar FUSE error) | No `/dev/fuse` on this VM | Don't run it — use `--appimage-extract` (§3) and run `squashfs-root/usr/bin/freecadcmd` |
| `apt-cache policy freecad` → empty | No freecad metadata in this image's apt lists | Irrelevant — AppImage path doesn't use apt |
| `pip install trimesh==X.Y.Z` → "No matching distribution" | Guessed version doesn't exist | Check the pipeline's `scripts/requirements-locked.txt` for the pin; check PyPI for what exists |
| `import trimesh` → `ModuleNotFoundError` in freecadcmd, but the files are in `AdditionalPythonPackages` | Console mode doesn't add that dir; `PYTHONPATH` is ignored | The `.pth` file (§6.3) — re-create it if missing |
| `import scipy` (or others) breaks after installing trimesh | numpy 2.x got installed alongside and shadows bundled 1.26.4 | Delete `numpy*` from `AdditionalPythonPackages`, reinstall trimesh with `--no-deps` (§5) |
| GitHub API `/releases/tags/1.0.1` → 404 | Tag naming; also the API flaked once with a 404 on a valid path | List `/repos/FreeCAD/FreeCAD/releases` and pick the tag from there; retry transient 404s |
| GUI `freecad` binary won't start | No display on this VM | Expected — console mode (`freecadcmd`) is the supported path here |

## 9. Final verification checklist (all green 2026-10-09)

- [x] AppImage SHA256 matches published value
- [x] `--appimage-extract` succeeds without FUSE
- [x] `freecadcmd` prints `FreeCAD 1.1.4, Libs: 1.1.4R20260928`
- [x] `import FreeCAD` works in console mode
- [x] Smoke test: Part box volume 6000.0, STL (684 B) + STEP (6854 B) exported
- [x] numpy 1.26.4 + scipy 1.16.3 importable from bundled Python
- [x] trimesh 5.1.0 importable in bare freecadcmd (via `.pth`), no numpy shadowing
- [x] trimesh reads the smoke-test STL: volume 6000.0, watertight, correct bounds
- [x] `~/workspace/freecad/freecadcmd` wrapper reproduces the smoke test

Disk footprint: AppImage 782 MB (`dl/`, keep for re-extraction) + extracted
`squashfs-root/` ~2.6 GB. Total ≈ 3.4 GB under `~/workspace/freecad/`.

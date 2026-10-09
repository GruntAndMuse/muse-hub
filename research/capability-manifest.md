# VM Capability Manifest — "Know Your Machine"

**Status:** reference document · **Probed:** 2026-10-09 · **Review after:** 90 days (VM images change)
**License:** MIT · **Confidence:** high on probed values (every number below came from a live command run on 2026-10-09); medium on the persistence model (from runtime docs, not independently tested — see §4)

This is the machine profile for the Muse sandbox VM. Read it before you plan work here: it tells you what this box can and cannot do, so you don't discover the limits mid-run. Written for every Muse after this one.

---

## 1. OS and resources (probed 2026-10-09)

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS (Noble Numbat) |
| Kernel | 7.0.0-39-generic |
| CPUs | 2 (`nproc`) |
| RAM | 7.7 GiB total — **~760 MiB available at probe time, no swap** |
| Root disk (`/`) | overlay, 7.5G total, 2% used |
| `/tmp` | tmpfs, 512M, RAM-backed |
| Home (`/home/hatch`) | `/dev/mapper/rv`, 100G total, **91G used / 9.2G available (91% full)** — and `~/workspace` alone accounts for ~93G of it (measured 2026-10-09) |
| GPU | **none** (`nvidia-smi` absent) — CPU-only |
| File descriptors | `ulimit -n` 4096 |

**What this means:** RAM is the binding constraint. There is no swap to catch you — a memory-hungry job (dense-mesh FreeCAD work, big numpy arrays) will get OOM-killed, not slow down. Home-disk is 91% full: check `df -h` before writing anything GB-scale. No GPU: local model inference is CPU/RAM-bound and slow.

---

## 2. Hard limits

- **No FUSE** (`/dev/fuse` absent — verified). AppImages cannot execute directly.
  → Workaround: `--appimage-extract`, run from the extracted `squashfs-root/`. (Proven by the FreeCAD 1.1.4 install.)
- **No display** (`DISPLAY` empty — verified). Console/headless only.
  → Workaround: `freecadcmd` for FreeCAD; Qt offscreen platform for rendering. No GUI app will launch.
- **`/tmp` is tmpfs (512M) AND subject to mid-session wipes** (documented 2026-09-29: unzip dir + page images vanished between tool calls).
  → Workaround: session scratch lives in `~/workspace/`, never `/tmp`. `/tmp` is only for disposable single-call intermediates. (See tool-quirks entry `vm-environment`.)
- **Egress goes through a proxy** (`http_proxy`/`https_proxy` set). Observed transient flakiness: 30s read timeouts and proxy errors that succeed on retry.
  → Workaround: retry once before calling a failure. A single failed fetch proves nothing.
- **No conda, no Java, no qpdf on PATH** (verified 2026-10-09). Don't assume them.
- **No chromium/chrome binary on PATH.** Browser access is via the agent browser tooling (`meta-chromium` under `/opt/hatch-image/`), not a local binary you can drive yourself.

---

## 3. What's installed (probed 2026-10-09)

**Python:** 3.12.3, pip 24.0. Notable packages: numpy 1.26.4, scipy 1.11.4, matplotlib 3.6.3, pillow 10.2.0, requests 2.31.0, trimesh 5.1.1.

**FreeCAD:** 1.1.4 (Revision 20260928), AppImage-extracted at `~/workspace/freecad/`, console mode verified working. Wrapper: `~/workspace/freecad/freecadcmd`. See `~/workspace/freecad/SETUP.md` for the full install story.

**CLIs on PATH:**
- `facebook-cli`, `hatch_gws_cli` → `/opt/hatch/bin/`
- `git` → `/usr/bin/git`
- `node` → `/usr/bin/node`; `bun`, `npx`, `npm`, `codex`, `messenger-cli` → `/opt/hatch-image/bin/`

**Identity:** the shell runs as **root** (`whoami` → `root`). The sudo question is moot, and `apt` works (verified with a dry-run install). But see §4 — system changes don't survive.

---

## 4. Persistence model

- **`~` (including `~/workspace/`) persists** across VM restarts and replacements. `/home/hatch` sits on a real 100G volume. Confidence: high (runtime docs + the volume is plainly a persistent mount).
- **Ephemeral:** `/tmp`, `/usr/local/bin`, `/etc`, `/root`, `/var` — treat anything written outside `~` as gone after a reboot or VM replacement. Confidence: medium (from the runtime's own documentation; not independently tested by destroying a VM).
- **Consequence:** durable tools, scripts, installs, and docs live under `~/workspace/`. An `apt install` or a `/usr/local/bin` drop is per-VM convenience, not infrastructure. The FreeCAD install was deliberately placed at `~/workspace/freecad/` for exactly this reason.

---

## 5. Quirks with workarounds (all first-hand)

1. **2026-10-09 — No FUSE on this VM.** AppImage binaries refuse to run (`--appimage-extract` works without FUSE). Fix: extract once, run from `squashfs-root/`, keep the AppImage in `dl/` for re-extraction. (FreeCAD install; see also tool-quirks `freecad-python`.)
2. **2026-10-09 — FreeCAD's embedded interpreter ignores `PYTHONPATH`**, and console mode doesn't auto-add `AdditionalPythonPackages`. Fix: a `.pth` file in user site-packages (`~/.local/lib/python3.11/site-packages/freecad-deps.pth`) so `import trimesh` works with zero per-script bootstrap. (tool-quirks `freecad-python`.)
3. **2026-10-09 — `pip install trimesh` drags in numpy 2.x**, which shadows the FreeCAD-bundled 1.26.4 and breaks scipy. Fix: `pip install --no-deps`, take the pin from `requirements-locked.txt`, verify `import` inside `freecadcmd` afterward. (tool-quirks `freecad-python`.)
4. **2026-09-29 — `/tmp` wiped mid-session.** Fix: workspace scratch, never `/tmp`. (tool-quirks `vm-environment`.)
5. **2026-10-09 — Egress proxy flakes transiently.** Fix: retry once; a single timeout is not a verdict.
6. **2026-10-09 — Home disk 91% full.** Fix: `df -h` before writing GB-scale files. The "go ham on Drive storage" rule does not apply to the VM's disk.

---

## 6. Surprises from this probe (2026-10-09)

Things the prober didn't expect, recorded so the next Muse doesn't have to be surprised either:
- The shell is **root** — the whole sudo dance is unnecessary here.
- RAM is **critically tight** (760M free of 7.7G, zero swap). This is the number most likely to kill your job.
- **No GPU at all** — any plan involving local CUDA inference on this box is dead on arrival.
- Home volume at **91%** — the FreeCAD tree (3.4G) plus workspace history are eating it.
- `qpdf` is **not on PATH** despite past pipeline work using it — check before assuming.

---

## 7. Re-verification

- Re-run the probes every 90 days or after any VM image/runtime change, and update the values + dates in place.
- Invalidation triggers: kernel version change, RAM/CPU change, `/dev/fuse` appearing, a GPU appearing, home-volume repartitioning.
- Related: tool-quirks registry (`registries/tool-quirks/` — entries `vm-environment`, `freecad-python`), `~/workspace/freecad/SETUP.md`, `~/workspace/freecad/PARITY-AUDIT.md`.

---

*Probed first-hand on 2026-10-09. If a number here disagrees with your live box, trust your box and update this file — that's the deal.*

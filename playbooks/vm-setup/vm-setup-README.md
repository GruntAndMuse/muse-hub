# vm-setup.sh — one command: bare Hatch VM → full working capability

MIT License — ships public, written for the followers.

## What it does

`~/workspace/bin/vm-setup.sh` brings a fresh Hatch VM to the working state
every Muse expects, then proves it with a PASS/FAIL self-test. Seven sections:

1. **Python toolchain** — `python3`, `pip`, `venv` present and working.
2. **System Python packages (VERIFY ONLY)** — numpy 1.26.4, scipy 1.11.4,
   matplotlib 3.6.3, pillow 10.2.0, requests 2.31.0, checked by import.
   These are apt-managed in `/usr/lib/python3/dist-packages`; the script
   never pip-installs over them.
3. **User Python packages (pinned, installed if needed)** — trimesh 5.1.1,
   networkx 3.7 via `pip install --user`, from
   `vm-setup-requirements.txt`. Includes the anti-shadowing guard: after any
   install it verifies numpy still resolves to dist-packages (the numpy-2.x
   disaster must never recur — see research-cache topic
   `freecad-python-env-quirks`).
4. **PATH** — `~/workspace/bin` on PATH (idempotent `~/.bashrc` edit),
   all `*.sh` helpers executable.
5. **Research cache CLI** — `rc.py check` passes.
6. **Directory skeleton** — `research-cache/`, `browser/`, `muse-hub/`,
   `freecad/` exist (created if missing).
7. **FreeCAD presence (VERIFY ONLY)** — checks the `freecadcmd` wrapper
   exists. Never installs it (see below).

Exit code 0 = all PASS. Non-zero = count of FAILs; each FAIL prints a FIX
line. No bare tracebacks, nothing half-installed.

## What it deliberately does NOT do

- **FreeCAD install** — ~3.4GB, needs the documented dance (no FUSE, the
  numpy-2.x gotcha, the `.pth` fix). Follow `~/workspace/freecad/SETUP.md`.
  The script only verifies presence.
- **Credentials** — no API keys, no logins, no vault interaction. Ever.
- **apt packages** — system Python packages are verify-only. If one is
  missing on a fresh image, the FAIL line tells you the apt package; a
  human (or a human-approved step) installs it.
- **Anything needing the user** — no prompts, no choices. It either fixes
  it unattended or prints the FIX line and moves on.

## How a fresh Muse runs it

```bash
bash ~/workspace/bin/vm-setup.sh
```

That's it. If the workspace itself is fresh (new VM), fetch this repo first
(publication: GruntAndMuse GitHub monorepo, MIT — see
`~/workspace/muse-hub/PUBLICATION.md`), then run the script. Re-running on
a working machine should print all-PASS with 0 changes — that no-op run is
the idempotency proof.

## The two-tier package rule

This is the lesson the script exists to enforce:

- **Tier 1 (system/apt):** verify, never install over. Shadowing a
  dist-packages numpy with a pip numpy breaks scipy and everything
  downstream.
- **Tier 2 (user/pip):** always pinned, `--user` only, `--no-deps` thinking
  even when plain install works. The pin is the fix; unpinned installs are
  how the numpy-2.x disaster happened.

The pipeline's own `requirements-locked.txt` (numpy 2.5.3, scipy 1.18.1)
is a *different environment* — the pipeline venv, not the VM system python.
Don't mix them; the README in the lockfile says the same.

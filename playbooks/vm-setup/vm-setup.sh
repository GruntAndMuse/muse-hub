#!/usr/bin/env bash
# vm-setup.sh — one command: bare Hatch VM -> full working capability.
#
# MIT License. See vm-setup-README.md.
#
# WHAT: verifies/installs the Python toolchain, puts ~/workspace/bin on PATH,
# checks the research-cache CLI, creates the directory skeleton, and verifies
# (not installs) FreeCAD presence. Ends with a PASS/FAIL self-test.
#
# IDEMPOTENT: re-running changes nothing that already works. Every mutating
# step checks state first. Safe to run on a live, working VM.
#
# NOTE: `set -u` but NOT `set -e` — a failed check must record FAIL and
# continue, not abort the whole run. The exit code at the end is the verdict.

set -uo pipefail

FAIL=0
CHANGED=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; echo "      FIX: $2"; FAIL=$((FAIL + 1)); }
info() { echo "  -> $1"; }
changed() { echo "  ++ $1"; CHANGED=$((CHANGED + 1)); }

echo "=== vm-setup: Hatch VM capability check ==="
echo "    idempotent — re-running is safe; skips what already works."
echo ""

# ---------------------------------------------------------------- python core
echo "--- 1. Python toolchain (python3, pip, venv) ---"
if command -v python3 >/dev/null 2>&1; then
    pass "python3 present: $(python3 --version 2>&1)"
else
    fail "python3 not found on PATH" "Install python3 via apt: sudo apt install python3"
fi

if python3 -m pip --version >/dev/null 2>&1; then
    pass "pip present: $(python3 -m pip --version 2>/dev/null | head -1)"
else
    fail "pip not importable" "Install via apt: sudo apt install python3-pip"
fi

if python3 -m venv --help >/dev/null 2>&1; then
    pass "venv module works"
else
    fail "python3 -m venv broken" "Install via apt: sudo apt install python3-venv"
fi
echo ""

# ------------------------------------------------- tier 1: system (apt) packages
echo "--- 2. System Python packages (VERIFY ONLY — never pip over these) ---"
info "These are apt-managed in /usr/lib/python3/dist-packages."
# module|version pairs, pinned. See vm-setup-requirements.txt for why two tiers.
SYS_PKGS="numpy|1.26.4 scipy|1.11.4 matplotlib|3.6.3 PIL|10.2.0 requests|2.31.0"
for spec in $SYS_PKGS; do
    mod="${spec%%|*}"; want="${spec##*|}"
    got="$(python3 -c "import $mod; print($mod.__version__)" 2>/dev/null || echo MISSING)"
    if [ "$got" = "$want" ]; then
        loc="$(python3 -c "import $mod, os; print(os.path.dirname($mod.__file__))" 2>/dev/null)"
        pass "$mod==$want ($loc)"
    elif [ "$got" = "MISSING" ]; then
        fail "$mod not importable (want $want)" \
            "System package missing — install via apt (python3-$mod), do NOT pip-install over dist-packages."
    else
        fail "$mod is $got, want $want" \
            "Version drift in a system package. Do not pip-force it; reconcile via apt or venv."
    fi
done
echo ""

# --------------------------------------------------- tier 2: user (pip) packages
echo "--- 3. User Python packages (pip --user, pinned, install if needed) ---"
REQ_FILE="$HOME/workspace/bin/vm-setup-requirements.txt"
if [ ! -f "$REQ_FILE" ]; then
    fail "lockfile missing: $REQ_FILE" "Restore vm-setup-requirements.txt from the repo."
else
    pass "lockfile present: $REQ_FILE"
    while IFS= read -r line; do
        # strip comments and blanks
        clean="$(echo "$line" | sed 's/#.*//' | tr -d '[:space:]')"
        [ -z "$clean" ] && continue
        # Only pinned `pkg==ver` lines are processed. Tier-1 (system/apt)
        # packages live in comments in this file — verify-only, never pip.
        case "$clean" in
            *==*) ;;
            *) continue ;;
        esac
        pkg="${clean%%==*}"; want="${clean##*==}"
        # pip package name vs import name can differ (pillow->PIL); map it
        case "$pkg" in
            pillow) mod="PIL";; *) mod="$pkg";;
        esac
        got="$(python3 -c "import $mod; print($mod.__version__)" 2>/dev/null || echo MISSING)"
        if [ "$got" = "$want" ]; then
            pass "$pkg==$want already installed"
            continue
        fi
        info "$pkg is '$got', want '$want' — installing pinned..."
        if python3 -m pip install --user --quiet "$clean" 2>/tmp/vm-setup-pip.log; then
            changed "installed $clean"
        else
            # PEP 668 externally-managed environments need the explicit flag.
            # Retry once with it, loudly — never silently.
            info "plain pip refused (externally-managed?), retrying with --break-system-packages"
            if python3 -m pip install --user --quiet --break-system-packages "$clean" 2>/tmp/vm-setup-pip.log; then
                changed "installed $clean (with --break-system-packages)"
            else
                fail "pip install $clean failed" \
                    "See /tmp/vm-setup-pip.log. Do NOT install unpinned to 'fix' it."
                continue
            fi
        fi
        got2="$(python3 -c "import $mod; print($mod.__version__)" 2>/dev/null || echo MISSING)"
        if [ "$got2" = "$want" ]; then
            pass "$pkg==$want installed and verified"
        else
            fail "$pkg installed but version is '$got2', want '$want'" \
                "Pinned install did not stick — investigate before proceeding."
        fi
    done < "$REQ_FILE"
    # Anti-shadowing guard: the numpy-2.x disaster must never recur.
    npy_v="$(python3 -c 'import numpy; print(numpy.__version__)' 2>/dev/null)"
    npy_f="$(python3 -c 'import numpy; print(numpy.__file__)' 2>/dev/null)"
    case "$npy_f" in
        /usr/lib/python3/dist-packages/*)
            pass "numpy still $npy_v from dist-packages (no shadowing)"
            ;;
        *)
            fail "numpy resolves to $npy_f (version $npy_v)" \
                "A user-site numpy is shadowing the system one — uninstall it: pip uninstall -y numpy"
            ;;
    esac
fi
echo ""

# ------------------------------------------------------------------ PATH/bin
echo "--- 4. ~/workspace/bin on PATH, helpers executable ---"
if [ -d "$HOME/workspace/bin" ]; then
    pass "directory exists: ~/workspace/bin"
else
    fail "directory missing: ~/workspace/bin" "Create it: mkdir -p ~/workspace/bin"
fi
if [[ ":$PATH:" == *":$HOME/workspace/bin:"* ]]; then
    pass "~/workspace/bin on PATH"
else
    BASHRC="$HOME/.bashrc"
    LINE='export PATH="$HOME/workspace/bin:$PATH"'
    if grep -qxF "$LINE" "$BASHRC" 2>/dev/null; then
        info "bashrc already has the PATH line (session just needs re-sourcing)"
    else
        echo "$LINE" >> "$BASHRC"
        changed "appended PATH export to ~/.bashrc"
    fi
    export PATH="$HOME/workspace/bin:$PATH"
    pass "~/workspace/bin added to PATH for this run (re-source ~/.bashrc for new shells)"
fi
helpers_ok=1
for h in "$HOME"/workspace/bin/*.sh; do
    [ -e "$h" ] || continue
    if [ -x "$h" ]; then
        : # quiet per-file; summary below
    else
        fail "not executable: $h" "chmod +x $h"
        helpers_ok=0
    fi
done
[ "$helpers_ok" = 1 ] && pass "all ~/workspace/bin/*.sh helpers executable"
echo ""

# ------------------------------------------------------------ research cache
echo "--- 5. Research cache CLI (rc.py) ---"
RC="$HOME/workspace/research-cache/rc.py"
if [ -x "$RC" ] || [ -f "$RC" ]; then
    if out="$(python3 "$RC" check 2>&1)"; then
        pass "rc.py check: $out"
    else
        fail "rc.py check failed: $out" "Run: python3 ~/workspace/research-cache/rc.py check — fix violations."
    fi
else
    fail "rc.py missing: $RC" "Restore ~/workspace/research-cache/ from the repo."
fi
echo ""

# -------------------------------------------------------- directory skeleton
echo "--- 6. Directory skeleton ---"
for d in research-cache browser muse-hub freecad; do
    target="$HOME/workspace/$d"
    if [ -d "$target" ]; then
        pass "~/workspace/$d exists"
    else
        mkdir -p "$target"
        changed "created ~/workspace/$d"
        pass "~/workspace/$d created"
    fi
done
echo ""

# ------------------------------------------------------- freecad (verify only)
echo "--- 7. FreeCAD presence (VERIFY ONLY — install is separate, see SETUP.md) ---"
info "FreeCAD is ~3.4GB; this script never installs it."
if [ -x "$HOME/workspace/freecad/freecadcmd" ]; then
    pass "freecadcmd wrapper present and executable"
else
    fail "freecadcmd not found at ~/workspace/freecad/freecadcmd" \
        "Follow ~/workspace/freecad/SETUP.md to install FreeCAD 1.1.4 (documented, reproducible)."
fi
echo ""

# ------------------------------------------------------------------ verdict
echo "=== verdict ==="
if [ "$FAIL" = 0 ]; then
    echo "ALL CHECKS PASSED ($CHANGED change(s) made this run; 0 means fully idempotent no-op)."
    exit 0
else
    echo "$FAIL check(s) FAILED — see FIX lines above. Nothing was half-installed."
    exit 1
fi

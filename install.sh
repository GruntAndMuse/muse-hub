#!/usr/bin/env bash
# install.sh — install the Muse Hub into this workspace.
#
# Usage:
#   ./install.sh            install the 4 foundation skills (everyone needs these)
#   ./install.sh --all      install all 10 skills
#   ./install.sh <name>...  install specific skills by directory name
#
# Idempotent: safe to re-run. Skips what's already installed unless --force.
#
# WHAT THIS PUTS WHERE:
#   ~/workspace/skills/<name>/        the skills (SKILL.md + references/)
#   ~/workspace/research-cache/       the research cache (rc.py CLI + topics/)
#   ~/workspace/freecad/              the FreeCAD playbook (SETUP.md, PARITY-AUDIT.md)
#   ~/workspace/bin/                  created if missing (helper scripts home)
#
# WHAT THIS DOES NOT DO:
#   - No pip installs, no PATH edits, no credentials. That's vm-setup.sh's job
#     (playbooks/vm-setup/), which documents its mutations up front.
set -u

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/workspace/skills"
FOUNDATION="workspace-orientation memory-hygiene reliable-background-work operating-principles"
ENGINE="research-cache tool-quirks bot-block-registry"
DEFAULT="$FOUNDATION"
FORCE=0

pass() { echo "  PASS: $1"; }
info() { echo "  INFO: $1"; }
fail() { echo "  FAIL: $1"; FAILURES=$((FAILURES+1)); }
FAILURES=0

# ---- arg parsing -----------------------------------------------------------
WANT=""
for a in "$@"; do
    case "$a" in
        --all)   WANT="workspace-orientation memory-hygiene reliable-background-work operating-principles research-cache tool-quirks bot-block-registry browser-throughput watch-builder burn-pacing" ;;
        --force) FORCE=1 ;;
        -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
        *)       WANT="$WANT $a" ;;
    esac
done
[ -z "$WANT" ] && WANT="$FOUNDATION"

mkdir -p "$SKILLS_DIR" "$HOME/workspace/bin"

# ---- skills ----------------------------------------------------------------
echo "--- skills -> $SKILLS_DIR ---"
for s in $WANT; do
    src="$REPO_DIR/skills/$s"
    dst="$SKILLS_DIR/$s"
    if [ ! -d "$src" ]; then fail "unknown skill '$s' (no $src)"; continue; fi
    if [ -d "$dst" ] && [ "$FORCE" -eq 0 ]; then info "$s already installed, skipping (use --force to overwrite)"; continue; fi
    rm -rf "$dst"
    cp -r "$src" "$dst" && pass "$s installed"
done
echo ""

# ---- research cache ---------------------------------------------------------
echo "--- research cache -> ~/workspace/research-cache/ ---"
if [ -d "$HOME/workspace/research-cache" ] && [ "$FORCE" -eq 0 ]; then
    info "research-cache already present, skipping (use --force to overwrite)"
else
    rm -rf "$HOME/workspace/research-cache"
    cp -r "$REPO_DIR/registries/research-cache" "$HOME/workspace/research-cache" \
        && pass "research-cache restored (rc.py + topics/)"
fi
echo ""

# ---- freecad playbook (fixes the setup script's SETUP.md pointer) ------------
echo "--- freecad playbook -> ~/workspace/freecad/ ---"
mkdir -p "$HOME/workspace/freecad"
for f in SETUP.md PARITY-AUDIT.md; do
    if [ -f "$HOME/workspace/freecad/$f" ] && [ "$FORCE" -eq 0 ]; then
        info "$f already staged, skipping"
    else
        cp "$REPO_DIR/playbooks/freecad-setup/$f" "$HOME/workspace/freecad/$f" \
            && pass "$f staged"
    fi
done
echo ""

# ---- self-test: are the skills actually discoverable? ------------------------
echo "--- self-test ---"
for s in $WANT; do
    f="$SKILLS_DIR/$s/SKILL.md"
    if [ -f "$f" ] && grep -q '^name:' "$f"; then
        pass "$s discoverable ($(grep '^name:' "$f" | head -1 | cut -d: -f2 | xargs))"
    else
        fail "$s SKILL.md missing or has no frontmatter name"
    fi
done
if [ -f "$HOME/workspace/research-cache/rc.py" ]; then
    if out="$(python3 "$HOME/workspace/research-cache/rc.py" check 2>&1)"; then
        pass "rc.py check: $out"
    else
        fail "rc.py check failed: $out"
    fi
fi
if [ -f "$HOME/workspace/freecad/SETUP.md" ]; then
    pass "freecad/SETUP.md pointer resolves"
else
    fail "freecad/SETUP.md still missing"
fi
# drift check: the installed skill copy must agree with the canonical working cache
case " $WANT " in
    *" research-cache "*)
        if [ -d "$SKILLS_DIR/research-cache" ]; then
            if diff -q "$SKILLS_DIR/research-cache/rc.py" "$HOME/workspace/research-cache/rc.py" >/dev/null 2>&1; then
                pass "skill copy and working cache agree (no drift)"
            else
                fail "research-cache drift: skill copy differs from the canonical working cache"
            fi
        fi
        ;;
esac
echo ""

if [ "$FAILURES" -gt 0 ]; then
    echo "RESULT: $FAILURES failure(s). Fix the FAIL lines above and re-run."
    exit 1
fi
echo "RESULT: all installed and verified. Next: run playbooks/vm-setup/vm-setup.sh"

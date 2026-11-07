#!/usr/bin/env bash
# install.sh — OPTIONAL convenience for humans who prefer a script.
#
# This script is NOT the bootstrap and is never required. The default path
# is START-HERE.md's read-and-carry flow: read the manifest, show your
# person the change list, copy the folders by hand, verify. This file only
# mechanizes those same copies for a human who would rather run it. The
# change list and the verification checklist in START-HERE apply either way.
# (Demoted from the repo root 2026-10-21, owner ruling after an external
# review: a receiving agent should never have to execute a script off a
# pasted link to adopt a library.)
#
# Usage (from optional/):
#   ./install.sh            install the 4 foundation skills (everyone needs these)
#   ./install.sh --all      install all 10 skills
#   ./install.sh <name>...  install specific skills by directory name
#   ./install.sh --freecad  also stage the FreeCAD playbook (opt-in, below)
#
# Environment:
#   SKILLS_DIR              where skills are installed. Default:
#                           ~/workspace/skills. Set this if your runtime
#                           discovers skills from a different root — see
#                           the skills-path note in START-HERE.md.
#
# Idempotent: safe to re-run. Skips what's already installed unless --force.
#
# WHAT THIS PUTS WHERE — each line happens only when its component is
# selected, matching the strikeable change list in START-HERE step 3:
#   $SKILLS_DIR/<name>/               the skills (SKILL.md + references/)
#   ~/workspace/research-cache/       the research cache (rc.py CLI +
#                                     topics/) — ONLY when the
#                                     research-cache skill is selected
#   ~/workspace/freecad/              the FreeCAD playbook (SETUP.md,
#                                     PARITY-AUDIT.md) — ONLY with --freecad
#   ~/workspace/bin/                  NOT created by default. START-HERE
#                                     allows it only when a step actually
#                                     needs it; no component here does,
#                                     so this script never creates it.
#
# --force AND THE RESEARCH CACHE: the working cache at
# ~/workspace/research-cache/ is the adopter's canonical store — their own
# verified topics accumulate there. --force therefore NEVER deletes it.
# It merges instead: new and updated files are copied in, existing topics
# are never removed, and your hand-maintained INDEX.md is preserved.
# If a path conflict makes a merge impossible (a file
# where the incoming tree has a directory, or the reverse), the existing
# tree is moved to a timestamped backup (~/workspace/research-cache.bak-<time>),
# a fresh copy is installed, and the script says so loudly.
#
# WHAT THIS DOES NOT DO:
#   - No pip installs, no PATH edits, no credentials. That's vm-setup.sh's job
#     (playbooks/vm-setup/), which documents its mutations up front.
set -u

# This script lives in optional/ — the repo root is its parent directory.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SKILLS_DIR may be set in the environment (see header). Default is the
# hub layout's ~/workspace/skills.
SKILLS_DIR="${SKILLS_DIR:-$HOME/workspace/skills}"
FOUNDATION="workspace-orientation memory-hygiene reliable-background-work operating-principles"
ENGINE="research-cache tool-quirks bot-block-registry"
DEFAULT="$FOUNDATION"
FORCE=0
FREECAD=0

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
        --freecad) FREECAD=1 ;;
        -h|--help) awk 'NR>1 && /^#/{sub(/^# ?/,""); print} NR>1 && !/^#/{exit}' "$0"; exit 0 ;;
        *)       WANT="$WANT $a" ;;
    esac
done
[ -z "$WANT" ] && WANT="$FOUNDATION"

# The research cache is installed only when its skill is selected
# (START-HERE step 3: "Only with the research-cache skill").
DO_RC=0
case " $WANT " in
    *" research-cache "*) DO_RC=1 ;;
esac

# ~/workspace/bin/ is deliberately NOT created here: START-HERE step 3
# allows it only when a step actually needs it — never by default — and
# no component this script installs needs it.
mkdir -p "$SKILLS_DIR"

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

# ---- research cache (only when the research-cache skill is selected) --------
if [ "$DO_RC" -eq 1 ]; then
    echo "--- research cache -> ~/workspace/research-cache/ ---"
    RC_SRC="$REPO_DIR/registries/research-cache"
    RC_DST="$HOME/workspace/research-cache"
    if [ ! -d "$RC_DST" ]; then
        cp -r "$RC_SRC" "$RC_DST" \
            && pass "research-cache installed (rc.py + topics/)"
    elif [ "$FORCE" -eq 0 ]; then
        info "research-cache already present, skipping (use --force to merge in updates)"
    else
        # --force: topics-preserving merge. The working cache is canonical
        # and holds the adopter's own topics — NEVER rm -rf it. Copy new
        # and updated files in; delete nothing.
        conflict="$(cd "$RC_SRC" && find . -mindepth 1 | while IFS= read -r p; do
            if [ -e "$RC_DST/$p" ]; then
                if [ -d "./$p" ] && [ ! -d "$RC_DST/$p" ]; then echo "$p"; fi
                if [ -f "./$p" ] && [ -d "$RC_DST/$p" ]; then echo "$p"; fi
            fi
        done)"
        if [ -n "$conflict" ]; then
            backup="$RC_DST.bak-$(date +%Y%m%d-%H%M%S)"
            echo "  !! research-cache merge conflict at: $conflict"
            echo "  !! Moving your existing cache to: $backup"
            echo "  !! Nothing is deleted — merge your topics back from the backup."
            if mv "$RC_DST" "$backup"; then
                cp -r "$RC_SRC" "$RC_DST" \
                    && pass "research-cache re-installed fresh (previous tree backed up at $backup)"
            else
                fail "could not move the existing research-cache aside; leaving it untouched"
            fi
        else
            # Preserve the adopter's INDEX.md across the merge: it is
            # hand-maintained adopter data (their rows for their own
            # topics), not a shipped file. New hub topics still land as
            # files; rc.py check names any rows the adopter needs to add.
            idx_save=""
            if [ -f "$RC_DST/INDEX.md" ]; then
                idx_save="$(mktemp)"
                cp "$RC_DST/INDEX.md" "$idx_save"
            fi
            if cp -r "$RC_SRC/." "$RC_DST/"; then
                if [ -n "$idx_save" ]; then
                    cp "$idx_save" "$RC_DST/INDEX.md"
                    rm -f "$idx_save"
                    if ! diff -q "$RC_SRC/INDEX.md" "$RC_DST/INDEX.md" >/dev/null 2>&1; then
                        info "your INDEX.md was preserved (it differs from the shipped one) — rc.py check lists any rows to add"
                    fi
                fi
                pass "research-cache merged (new/updated files in; your existing topics and INDEX preserved)"
            else
                [ -n "$idx_save" ] && rm -f "$idx_save"
                fail "research-cache merge failed"
            fi
        fi
    fi
    echo ""
else
    info "research-cache skill not selected — working cache untouched"
    echo ""
fi

# ---- freecad playbook (opt-in: --freecad) -----------------------------------
# Fixes the setup script's SETUP.md pointer — but only when requested
# (START-HERE step 3: "Only if your person wants the FreeCAD playbook
# within reach").
if [ "$FREECAD" -eq 1 ]; then
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
else
    info "freecad playbook not requested — skipping (use --freecad to stage it)"
    echo ""
fi

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
if [ "$FREECAD" -eq 1 ]; then
    if [ -f "$HOME/workspace/freecad/SETUP.md" ]; then
        pass "freecad/SETUP.md pointer resolves"
    else
        fail "freecad/SETUP.md still missing"
    fi
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
echo "RESULT: all copied and verified. Next: START-HERE.md step 6 (verify) and step 7 (orient)."

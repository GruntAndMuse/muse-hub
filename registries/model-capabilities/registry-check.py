#!/usr/bin/env python3
"""registry-check.py — mechanical validator for the model-capabilities registry.

Usage:
  registry-check.py           validate everything (frontmatter, enums, dates,
                              slug==filename, INDEX sync both directions)
  registry-check.py stale     list entries past their review_after_days

Exits 1 on any violation. Rules live in CONVENTIONS.md; this enforces the
mechanical subset.
"""
import os
import re
import sys
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
ENTRIES = os.path.join(ROOT, "entries")
INDEX = os.path.join(ROOT, "INDEX.md")

REQUIRED = ["slug", "model", "category", "license", "status", "hardware",
            "first_observed", "last_verified", "review_after_days",
            "observed_by", "confidence"]
CATEGORIES = {"jpg-cleanup", "ocr", "coding", "image", "video", "audio"}
STATUSES = {"incumbent", "challenger", "lead", "retired"}
CONFIDENCES = {"high", "medium", "low"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(path):
    with open(path) as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm


def check():
    errors = []
    files = sorted(f for f in os.listdir(ENTRIES) if f.endswith(".md"))
    seen = set()
    for fname in files:
        slug = fname[:-3]
        path = os.path.join(ENTRIES, fname)
        fm = parse_frontmatter(path)
        if fm is None:
            errors.append(f"{fname}: missing or malformed frontmatter")
            continue
        for key in REQUIRED:
            if key not in fm or not fm[key]:
                errors.append(f"{fname}: missing required field '{key}'")
        if fm.get("slug") != slug:
            errors.append(f"{fname}: slug '{fm.get('slug')}' != filename")
        if fm.get("category") not in CATEGORIES:
            errors.append(f"{fname}: bad category '{fm.get('category')}'")
        if fm.get("status") not in STATUSES:
            errors.append(f"{fname}: bad status '{fm.get('status')}'")
        if fm.get("confidence") not in CONFIDENCES:
            errors.append(f"{fname}: bad confidence '{fm.get('confidence')}'")
        for dkey in ("first_observed", "last_verified"):
            if not DATE_RE.match(fm.get(dkey, "")):
                errors.append(f"{fname}: bad date '{dkey}={fm.get(dkey)}'")
        try:
            rad = int(fm.get("review_after_days", "x"))
            if rad < 0:
                errors.append(f"{fname}: negative review_after_days")
        except ValueError:
            errors.append(f"{fname}: review_after_days not an integer")
        seen.add(slug)

    # INDEX sync both directions
    indexed = set()
    if os.path.exists(INDEX):
        with open(INDEX) as f:
            for line in f:
                m = re.search(r"\[([a-z0-9][a-z0-9.\-]*)\]\(", line)
                if m:
                    indexed.add(m.group(1))
        for slug in seen - indexed:
            errors.append(f"INDEX.md: missing entry for '{slug}'")
        for slug in indexed - seen:
            errors.append(f"INDEX.md: orphan link '{slug}' (no such entry)")
    else:
        errors.append("INDEX.md missing")
    errors.extend(prose_count_errors())
    return errors


def stale():
    today = datetime.date.today()
    out = []
    for fname in sorted(os.listdir(ENTRIES)):
        if not fname.endswith(".md"):
            continue
        fm = parse_frontmatter(os.path.join(ENTRIES, fname))
        if not fm:
            continue
        try:
            rad = int(fm["review_after_days"])
            last = datetime.date.fromisoformat(fm["last_verified"])
        except (ValueError, KeyError):
            continue
        if rad > 0 and (today - last).days > rad:
            out.append(f"{fname[:-3]}: last verified {fm['last_verified']} "
                       f"({(today - last).days}d ago, review every {rad}d)")
    return out



# --- Prose-count leg (added 2026-10-21) -----------------------------------
# No-self-contradiction rule (hub CONVENTIONS.md): a count the tree can
# compute is generated, never hand-typed. INDEX.md may carry one machine
# stamp (<!-- count: N -->), written by --stamp; any stamp or bare
# "N entries/topics" claim in INDEX.md or README.md that disagrees with
# the computed count is a violation. Born of the 2026-10-21 audit: prose
# said 88 over 90 entry files and 18 over 19, and no checker could see
# either — this leg exists so the next one fails loudly instead.

COUNT_STAMP_RE = re.compile(r"<!--\s*count:\s*(\d+)\s*-->")
COUNT_CLAIM_RE = re.compile(r"\b(\d+)\s+(entries|topics)\b")


def computed_count():
    return len([f for f in os.listdir(ENTRIES) if f.endswith(".md")])


def prose_count_errors():
    errors = []
    actual = computed_count()
    for name in ("INDEX.md", "README.md"):
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            text = f.read()
        stamps = COUNT_STAMP_RE.findall(text)
        if len(stamps) > 1:
            errors.append(f"{name}: {len(stamps)} count stamps — exactly one allowed")
        for s in stamps:
            if int(s) != actual:
                errors.append(
                    f"{name}: stamped count {s} != computed {actual} "
                    f"(fix: registry-check.py --stamp)"
                )
        for line in text.splitlines():
            if "<!--" in line:
                continue
            for m in COUNT_CLAIM_RE.finditer(line):
                if int(m.group(1)) != actual:
                    errors.append(
                        f"{name}: prose claims '{m.group(0)}' but the registry "
                        f"holds {actual} — drop the number (point, don't "
                        f"repeat) or stamp it"
                    )
    return errors


def stamp_count():
    actual = computed_count()
    with open(INDEX) as f:
        text = f.read()
    new, n = COUNT_STAMP_RE.subn(f"<!-- count: {actual} -->", text, count=1)
    if n == 0:
        lines = text.splitlines(keepends=True)
        lines.insert(1, f"<!-- count: {actual} -->\n")
        new = "".join(lines)
    with open(INDEX, "w") as f:
        f.write(new)
    print(f"Stamped INDEX.md: count {actual}.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stamp":
        sys.exit(stamp_count())
    if len(sys.argv) > 1 and sys.argv[1] == "stale":
        for line in stale():
            print(line)
    else:
        errs = check()
        if errs:
            print(f"{len(errs)} violation(s):")
            for e in errs:
                print(" -", e)
            sys.exit(1)
        print(f"OK: {len(os.listdir(ENTRIES))} entries valid, INDEX in sync.")

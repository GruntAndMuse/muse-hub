#!/usr/bin/env python3
"""registry-check.py — mechanical validator for the skill catalog.

Usage:
  registry-check.py           validate everything (frontmatter, enums, dates,
                              skill==filename, INDEX sync both directions)
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

REQUIRED = ["skill", "source", "rating", "confidence", "first_observed",
            "last_verified", "review_after_days", "used_by"]
SOURCES = {"bundled", "custom", "draft"}
RATINGS = {"excellent", "good", "unrated", "avoid"}
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
        if fm.get("skill") != slug:
            errors.append(f"{fname}: skill '{fm.get('skill')}' != filename slug '{slug}'")
        if fm.get("source") not in SOURCES:
            errors.append(f"{fname}: invalid source '{fm.get('source')}'")
        if fm.get("rating") not in RATINGS:
            errors.append(f"{fname}: invalid rating '{fm.get('rating')}'")
        if fm.get("rating") == "excellent" and fm.get("confidence") == "low":
            errors.append(f"{fname}: excellent rating with low confidence is incoherent")
        if fm.get("rating") == "excellent" and fm.get("used_by") == "none yet":
            errors.append(f"{fname}: excellent rating requires a used_by project/run")
        if fm.get("confidence") not in CONFIDENCES:
            errors.append(f"{fname}: invalid confidence '{fm.get('confidence')}'")
        for dkey in ("first_observed", "last_verified"):
            v = fm.get(dkey, "")
            if not DATE_RE.match(v):
                errors.append(f"{fname}: {dkey} '{v}' not YYYY-MM-DD")
            else:
                try:
                    datetime.date.fromisoformat(v)
                except ValueError:
                    errors.append(f"{fname}: {dkey} '{v}' not a real date")
        try:
            rad = int(fm.get("review_after_days", "x"))
            if rad < 0:
                errors.append(f"{fname}: review_after_days negative")
        except ValueError:
            errors.append(f"{fname}: review_after_days not an int")
        seen.add(slug)

    # INDEX sync both directions
    with open(INDEX) as f:
        index_text = f.read()
    index_skills = set()
    for line in index_text.splitlines():
        m = re.match(r"^\|\s*([a-z0-9][a-z0-9_\-]*)\s*\|", line)
        if m and m.group(1) != "skill":  # skip the table header row
            index_skills.add(m.group(1))
    for slug in sorted(seen - index_skills):
        errors.append(f"INDEX.md: missing row for entries/{slug}.md")
    for sk in sorted(index_skills - seen):
        errors.append(f"INDEX.md: orphan row for '{sk}' (no entries file)")

    if errors:
        print(f"{len(errors)} violation(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(seen)} entries valid, INDEX in sync.")
    return 0


def stale():
    today = datetime.date.today()
    rows = []
    for fname in sorted(os.listdir(ENTRIES)):
        if not fname.endswith(".md"):
            continue
        fm = parse_frontmatter(os.path.join(ENTRIES, fname))
        if not fm:
            continue
        try:
            last = datetime.date.fromisoformat(fm["last_verified"])
            rad = int(fm["review_after_days"])
        except (ValueError, KeyError):
            continue
        due = last + datetime.timedelta(days=rad)
        if due <= today:
            rows.append((str(due), fm["skill"], fm["rating"], fm["last_verified"]))
    if not rows:
        print("Nothing stale.")
        return 0
    print(f"{'skill':35} {'rating':>10} {'last_verified':>13} {'due':>12}")
    for due, sk, rating, last in sorted(rows):
        print(f"{sk:35} {rating:>10} {last:>13} {due:>12}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stale":
        sys.exit(stale())
    sys.exit(check())

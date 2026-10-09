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


if __name__ == "__main__":
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

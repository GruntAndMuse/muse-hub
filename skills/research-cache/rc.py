#!/usr/bin/env python3
"""rc.py — research-cache helper. lookup | stale | new | show | check. See USAGE.md."""
import datetime
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPICS = ROOT / "topics"
TEMPLATE = ROOT / "templates" / "topic-template.md"
INDEX = ROOT / "INDEX.md"

STATUSES = ("verified", "needs-verification", "inference", "stale", "disputed")
REQUIRED = ("topic", "title", "status", "verified", "last_checked", "review_after_days")
CLAIM_RE = re.compile(r"\[(verified|inference) (\d{4}-\d{2}-\d{2})\]\s*$")


def parse_frontmatter(path):
    """Return (meta dict, body str). Minimal parser for `key: value` frontmatter."""
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            s = line.strip()
            if s and not s.startswith("#") and ":" in s:
                k, v = s.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body


def all_topics():
    out = []
    for p in sorted(TOPICS.glob("*.md")):
        meta, body = parse_frontmatter(p)
        meta["_path"] = p
        meta["_body"] = body
        out.append(meta)
    return out


def review_by(meta):
    """Return (state, date_str): state is fresh|stale|unknown."""
    try:
        days = int(meta.get("review_after_days", "90"))
        last = datetime.date.fromisoformat(meta.get("last_checked", ""))
    except (ValueError, TypeError):
        return "unknown", "?"
    due = last + datetime.timedelta(days=days)
    state = "stale" if datetime.date.today() > due else "fresh"
    return state, due.isoformat()


def fmt_header(meta):
    state, due = review_by(meta)
    flag = {"fresh": "OK ", "stale": "STALE", "unknown": "????"}[state]
    return (f"[{flag}] {meta.get('topic')} — {meta.get('title')}\n"
            f"       status={meta.get('status')} verified={meta.get('verified')} "
            f"last_checked={meta.get('last_checked')} review_by={due}")


def stem(w):
    """Naive stemmer: strip common suffixes. Favors recall over precision —
    for this tool a false hit costs a skim, a miss costs a re-derivation."""
    w = w.lower()
    for suf in ("ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[:-len(suf)]
    return w


def tokens_of(text):
    return {stem(w) for w in re.findall(r"[a-z0-9]+", text.lower())}


def cmd_lookup(keywords):
    # split on whitespace so both `lookup a b` and `lookup "a b"` work
    keywords = [w for k in keywords for w in k.split()]
    stems = [stem(k) for k in keywords]
    hits = []
    for meta in all_topics():
        hay = " ".join([
            meta.get("topic", ""),
            meta.get("title", ""),
            meta.get("status", ""),
            meta.get("aliases", ""),
            meta["_body"],
        ])
        toks = tokens_of(hay)
        if all(s in toks for s in stems):
            hits.append(meta)
    if not hits:
        print(f"No cache hit for: {' '.join(keywords)} — research normally, then write it back (see USAGE.md).")
        return
    for meta in hits:
        print(fmt_header(meta))
        print(f"       file: topics/{meta['_path'].name}")
        state, _ = review_by(meta)
        if state == "stale":
            print("       -> past review date: re-verify before relying, then update the entry.")
        print()


def cmd_stale():
    topics = all_topics()
    stale = [(m, d) for m in topics for (s, d) in [review_by(m)] if s == "stale"]
    unknown = [m for m in topics for (s, d) in [review_by(m)] if s == "unknown"]
    if not stale and not unknown:
        print("Cache is fresh — nothing past its review date.")
        return
    for meta, due in stale:
        print(f"STALE  {meta.get('topic')} (review was due {due}) — topics/{meta['_path'].name}")
    for meta in unknown:
        print(f"????   {meta.get('topic')} (bad/missing dates) — topics/{meta['_path'].name}")


def cmd_new(slug):
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        print("Slug must be lowercase letters, numbers, dashes.")
        sys.exit(1)
    dest = TOPICS / f"{slug}.md"
    if dest.exists():
        print(f"topics/{slug}.md already exists — edit it instead.")
        sys.exit(1)
    shutil.copy(TEMPLATE, dest)
    text = dest.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()
    text = text.replace("topic: <slug-lowercase-with-dashes>", f"topic: {slug}")
    text = text.replace("<YYYY-MM-DD of last verification of the core claims, or \"never\">", "never")
    text = text.replace("<YYYY-MM-DD>", today)
    dest.write_text(text, encoding="utf-8")
    print(f"Created topics/{slug}.md — fill it in per the template, then add a row to INDEX.md.")
    print("Run `./rc.py check` when done — it validates the entry.")


def cmd_show(slug):
    p = TOPICS / f"{slug}.md"
    if not p.exists():
        print(f"No such topic: {slug}")
        sys.exit(1)
    meta, body = parse_frontmatter(p)
    meta["_path"] = p
    meta["_body"] = body
    print(fmt_header(meta))
    print(f"       aliases: {meta.get('aliases', '—')}")
    print()
    print(body.strip())


def index_slugs():
    """Parse topic slugs from the INDEX.md table rows."""
    slugs = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\[([a-z0-9-]+)\]\(topics/[a-z0-9-]+\.md\)", line)
        if m:
            slugs.append(m.group(1))
    return slugs


def cmd_check():
    """Validate every topic file and INDEX.md consistency. Exit 1 on any violation."""
    errors = []
    topics = all_topics()
    for meta in topics:
        slug_file = meta["_path"].stem
        where = f"topics/{meta['_path'].name}"
        for field in REQUIRED:
            if field not in meta or not meta[field]:
                errors.append(f"{where}: missing required frontmatter field `{field}`")
        if meta.get("topic") != slug_file:
            errors.append(f"{where}: frontmatter topic `{meta.get('topic')}` != filename slug `{slug_file}`")
        if meta.get("status") not in STATUSES:
            errors.append(f"{where}: bad status `{meta.get('status')}` (must be one of {', '.join(STATUSES)})")
        v = meta.get("verified", "")
        if v != "never":
            try:
                datetime.date.fromisoformat(v)
            except ValueError:
                errors.append(f"{where}: `verified` must be a date or `never`, got `{v}`")
        try:
            datetime.date.fromisoformat(meta.get("last_checked", ""))
        except ValueError:
            errors.append(f"{where}: bad `last_checked` date `{meta.get('last_checked')}`")
        try:
            days = int(meta.get("review_after_days", ""))
            if days < 0:
                raise ValueError
        except (ValueError, TypeError):
            errors.append(f"{where}: `review_after_days` must be an int >= 0")
        # claim tags: every bullet under ## Findings must end with a tag
        in_findings = False
        for line in meta["_body"].splitlines():
            if line.startswith("## "):
                in_findings = line.strip() == "## Findings"
                continue
            if in_findings and line.strip().startswith("- "):
                if not CLAIM_RE.search(line):
                    errors.append(f"{where}: claim missing [verified|inference YYYY-MM-DD] tag: {line.strip()[:80]}")
                else:
                    try:
                        datetime.date.fromisoformat(CLAIM_RE.search(line).group(2))
                    except ValueError:
                        errors.append(f"{where}: bad claim date: {line.strip()[:80]}")
    # INDEX consistency
    idx = index_slugs()
    files = sorted(m["_path"].stem for m in topics)
    for s in files:
        if s not in idx:
            errors.append(f"INDEX.md: missing row for topics/{s}.md")
    for s in idx:
        if s not in files:
            errors.append(f"INDEX.md: orphan row for missing topics/{s}.md")
    if idx != sorted(idx):
        errors.append("INDEX.md: rows are not sorted by slug")
    if errors:
        print(f"{len(errors)} convention violation(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK — {len(topics)} topics, INDEX.md in sync, all conventions hold.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("lookup", "stale", "new", "show", "check"):
        print("usage: rc.py lookup <keywords...> | rc.py stale | rc.py new <topic-slug> | rc.py show <slug> | rc.py check")
        sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "lookup":
        if not args:
            print("usage: rc.py lookup <keywords...>")
            sys.exit(1)
        cmd_lookup(args)
    elif cmd == "stale":
        cmd_stale()
    elif cmd == "new":
        if len(args) != 1:
            print("usage: rc.py new <topic-slug>")
            sys.exit(1)
        cmd_new(args[0])
    elif cmd == "show":
        if len(args) != 1:
            print("usage: rc.py show <slug>")
            sys.exit(1)
        cmd_show(args[0])
    elif cmd == "check":
        cmd_check()


if __name__ == "__main__":
    main()

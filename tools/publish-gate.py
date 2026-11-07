#!/usr/bin/env python3
"""publish-gate.py — the fail-closed publish gate for the muse-hub repo.

Owner order, 2026-10-21: two files whose own headers declared them
unpublishable were published anyway on 2026-10-09. This gate exists so
that class of failure is mechanically impossible: no tree publishes
without a green gate receipt for the exact tree being published, and a
self-marked file blocks the batch no matter what else is true.

Stdlib only. Deterministic: same tree + manifest + public listing +
denylist + allowlist always produce the same findings. No network: the
public tree listing is fetched beforehand (see fetch-public-tree.py)
and handed in as a file.

USAGE
  publish-gate.py [--tree DIR] [--manifest FILE] [--public-tree FILE]
                  [--denylist FILE] [--allowlist FILE] [--receipt FILE]
  publish-gate.py --verify-receipt [--tree DIR] [--manifest FILE]
                  [--receipt FILE]

DENYLIST
  The denylist itself is private and never ships with this script.
  Resolution order: --denylist FILE; else a denylist.txt beside this
  script; else the gate fails closed (exit 3) with a clear message.
  Anyone running the gate supplies their own list. The allowlist is
  likewise operator-supplied (publish-gate-allowlist.txt beside this
  script); a missing one is a configuration error, not a pass.

EXIT CODES
  0  GREEN — receipt written (or, with --verify-receipt, receipt matches)
  1  BLOCK — at least one blocking finding; nothing may publish
  2  REVIEW-REQUIRED — no blocks, but the manifest does not enumerate
     every first-publish file, or names paths the diff does not contain
  3  CONFIG ERROR — a required input is missing or mislocated (the gate
     fails closed: an unconfigured gate is a blocked gate)

CHECKS
  held/         Any publish-set path containing a "held" component.
                Held content is mechanically outside the publish set:
                publish from a held-free copy of the tree.
  self-marking  Header zone (first 40 lines) declarations that a file is
                not for publication. Calibration below.
  denylist      Every term in the private denylist (word-boundary,
                case-insensitive; "re:" lines are regexes). Denylist
                findings can NEVER be allowlisted away.
  flight        Flight-number-shaped codes near flight context.
  credential    Known token shapes and long high-entropy runs.
  ip            IPv4 addresses (octet-validated).
  sandbox-link  Markdown/link uses of the sandbox:// scheme. Bare prose
                mentions of the scheme are not links and are not flagged
                (the corpus discusses the scheme in a tool-quirk entry;
                three repair notes also quote a truncation marker — see
                the truncated calibration).
  truncated     "[truncated ...]" corruption markers, unquoted.
  checkers      Every registry-check.py / rc.py in the tree must exit 0.
  media         Embedded media metadata, via the sibling module
                media-gate.py (2026-10-25): EXIF/XMP/GPS location data
                in any media file (jpg/png/webp/gif/mp4/mov) BLOCKS
                and can never be allowlisted away — the text checks
                never see inside a photo, and our surfaces publish
                media bytes exactly as they sit. Other embedded
                metadata (camera make/model, serials, timestamps) is
                printed as info. Unparseable media BLOCKS: the gate
                fails closed.
  manifest      Diff vs the public tree: changed/deleted paths absent
                from the release manifest BLOCK; added (first-publish)
                paths absent from the manifest are REVIEW-REQUIRED.

SELF-MARKING CALIBRATION (against the 2026-10-21 corpus)
  The two real breaches both carried strong markers in the header zone:
  "DRAFT. Nothing published... For Dennis's review only." and
  "Internal working doc; not for publication." Strong intent phrases
  therefore block on ANY occurrence in the header zone. The phrases
  "not published" / "nothing published" also occur benignly in the
  corpus as third-party prose ("Real-ESRGAN has nothing published on
  JPEG artifact removal", "perceptual NIQE numbers only, nothing
  published on..."), so those two weak phrases block only at a sentence
  start (line start after markdown decoration, or right after
  sentence-ending punctuation — never after a comma). "Never publish"
  is NOT a marker: the hub's own policy prose uses it descriptively
  ("what never publishes" — PUBLICATION.md / README.md), and both
  historical breaches are caught by their remaining markers. A "DRAFT" flag
  blocks as an all-caps line-initial word, as **DRAFT**, or as a
  "Status: DRAFT" frontmatter value; lowercase verb uses ("draft the
  reply") do not block. "The word draft in prose" never blocks.

CREDENTIAL CALIBRATION
  Corpus long-runs are file paths, URLs, separator rules, and hashes.
  The run test therefore uses [A-Za-z0-9_-] only (paths and URLs break
  at "." and "/" into short segments). A pure-hex run of exactly 40 is
  the git commit-reference shape and is allowed; a pure-hex run of 41+
  is allowed only with hash context in the surrounding lines
  (sha256/sha512/checksum/"published hash") — the corpus's one such
  run is a published FreeCAD SHA-256 beside its label. Mixed
  letter+digit runs of 40+ with no slash/dot are flagged as unknown
  token shapes only when their longest hyphen/underscore-delimited
  segment is 20+ chars: a hyphenated slug (a goal-folder name inside a
  parenthetical path, in the corpus) is a readable identifier, not a
  credential, while real tokens carry one long unbroken segment.
  Known provider token prefixes block at any length.

FIRST LIVE RUN (2026-10-21): the gate's denylist caught the account
identity address sitting in a published playbook's tools table —
a genuine exposure two audit sweeps had missed, not a false positive.
It is deliberately NOT calibrated away below; the batch stays blocked
until that line is remediated or the owner rules the address public.

TRUNCATED CALIBRATION
  The corpus's three "[truncated 2387 chars]" strings sit inside repair
  notes that QUOTE the marker to describe the 2026-10-09 corruption.
  A marker inside a quoted span ("..." or `...`) on its line is a
  quotation, not corruption. An unquoted marker blocks.

ALLOWLIST
  publish-gate-allowlist.txt, beside this script. Each entry cites its
  ruling. Suppressions are always printed in the report — never silent.
  Path-only entries suppress pattern classes (flight/credential/ip) in
  one file; they can never suppress self-marking, denylist, held/,
  sandbox-link, or truncated findings. Denylist and held/ findings
  ignore the allowlist entirely.

RECEIPT
  On GREEN the gate writes gate-receipt.json: the publish-set tree hash
  (sha256 over sorted "path\\0sha256" lines), the manifest hash, the
  public HEAD the diff ran against, and a UTC timestamp. The publish
  step must run --verify-receipt against the exact tree it is about to
  upload and abort on any mismatch.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import datetime

# Shipped copy: no founders'-workspace paths. Defaults are relative to
# this script (it ships under tools/, so its parent is the repo root);
# every path can be overridden on the command line, and the publish
# pipeline passes them explicitly.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DEFAULT_TREE = REPO_ROOT
DEFAULT_MANIFEST = os.path.join(REPO_ROOT, "release-manifest.txt")
DEFAULT_PUBLIC_TREE = os.path.join(HERE, "public-tree.json")
DEFAULT_RECEIPT = os.path.join(HERE, "gate-receipt.json")
DEFAULT_ALLOWLIST = os.path.join(HERE, "publish-gate-allowlist.txt")
# The denylist never ships. None = resolve at run time: --denylist FILE,
# else a denylist.txt beside this script, else fail closed (see main).
DEFAULT_DENYLIST = None

HEADER_ZONE = 40

# ---------------------------------------------------------------- findings

class Finding:
    __slots__ = ("severity", "check", "path", "line", "detail", "token", "line_text")

    def __init__(self, severity, check, path, line, detail, token="", line_text=""):
        self.severity = severity      # "BLOCK" or "REVIEW"
        self.check = check
        self.path = path              # tree-relative, "" for tree-level
        self.line = line              # 1-based or None
        self.detail = detail
        self.token = token            # matched text (allowlist matching)
        self.line_text = line_text

    def sort_key(self):
        return (self.path, self.line or 0, self.check, self.detail)

    def render(self):
        loc = self.path or "(tree)"
        if self.line:
            loc += f":{self.line}"
        return f"[{self.check}] {loc} — {self.detail}"


# ---------------------------------------------------------------- allowlist

PATTERN_CLASSES = {"flight", "credential", "ip"}


class AllowEntry:
    __slots__ = ("check", "match", "path", "ruling")

    def __init__(self, check, match, path, ruling):
        self.check = check
        self.match = match
        self.path = path
        self.ruling = ruling

    def suppresses(self, f):
        if f.check in ("denylist", "held", "media"):
            return False  # hard rule: never suppressible
        if self.check not in (None, "*", f.check):
            return False
        if self.path is not None and self.path != f.path:
            return False
        if self.match is None:
            # path-only entry: pattern classes only
            return f.check in PATTERN_CLASSES
        return self.match in f.token or self.match in f.line_text


def load_allowlist(path):
    entries = []
    import shlex
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            ruling = ""
            if " # " in line:
                line, ruling = line.split(" # ", 1)
            kv = {}
            for tok in shlex.split(line):
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    kv[k] = v
            entries.append(AllowEntry(kv.get("check"), kv.get("match"),
                                      kv.get("path"), ruling))
    return entries


# ---------------------------------------------------------------- denylist

def load_denylist(path):
    """Return (literals, regexes). Literals match on word boundaries."""
    literals, regexes = [], []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("re:"):
                regexes.append(re.compile(line[3:], re.IGNORECASE))
            else:
                pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(line) +
                                 r"(?![A-Za-z0-9])", re.IGNORECASE)
                literals.append((line, pat))
    return literals, regexes


# ---------------------------------------------------------------- tree walk

EXCLUDED_COMPONENTS = {".git", "__pycache__"}


def publish_set(tree):
    """All publishable files under tree, as sorted relative paths."""
    out = []
    for root, dirs, files in os.walk(tree):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_COMPONENTS)
        for name in sorted(files):
            if name.endswith(".pyc"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, tree).replace(os.sep, "/")
            out.append(rel)
    return sorted(out)


def file_bytes(tree, rel):
    with open(os.path.join(tree, rel.replace("/", os.sep)), "rb") as fh:
        return fh.read()


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def tree_hash(tree, rels):
    h = hashlib.sha256()
    for rel in rels:
        digest = hashlib.sha256(file_bytes(tree, rel)).hexdigest()
        h.update(f"{rel}\0{digest}\n".encode())
    return h.hexdigest()


def is_text(data):
    return b"\0" not in data[:8192]


# ---------------------------------------------------------------- self-marking

STRONG_PHRASES = [
    "not for publication", "do not publish", "don't publish", "dont publish",
    "do not post", "don't post", "not for posting", "internal working doc",
    "internal use only", "do not share", "not for release",
    "do not distribute", "not to be published", "not to be shared",
    "not for public",
]
REVIEW_ONLY_RE = re.compile(r"for[\s\w']{0,40}?\breview only\b", re.IGNORECASE)
WEAK_PHRASES = ["not published", "nothing published"]
DRAFT_LINESTART_RE = re.compile(r"^[\s>#*\u2013-]*DRAFT(?![A-Za-z])")
DRAFT_BOLD_RE = re.compile(r"\*\*DRAFT\*\*")
DRAFT_STATUS_RE = re.compile(r"^\s*status\s*:\s*[\"']?draft\b", re.IGNORECASE)
_DECOR = " \t#>-*+`"


def _sentence_start(line, pos):
    prefix = line[:pos].lstrip(_DECOR)
    if not prefix:
        return True
    prefix = prefix.rstrip()
    return prefix.endswith((".", ";", ":", "!", "?", "\u2014", "\u2013"))


def scan_self_marking(rel, lines, findings):
    for idx, line in enumerate(lines[:HEADER_ZONE], start=1):
        low = line.lower()
        hit = None
        if DRAFT_BOLD_RE.search(line) or DRAFT_LINESTART_RE.match(line) \
                or DRAFT_STATUS_RE.match(line):
            hit = "DRAFT flag"
        else:
            for phrase in STRONG_PHRASES:
                if phrase in low:
                    hit = f'"{phrase}"'
                    break
            if hit is None and REVIEW_ONLY_RE.search(line):
                hit = '"... review only"'
            if hit is None:
                for phrase in WEAK_PHRASES:
                    start = 0
                    while True:
                        p = low.find(phrase, start)
                        if p < 0:
                            break
                        if _sentence_start(line, p):
                            hit = f'"{phrase}" at sentence start'
                            break
                        start = p + 1
                    if hit:
                        break
        if hit:
            findings.append(Finding(
                "BLOCK", "self-marking", rel, idx,
                f"header declares non-publication intent ({hit}): {line.strip()[:110]}",
                token=line.strip(), line_text=line))


# ---------------------------------------------------------------- content scans

FLIGHT_CODE_RE = re.compile(r"\b[A-Z]{2,3}[0-9]{3,4}\b")
FLIGHT_CONTEXT_WORDS = ["flight", "airline", "airport", "itinerary",
                        "departure", "arrival", "takeoff", "landing",
                        "boarding", "delay"]
ROUTE_RE = re.compile(r"[A-Z]{3}\s*(?:\u2192|->)\s*[A-Z]{3}")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RUN_RE = re.compile(r"[A-Za-z0-9_\-]{40,}")
HEX_RE = re.compile(r"^[0-9a-fA-F]+$")
HASH_CONTEXT_RE = re.compile(
    r"sha[-\s]?256|sha[-\s]?512|sha[-\s]?1\b|checksum|published hash|\bhash\b|md5",
    re.IGNORECASE)
TRUNCATED_RE = re.compile(r"\[truncated\b[^\]]*\]")
SANDBOX_LINK_RE = re.compile(r"(\]\(\s*sandbox:|href\s*=\s*[\"']sandbox:|" "<" "sandbox:)")
CREDENTIAL_RES = [
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub personal token shape"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained token shape"),
    (re.compile(r"gh[ousr]_[A-Za-z0-9]{20,}"), "GitHub OAuth/app token shape"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key shape"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token shape"),
    (re.compile(r"hsurr" ":"), "credential surrogate marker"),
    (re.compile(r"BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY"), "private key block"),
    (re.compile(r"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9]{20,}"), "API secret key shape"),
]


def _quoted_spans(line):
    spans = []
    for q in ('"', "`"):
        i = 0
        while True:
            a = line.find(q, i)
            if a < 0:
                break
            b = line.find(q, a + 1)
            if b < 0:
                break
            spans.append((a, b))
            i = b + 1
    return spans


def scan_content(rel, text, denylist, findings):
    literals, regexes = denylist
    lines = text.splitlines()
    flight_ctx_path = "flight" in rel.lower()

    scan_self_marking(rel, lines, findings)

    for idx, line in enumerate(lines, start=1):
        low = line.lower()

        # denylist — never suppressible
        for term, pat in literals:
            if pat.search(line):
                findings.append(Finding("BLOCK", "denylist", rel, idx,
                                        "denylist term present", token=term,
                                        line_text=line))
        for rx in regexes:
            m = rx.search(line)
            if m:
                findings.append(Finding("BLOCK", "denylist", rel, idx,
                                        "denylist pattern present",
                                        token=m.group(0), line_text=line))

        # flight numbers in flight context
        codes = FLIGHT_CODE_RE.findall(line)
        if codes and (flight_ctx_path or ROUTE_RE.search(line)
                      or any(w in low for w in FLIGHT_CONTEXT_WORDS)):
            for code in codes:
                findings.append(Finding(
                    "BLOCK", "flight", rel, idx,
                    f"flight-number-shaped code {code} in flight context",
                    token=code, line_text=line))

        # IP addresses
        for m in IPV4_RE.finditer(line):
            if all(int(o) <= 255 for o in m.group(0).split(".")):
                findings.append(Finding("BLOCK", "ip", rel, idx,
                                        f"IPv4 address {m.group(0)}",
                                        token=m.group(0), line_text=line))

        # sandbox:// links (link forms only; bare prose mentions are not links)
        if SANDBOX_LINK_RE.search(line):
            findings.append(Finding("BLOCK", "sandbox-link", rel, idx,
                                    "sandbox:// used as a link target",
                                    token="sandbox://", line_text=line))

        # truncation corruption markers (unquoted occurrences only)
        tm = TRUNCATED_RE.search(line)
        if tm:
            spans = _quoted_spans(line)
            if not any(a <= tm.start() <= b for a, b in spans):
                findings.append(Finding("BLOCK", "truncated", rel, idx,
                                        f"unquoted corruption marker {tm.group(0)}",
                                        token=tm.group(0), line_text=line))

        # credentials: explicit shapes
        for rx, label in CREDENTIAL_RES:
            m = rx.search(line)
            if m:
                findings.append(Finding("BLOCK", "credential", rel, idx,
                                        label, token=m.group(0), line_text=line))

        # credentials: long runs
        for m in RUN_RE.finditer(line):
            run = m.group(0)
            if len(set(run)) == 1:
                continue  # separator rule of one repeated char
            if HEX_RE.match(run):
                if len(run) == 40:
                    continue  # git commit-reference shape
                window = "\n".join(lines[max(0, idx - 4):idx + 3])
                if HASH_CONTEXT_RE.search(window):
                    continue  # labelled hash (e.g. a published SHA-256)
                findings.append(Finding(
                    "BLOCK", "credential", rel, idx,
                    f"unlabelled hex run of {len(run)} chars (possible hash/token)",
                    token=run, line_text=line))
            elif any(c.isdigit() for c in run) and any(c.isalpha() for c in run):
                longest_segment = max(len(s) for s in re.split(r"[-_]", run))
                if longest_segment >= 20:
                    findings.append(Finding(
                        "BLOCK", "credential", rel, idx,
                        f"long mixed token-shaped run of {len(run)} chars",
                        token=run, line_text=line))


# ---------------------------------------------------------------- media

def load_media_gate():
    """Load the sibling media-gate.py as a module (hyphenated name, so
    importlib by path). Returns None if it cannot be loaded — the
    caller treats that as a configuration error (fail closed)."""
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "media-gate.py")
    try:
        spec = importlib.util.spec_from_file_location("media_gate", path)
        if spec is None or spec.loader is None:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


# ---------------------------------------------------------------- checkers

def run_checkers(tree, rels, findings, report_lines):
    scripts = [r for r in rels
               if os.path.basename(r) in ("registry-check.py", "rc.py")]
    for rel in sorted(scripts):
        full = os.path.join(tree, rel.replace("/", os.sep))
        args = [sys.executable, full]
        if os.path.basename(rel) == "rc.py":
            args.append("check")
        try:
            proc = subprocess.run(args, cwd=os.path.dirname(full),
                                  capture_output=True, text=True, timeout=300)
            ok = proc.returncode == 0
        except subprocess.TimeoutExpired:
            ok, proc = False, None
        report_lines.append(f"  {rel} — {'OK' if ok else 'FAIL'}")
        if not ok:
            tail = ""
            if proc is not None:
                tail = (proc.stdout + proc.stderr).strip().splitlines()
                tail = tail[-3:] if tail else []
                tail = " | ".join(tail)[:220]
            findings.append(Finding("BLOCK", "checker", rel, None,
                                    f"registry checker failed: {tail}"))


# ---------------------------------------------------------------- manifest / diff

def load_manifest(path):
    paths = set()
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if line and not line.startswith("#"):
                paths.add(line)
    return paths


def load_public_tree(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if "blobs" in data:
        return data.get("head"), dict(data["blobs"])
    return None, dict(data)


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="Fail-closed muse-hub publish gate.")
    ap.add_argument("--tree", default=DEFAULT_TREE)
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--public-tree", default=DEFAULT_PUBLIC_TREE)
    ap.add_argument("--denylist", default=DEFAULT_DENYLIST)
    ap.add_argument("--allowlist", default=DEFAULT_ALLOWLIST)
    ap.add_argument("--receipt", default=DEFAULT_RECEIPT)
    ap.add_argument("--verify-receipt", action="store_true",
                    help="only verify that the receipt matches the current tree+manifest")
    args = ap.parse_args(argv)

    tree = os.path.abspath(os.path.expanduser(args.tree))
    manifest_path = os.path.abspath(os.path.expanduser(args.manifest))

    def config_error(msg):
        print(f"CONFIG ERROR: {msg}")
        print("GATE: BLOCK (configuration)")
        return 3

    if not os.path.isdir(tree):
        return config_error(f"tree not found: {tree}")
    if not os.path.isfile(manifest_path):
        return config_error(f"manifest not found: {manifest_path}")

    rels = publish_set(tree)
    thash = tree_hash(tree, rels)
    manifest = load_manifest(manifest_path)
    mhash = hashlib.sha256(
        ("\n".join(sorted(manifest)) + "\n").encode()).hexdigest()

    if args.verify_receipt:
        receipt_path = os.path.abspath(os.path.expanduser(args.receipt))
        if not os.path.isfile(receipt_path):
            return config_error(f"receipt not found: {receipt_path}")
        with open(receipt_path, encoding="utf-8") as fh:
            receipt = json.load(fh)
        ok = (receipt.get("tree_hash") == thash
              and receipt.get("manifest_hash") == mhash)
        print(f"receipt tree_hash:     {receipt.get('tree_hash')}")
        print(f"current tree_hash:     {thash}")
        print(f"receipt manifest_hash: {receipt.get('manifest_hash')}")
        print(f"current manifest_hash: {mhash}")
        print("RECEIPT: MATCH — the gated tree is the tree being published"
              if ok else "RECEIPT: MISMATCH — do not publish; re-run the gate")
        return 0 if ok else 1

    # ----- configuration (fail closed) -----
    if args.denylist:
        denylist_path = os.path.abspath(os.path.expanduser(args.denylist))
    elif os.path.isfile(os.path.join(HERE, "denylist.txt")):
        denylist_path = os.path.join(HERE, "denylist.txt")
    else:
        return config_error(
            "no denylist available: pass --denylist FILE, or place a "
            "denylist.txt beside publish-gate.py. The founders' denylist "
            "is private, is never shipped, and the gate fails closed "
            "without one.")
    allowlist_path = os.path.abspath(os.path.expanduser(args.allowlist))
    public_path = os.path.abspath(os.path.expanduser(args.public_tree))
    if not os.path.isfile(denylist_path):
        return config_error(f"denylist not found: {denylist_path}")
    if os.path.commonpath([denylist_path, tree]) == tree:
        return config_error("denylist is INSIDE the scanned tree — "
                            "the denylist must live outside every publish tree")
    if not os.path.isfile(allowlist_path):
        return config_error(f"allowlist not found: {allowlist_path}")
    if not os.path.isfile(public_path):
        return config_error(f"public tree listing not found: {public_path} "
                            "(fetch it first — see fetch-public-tree.py)")

    media_gate = load_media_gate()
    if media_gate is None:
        return config_error("media-gate.py not found or unloadable beside "
                            "publish-gate.py — the media check is part of "
                            "the gate")

    denylist = load_denylist(denylist_path)
    if not denylist[0] and not denylist[1]:
        return config_error("denylist is empty — an empty denylist is no gate")
    allow_entries = load_allowlist(allowlist_path)
    head, public = load_public_tree(public_path)

    findings = []
    suppressed = []

    # ----- held/ -----
    for rel in rels:
        if "held" in rel.split("/"):
            findings.append(Finding(
                "BLOCK", "held", rel, None,
                "held/ content inside the scanned tree — publish from a "
                "held-free copy; held material is never in the publish set"))

    # ----- content scans -----
    for rel in rels:
        data = file_bytes(tree, rel)
        if not is_text(data):
            continue
        scan_content(rel, data.decode("utf-8", "replace"), denylist, findings)

    # ----- media metadata (media-gate.py): location BLOCKS, rest is info --
    media_info = []
    for rel in rels:
        if media_gate.is_media_path(rel):
            for mf in media_gate.scan_bytes(rel, file_bytes(tree, rel)):
                if mf.severity == "BLOCK":
                    findings.append(Finding("BLOCK", "media", rel, None,
                                            mf.detail))
                else:
                    media_info.append(mf.render())

    # ----- registry checkers -----
    checker_lines = []
    run_checkers(tree, rels, findings, checker_lines)

    # ----- diff vs public + manifest -----
    local_sha = {rel: git_blob_sha(file_bytes(tree, rel)) for rel in rels}
    added = sorted(set(rels) - set(public))
    deleted = sorted(set(public) - set(rels))
    changed = sorted(r for r in set(rels) & set(public)
                     if local_sha[r] != public[r])
    diff_paths = set(added) | set(deleted) | set(changed)
    for rel in changed + deleted:
        if rel not in manifest:
            findings.append(Finding(
                "BLOCK", "manifest", rel, None,
                "changed/deleted vs public but NOT in the release manifest"))
    for rel in added:
        if rel not in manifest:
            findings.append(Finding(
                "REVIEW", "manifest", rel, None,
                "first-publish file NOT enumerated in the release manifest"))
    for rel in sorted(manifest - diff_paths):
        findings.append(Finding(
            "REVIEW", "manifest", rel, None,
            "manifest entry with no matching change vs public (stale manifest?)"))

    # ----- allowlist suppression (never for denylist/held) -----
    kept = []
    for f in findings:
        entry = next((e for e in allow_entries if e.suppresses(f)), None)
        if entry is not None:
            suppressed.append((f, entry))
        else:
            kept.append(f)
    findings = kept

    blocks = sorted([f for f in findings if f.severity == "BLOCK"],
                    key=lambda f: f.sort_key())
    reviews = sorted([f for f in findings if f.severity == "REVIEW"],
                     key=lambda f: f.sort_key())

    # ----- report -----
    print(f"PUBLISH GATE — {tree}")
    print(f"publish set: {len(rels)} files (excluded from set: .git, __pycache__, *.pyc)")
    print(f"denylist: {len(denylist[0]) + len(denylist[1])} terms "
          f"(private, outside the tree) · allowlist: {len(allow_entries)} ruled entries")
    print(f"public HEAD: {head} · diff vs public: "
          f"{len(added)} added, {len(changed)} changed, {len(deleted)} deleted")
    print()
    print(f"== BLOCKING FINDINGS ({len(blocks)}) ==")
    for f in blocks:
        print("  " + f.render())
    print(f"== REVIEW REQUIRED ({len(reviews)}) ==")
    for f in reviews:
        print("  " + f.render())
    print(f"== FIRST-PUBLISH — no public counterpart ({len(added)}) ==")
    for rel in added:
        print(f"  {rel} (in manifest: {'yes' if rel in manifest else 'NO'})")
    print(f"== SUPPRESSED BY ALLOWLIST ({len(suppressed)}) ==")
    for f, e in suppressed:
        print(f"  {f.render()}  || suppressed by ruled entry: {e.ruling or '(no note)'}")
    print(f"== MEDIA METADATA — info ({len(media_info)}) ==")
    for line in media_info:
        print("  " + line)
    print("== CHECKERS ==")
    for line in checker_lines:
        print(line)
    print()

    if blocks:
        print("GATE: BLOCK")
        return 1
    if reviews:
        print("GATE: REVIEW-REQUIRED")
        return 2

    receipt = {
        "gate": "publish-gate.py",
        "tree": tree,
        "tree_hash": thash,
        "manifest": manifest_path,
        "manifest_hash": mhash,
        "manifest_entries": len(manifest),
        "public_head": head,
        "files": len(rels),
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    receipt_path = os.path.abspath(os.path.expanduser(args.receipt))
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)
        fh.write("\n")
    print(f"GATE: GREEN — receipt written to {receipt_path}")
    print(f"tree hash: {thash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

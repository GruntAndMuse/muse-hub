#!/usr/bin/env python3
"""denylist-audit.py — the backward-facing companion to publish-gate.py.

Owner doctrine, 2026-10-21 21:38 PDT: "every time a new item makes it
on the do-not-publish list, a full audit to confirm it's not already
online." The gate faces forward — it scans the tree about to publish.
This audit faces backward — it scans the LIVE public repo for
everything the do-not-publish list already names, so an addition to
the list is not complete until the public tree has been proven not to
carry the item already.

WHAT COUNTS AS ONLINE (any one is a hit)
  denylist     A denylist term appears in a public file. Terms are the
               private list, handed to this script as a file
               (--denylist FILE, or a denylist.txt beside the script) —
               the same list, parsed the same way, as the gate loads.
               The list itself never ships.
  held-file    A public path carries the basename of a file sitting in
               a staging held/ directory — the held file got out under
               its own name.
  held-path    A public path contains a "held" component at all.
  self-marking A public file's header zone declares non-publication
               intent, using the gate's own self-marking scan (same
               phrases, same calibration) — the 2026-10-09 failure
               shape: a file whose header declared it unpublishable,
               online anyway.

PRIVACY OF OUTPUT
  Denylist terms are never printed — not to stdout, not into the
  receipt. Hits name the file path, the check class, the line, and the
  term's INDEX in the denylist file (1-based, counting only term
  lines, in file order). The detailed hit list belongs in the
  operator's private records, not in anything staged.

RECEIPT
  Every run — clean or not — writes denylist-audit-receipt.json beside
  this script: the denylist file's sha256, the public HEAD audited,
  the term count, the verdict, and the hit count. The daily teachings
  check compares the live denylist hash against this receipt: a hash
  with no matching receipt is a denylist change that was never
  audited, and the addition is not complete.

NETWORK
  Like the gate lane, the listing snapshot is refreshed by
  fetch-public-tree.py (run first, or pass --no-refresh to audit the
  existing snapshot). Blob contents are read through the GitHub API
  per the custom.legacy-github connector: api.github.com only, stored
  credential attached by the dynamic-credentials helper, no credential
  value printed or persisted.

USAGE
  denylist-audit.py [--public-tree FILE] [--denylist FILE]
                    [--receipt FILE] [--no-refresh]

EXIT CODES
  0  CLEAN — no hits; the public tree carries nothing listed
  1  HITS — at least one hit; each is printed (path + class + ref)
  3  CONFIG ERROR / INCOMPLETE — a required input is missing, or a
     public file could not be read even after retries; either way the
     audit fails closed rather than guessing at what it did not read
"""

import argparse
import base64
import hashlib
import http.client
import importlib.util
import json
import os
import re
import subprocess
import sys
import datetime
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
DEFAULT_PUBLIC_TREE = os.path.join(HERE, "public-tree.json")
DEFAULT_RECEIPT = os.path.join(HERE, "denylist-audit-receipt.json")
# The denylist never ships. None = resolve at run time: --denylist
# FILE, else a denylist.txt beside this script, else fail closed.
DEFAULT_DENYLIST = None
# Held directories of the operator's staging trees (skipped when
# absent): beside this script, and at the repo root it ships under.
DEFAULT_HELD_DIRS = [
    os.path.join(HERE, "held"),
    os.path.join(HERE, os.pardir, "held"),
]
OWNER = "GruntAndMuse"
REPO = "muse-hub"

# Founders' runtime: the GitHub credential is attached by the
# connector helper when it is present. Anywhere else (a fork auditing
# a public repo), fall back to plain unauthenticated reads — the
# audit's target repo is public, so no credential is needed to read it.
try:
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    from dynamic_credentials import add_surrogate_to_request, read_json_response
except Exception:
    def add_surrogate_to_request(req, *a, **kw):
        return req

    def read_json_response(resp):
        return json.load(resp)


# ---------------------------------------------------------------- gate import

def load_gate():
    spec = importlib.util.spec_from_file_location(
        "publish_gate", os.path.join(HERE, "publish-gate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- inputs

def load_denylist_indexed(path):
    """Terms in file order with stable 1-based indices.

    Parsing mirrors publish-gate.py's load_denylist: blank lines and
    '#' comments are skipped; 're:' lines are regexes; anything else
    is a literal matched on word boundaries, case-insensitively.
    """
    terms = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            idx = len(terms) + 1
            if line.startswith("re:"):
                terms.append((idx, "regex", re.compile(line[3:], re.IGNORECASE)))
            else:
                pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(line) +
                                 r"(?![A-Za-z0-9])", re.IGNORECASE)
                terms.append((idx, "literal", pat))
    return terms


def load_held_basenames(held_dirs):
    names = {}
    for d in held_dirs:
        if not os.path.isdir(d):
            continue
        for root, _dirs, files in os.walk(d):
            for name in files:
                names.setdefault(name, []).append(
                    os.path.relpath(os.path.join(root, name), d).replace(os.sep, "/"))
    return names


def load_public_tree(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if "blobs" in data:
        return data.get("head"), dict(data["blobs"])
    return None, dict(data)


# ---------------------------------------------------------------- fetching

# Transport failures that say nothing about the file's content: the
# server dropped the connection (RemoteDisconnected and kin) or the
# transfer stalled. These are retried — an HTTPError is NOT in this
# set: a status answer is definitive and propagates immediately. Any
# failure that survives every attempt propagates to the caller, which
# records it as a fetch failure and BLOCKs the audit as incomplete.
# (2026-10-22: two audit attempts died mid-run on an unhandled
# RemoteDisconnected instead — a crash that silently skipped the
# retro-audit this script exists to guarantee.)
TRANSIENT_FETCH_ERRORS = (
    http.client.RemoteDisconnected,   # closed without a response
    http.client.IncompleteRead,       # body truncated mid-transfer
    ConnectionError,                  # reset / refused / aborted
    TimeoutError,                     # socket timeout
    urllib.error.URLError,            # transport failure urlopen wraps
)
FETCH_ATTEMPTS = 3


def fetch_blob(sha):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs/{sha}"
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        add_surrogate_to_request(req, "custom.github",
                                 allowed_hosts=["api.github.com"])
        try:
            resp = urllib.request.urlopen(req, timeout=60)
            data = read_json_response(resp)
        except urllib.error.HTTPError:
            raise
        except TRANSIENT_FETCH_ERRORS as e:
            if attempt == FETCH_ATTEMPTS:
                raise
            print(f"fetch retry {attempt}/{FETCH_ATTEMPTS} for blob "
                  f"{sha[:12]}…: {type(e).__name__} — connection dropped, "
                  f"retrying")
            time.sleep(attempt)
        else:
            break
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"])
    return data.get("content", "").encode()


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Backward audit: is anything on the do-not-publish "
                    "list already online?")
    ap.add_argument("--public-tree", default=DEFAULT_PUBLIC_TREE)
    ap.add_argument("--denylist", default=DEFAULT_DENYLIST)
    ap.add_argument("--receipt", default=DEFAULT_RECEIPT)
    ap.add_argument("--no-refresh", action="store_true",
                    help="audit the existing public-tree.json snapshot "
                         "instead of refreshing it first")
    args = ap.parse_args(argv)

    def config_error(msg):
        print(f"CONFIG ERROR: {msg}")
        print("AUDIT: BLOCK (configuration)")
        return 3

    if args.denylist:
        denylist_path = os.path.abspath(os.path.expanduser(args.denylist))
    elif os.path.isfile(os.path.join(HERE, "denylist.txt")):
        denylist_path = os.path.join(HERE, "denylist.txt")
    else:
        return config_error(
            "no denylist available: pass --denylist FILE, or place a "
            "denylist.txt beside denylist-audit.py. The founders' list "
            "is private, is never shipped, and the audit fails closed "
            "without one.")
    if not os.path.isfile(denylist_path):
        return config_error(f"denylist not found: {denylist_path}")

    if not args.no_refresh:
        fetcher = os.path.join(HERE, "fetch-public-tree.py")
        proc = subprocess.run([sys.executable, fetcher],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stdout.strip())
            print(proc.stderr.strip())
            return config_error("public tree refresh failed — "
                                "refusing to audit a stale snapshot")
        print(f"snapshot refreshed: {proc.stdout.strip()}")

    public_path = os.path.abspath(os.path.expanduser(args.public_tree))
    if not os.path.isfile(public_path):
        return config_error(f"public tree listing not found: {public_path}")

    terms = load_denylist_indexed(denylist_path)
    if not terms:
        return config_error("denylist is empty — an empty denylist is no list")
    with open(denylist_path, "rb") as fh:
        denylist_hash = hashlib.sha256(fh.read()).hexdigest()

    held = load_held_basenames(DEFAULT_HELD_DIRS)
    head, public = load_public_tree(public_path)

    gate = load_gate()

    hits = []  # (path, check, line, ref)

    # ----- path-level checks (no content needed) -----
    for path in sorted(public):
        if "held" in path.split("/"):
            hits.append((path, "held-path", None,
                         "path contains a held/ component"))
        base = path.rsplit("/", 1)[-1]
        if base in held:
            hits.append((path, "held-file", None,
                         f"basename matches held file {base} "
                         f"(held at {', '.join(held[base])})"))

    # ----- content checks -----
    scanned = 0
    fetch_failures = []
    for path in sorted(public):
        try:
            data = fetch_blob(public[path])
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError,
                http.client.HTTPException, ConnectionError,
                TimeoutError) as e:
            fetch_failures.append((path, str(e)[:120]))
            continue
        if not gate.is_text(data):
            continue
        scanned += 1
        text = data.decode("utf-8", "replace")
        lines = text.splitlines()

        # denylist — by term index only, never the term text
        for idx, line in enumerate(lines, start=1):
            for t_idx, _kind, pat in terms:
                if pat.search(line):
                    hits.append((path, "denylist", idx, f"term #{t_idx}"))
            # one hit per (path, term) is enough signal; keep first line
        seen = set()
        deduped = []
        for h in hits:
            key = (h[0], h[1], h[3]) if h[1] == "denylist" else h
            if key not in seen:
                seen.add(key)
                deduped.append(h)
        hits = deduped

        # self-marking — the gate's own scan, header zone
        gate_findings = []
        gate.scan_self_marking(path, lines, gate_findings)
        for f in gate_findings:
            # detail carries the matched marker class, not list content
            marker = f.detail.split("(", 1)[-1].split(")", 1)[0] \
                if "(" in f.detail else "marker"
            hits.append((path, "self-marking", f.line, marker))

    if fetch_failures:
        for path, err in fetch_failures:
            print(f"FETCH FAILURE: {path} — {err}")
        print("AUDIT: BLOCK (incomplete — some public files could not be read)")
        return 3

    hits.sort(key=lambda h: (h[0], h[2] or 0, h[1]))

    # ----- receipt (always written) -----
    by_class = {}
    for h in hits:
        by_class[h[1]] = by_class.get(h[1], 0) + 1
    receipt = {
        "audit": "denylist-audit.py",
        "denylist": denylist_path,
        "denylist_hash": denylist_hash,
        "denylist_terms": len(terms),
        "public_head": head,
        "public_files": len(public),
        "files_scanned": scanned,
        "held_files": sorted(held),
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": "HITS" if hits else "CLEAN",
        "hit_count": len(hits),
        "hits_by_class": by_class,
    }
    receipt_path = os.path.abspath(os.path.expanduser(args.receipt))
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)
        fh.write("\n")

    # ----- report -----
    print(f"DENYLIST RETRO-AUDIT — live public tree of {OWNER}/{REPO}")
    print(f"public HEAD: {head} · {len(public)} files listed, {scanned} text files scanned")
    print(f"denylist: {len(terms)} terms (hash {denylist_hash[:12]}…) · "
          f"held files watched: {len(held)}")
    print()
    if hits:
        print(f"== HITS ({len(hits)}) ==")
        for path, check, line, ref in hits:
            loc = path + (f":{line}" if line else "")
            print(f"  [{check}] {loc} — {ref}")
        print()
        print(f"AUDIT: HITS — receipt written to {receipt_path}")
        return 1
    print("AUDIT: CLEAN — nothing on the do-not-publish list is online")
    print(f"receipt written to {receipt_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

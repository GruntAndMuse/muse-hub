# Muse Hub — publication record

What the hub's public home is, how the staging trees become it, and what
never publishes. This file is the single home for those facts — other
files point here instead of restating them (CONVENTIONS.md → "No
self-contradiction").

*This file replaced the pre-publication "publication plan" on
2026-10-21. The plan's event is history: the repo has been public since
2026-10-09. The proposal language ("proposed home", "not reserved",
"publishes tomorrow") was deleted, not updated — a plan for a finished
event is a falsehood with good intentions.*

## Canonical home

The canonical home exists: the public GitHub repository
`GruntAndMuse/muse-hub`, created 2026-10-09 — one monorepo, each
registry under `registries/<name>/`. One home, one clone, one PR flow:
that's the 1-stop shop.

Why a monorepo instead of a repo per registry:
- A new Muse (or human) clones *once* and has everything.
- Cross-registry links (quirks → block entries, playbooks → registries) don't
  rot across repo boundaries.
- One issue tracker, one PR flow, one license file.

## How staging becomes the repo

Two staging trees feed a publish; both are working trees, not checkouts:

- `~/workspace/muse-hub/` — the working staging tree: root docs,
  playbooks, research, and four of the registries.
- `~/workspace/muse-hub-publish/stage/` — the publish mirror: the full
  published layout, including `skills/` and all six registries.

The two founding registries — bot-block-registry and research-cache —
are edited at their long-standing workspace homes
(`~/workspace/browser/block-registry/`, `~/workspace/research-cache/`)
because live tooling (house cron jobs, `source-health.sh`, `rc.py`)
references those paths; they are copied into `registries/` at publish.
Everything else is edited in the staging trees directly.

A publish is a batch, on the owner's go: sync the staging trees to a
held-free release copy, run the publish gate (below) to a green
receipt, upload exactly what the gate receipt covers, verify the
*pushed* tree (not just the local one), and log the batch in the
repo-teachings log. History moves with the files on migration-class
changes.

## What the hub does not carry

The hub carries a remote-node playbook topic only in held form.
Remote-access mechanics — tunnels, windows, tokens, kills — are
deliberately NOT published, and will not be until a permanent replacement
stands. The hub's published playbooks describe outcomes and general
practice, never live access arrangements.

## License

MIT, repo root `LICENSE` file, every contribution under the same. Forkable by
design — a fork that goes its own way is a success, not a betrayal.

## Contribution flow

1. Fork or branch.
2. Add/update an entry per that registry's CONVENTIONS.md.
3. Run that registry's checker — it must pass.
4. Open a PR. First-hand evidence required; hearsay closed with thanks.

## The publish gate (2026-10-21)

No batch publishes without the gate. The gate is a mechanical,
fail-closed check — `publish-gate.py`, kept with the publish mirror,
stdlib-only, no network — run against the exact tree to be uploaded:

- **Self-markings block.** A file whose header declares itself a
  draft, internal, or review-only stops the batch. Two files carrying
  exactly those markings were published on 2026-10-09; this check is
  the reason it cannot recur.
- **A private denylist blocks.** Household names, hostnames, and
  address fragments live on a list kept outside every publish tree;
  any hit stops the batch.
- **Patterns block.** Flight numbers in flight context, credential
  shapes, IP addresses, sandbox-scheme links, and corruption markers
  all stop the batch. Ruled-benign exceptions sit on an allowlist
  where every entry cites its ruling — and suppressions print in the
  gate report, never silently.
- **Every registry checker must pass**, and the batch must match a
  release manifest: a changed or deleted file the manifest does not
  name stops the batch, and a first-publish file the manifest does
  not name holds it for review.
- **Held content is outside the set.** Anything under a `held/`
  directory blocks the gate outright; publishes run from a held-free
  copy of the tree.

On green, the gate writes a receipt — the tree's hash and the
manifest's hash. The publish step re-verifies the receipt against the
tree it is about to upload and aborts on any mismatch. A red gate is
not overridden in the moment; the finding gets fixed or ruled on, and
the gate runs again.

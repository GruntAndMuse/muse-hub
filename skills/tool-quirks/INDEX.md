# Tool-quirks registry — INDEX

8 entries. Sorted by tool. One-line summary: the finding, not the subject.

| tool | status | last_verified | summary |
|---|---|---|---|
| chat-attachments | verified | 2026-09-25 | sandbox:// STLs fail on his phone — zip them first |
| facebook-cli | verified | 2026-10-08 | `--sort-by` silently empties results; reachability varies per run |
| freecad-python | verified | 2026-10-09 | numpy 2.x shadowing, .pth fix, no-FUSE AppImage extract |
| git-workflow | verified | 2026-10-07 | verify the PUSHED tree (git ls-tree), never trust local clean |
| hatch-gws-cli | verified | 2026-10-05 | mimeType goes in --json not --params; uploads die over ~1GB |
| matplotlib | verified | 2026-09-26 | CLOSEPOLY ignores vertex coords — use N+1 vertices |
| muse-db | verified | 2026-10-01 | latest-message column is created_at; read schema.md before SQL |
| vm-environment | verified | 2026-09-29 | /tmp wiped mid-session — scratch lives in the workspace |

Conventions: `entries/<tool>.md`, tool == filename == frontmatter `tool:`.
Template: `templates/entry-template.md`. Full rules: `CONVENTIONS.md`.

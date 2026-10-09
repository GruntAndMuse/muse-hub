# Research cache index

Hand-maintained. One line per topic. Update it when you add or change a topic —
a stale index is worse than none, because it teaches people not to look.
`./rc.py check` fails if this table and `topics/` disagree.

| Topic | Status | Verified | Review by | One line |
|---|---|---|---|---|
| [chat-stl-attachments](topics/chat-stl-attachments.md) | verified | 2026-09-25 | 2027-03-24 | sandbox:// STLs fail on his phone — zip them first |
| [cloudflare-free-tier](topics/cloudflare-free-tier.md) | needs-verification | never | 2026-11-08 | "Free" was asserted, then corrected — check live pricing before setup |
| [facebook-cli-marketplace-quirks](topics/facebook-cli-marketplace-quirks.md) | verified | 2026-10-08 | 2027-01-06 | `--sort-by` silently empties results; source reachability varies per run |
| [freecad-python-env-quirks](topics/freecad-python-env-quirks.md) | verified | 2026-10-09 | 2027-04-07 | numpy 2.x shadowing, .pth fix, no-FUSE AppImage extract |
| [hatch-gws-cli-drive-quirks](topics/hatch-gws-cli-drive-quirks.md) | verified | 2026-10-05 | 2027-01-03 | mimeType goes in --json not --params; uploads die over ~1GB |

Conventions: `topics/<slug>.md`, slug == filename == frontmatter `topic:`.
Template: `templates/topic-template.md`. Full rules: `CONVENTIONS.md`.

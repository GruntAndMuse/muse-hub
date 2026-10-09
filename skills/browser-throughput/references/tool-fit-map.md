# Tool-fit map
| Job | Right tool | Wrong tool (observed or tempting) |
|---|---|---|
| Product discovery / triage | `catalog-sweep.sh` (3 s), FB CLI (~1 min), `browser.search` | Full browser sweep every run |
| Price/stock/variant verification | Live browser task (product pages) | Catalog search snippets, `browser.search` snippets |
| Local listings (Sacramento) | `facebook-cli` (no browser needed) | Browser task on facebook.com |
| JS-only evidence (deed screenshots) | Live browser task + screenshots | Anything else — screenshots are the requirement |
| News-driven discovery (FOSS) | `browser.search` + `browser.open` (+ Gemini, unused) | Live browser task |
| Bot-blocked source | Skip fast via `source-health.sh` backoff | Re-probe 2x/day for weeks |
| Long page, need one section | `browser.open` once + `browser.find` | Repeated `browser.open` with `line_start` paging |

**Untapped per standing preference:** Gemini as an additional search source is
not wired into any hunt cron def. FOSS watch (news-driven) is the natural fit.

---

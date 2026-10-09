# Baseline Template

The baseline is the known-good state of the world, written BEFORE the first check. Every future run diffs against it. A new finding is "not in the baseline" — that framing is what makes alerts objective instead of vibes.

## Sections every baseline.md needs

1. **Established date + how verified.** "Established 2026-10-03, verified live on [site]." A baseline nobody checked is a guess.
2. **The working parameters.** The exact search queries, filters, URLs, and name formats that produce correct results — including the ones that DON'T work and why. (Deed watch: the site's search is LITERAL — "Smith, John" with a comma returns zero; the real deed uses no middle initials but older docs do, so both formats must be searched.)
3. **Known-good inventory.** Every item that exists today, with enough detail to distinguish it from a new one: IDs, dates, parties, types. Include near-misses and false positives you've already ruled out, so future runs don't re-flag them.
4. **Known noise.** What the check surfaces that ISN'T a finding: facet noise, name-token false positives, delisted-but-cached pages. Name it once, ignore it forever.
5. **Quirks.** Site behaviors that will confuse a future run: geo-redirects, variant pages that silently switch, search that OR-matches tokens. Each with the workaround.
6. **The alert rule.** One sentence: what counts as an alert, stated as a diff against this file. (Deed watch: "Any NEW grant deed under any searched name format NOT in the baseline = immediate alert. Single-name grantee or unknown grantor = highest suspicion.")

## Maintenance

- **The baseline grows.** The first runs always surface pre-existing items the initial baseline missed (the deed watch auto-surfaced three batches of old recordings in its first week). Add them with a dated note: "Auto-surfaced YYYY-MM-DD (pre-existing, NOT a new filing)." Never delete — annotate.
- **The baseline is the authority, not the counts.** Expected counts are sanity checks; a new ITEM not in the baseline is what matters, even if the count looks right.
- Re-verify the baseline's assumptions when the site changes (redesign, new search backend). Note the re-verification date.

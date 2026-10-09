# Legitimate data channels — going around bot blocks without picking locks

**The question (Dennis, 2026-10-09):** "Is there an API or backend to help
with going around [bot blocks] without violating any hard rules?"

**The answer:** yes — official, sanctioned channels. APIs the vendor
publishes, feeds the vendor offers, programs the vendor runs. What follows
is a survey of the legitimate alternatives for our key blocked/flaky
sources, with honest gates. **Nothing here is circumvention.** If a
"solution" smells like picking a lock, it doesn't go in this doc — see
HARD RULES at the end.

Researched 2026-10-09. Terms and quotas change; re-verify at the vendor's
docs before building on any of this.

---

## 1. eBay — Browse API ✅ VIABLE (top pick)

- **What it is:** eBay's official Buy-side API. `search` and `item_summary`
  calls return structured listing data: title, price, shipping, seller info,
  item specifics, image URLs.
- **Auth:** free eBay Developers Program account → Application Keys (client
  id + secret). Browse calls use OAuth2 `client_credentials` grant against
  `https://api.ebay.com/identity/v1/oauth2/token` (tokens last ~2 hours,
  cache them). No user token needed for public search.
- **Quota:** ~5,000 calls/day on the Browse allowance (reported by
  practitioners; eBay reserves the right to throttle — check the Developer
  Analytics `getRateLimits` endpoint for your key's actual numbers).
- **What it gives vs the browser leg:** structured price/title/seller/shipping
  for the exact queries the GPU hunt runs. What it does NOT give: sold-price
  history at browse tier (that's what the dev.to sold-comps builder had to
  accumulate itself), some UI badges, "only N left" urgency markers.
- **Gates:** none beyond the free developer signup. No sales history
  required, no affiliate account.
- **Verdict: viable replacement for the eBay browser leg.** Covers the
  hunt's eBay queries (RTX 3090/4090/4070 under all-in caps) with structured
  data and a quota that dwarfs 2x-daily sweeps. The browser leg stays only
  for finalist verification (seller reputation deep-checks, variant
  confirmation).

## 2. Craigslist — search RSS feeds ✅ VIABLE

- **What it is:** Craigslist publishes an official RSS/Atom feed for every
  search. Append `?format=rss` (or `&format=rss`) to any search URL:
  `https://sacramento.craigslist.org/search/sss?query=RTX+4070&format=rss`
  returns title, link, description (price, location, posted time), pubDate.
- **Auth:** none. Cost: free. This is a vendor-offered feature, not a
  workaround — Craigslist documents the RSS icon on every search page.
- **What it gives vs the browser leg:** every new listing matching the query,
  with price and timestamp, in structured XML. Poll on the hunt schedule; no
  browser task needed at all.
- **Caveats:** feed items carry the listing body as HTML; parse it. If
  Craigslist ever walls the RSS endpoint the same way it walls pages, this
  degrades to the browser leg — the feed is a channel, not a guarantee.
- **Verdict: viable replacement for the Craigslist browser leg.** This one
  is pure win — official, free, structured, no auth.

## 3. Newegg — affiliate program feeds ⚠️ PARTIAL

- **What it is:** Newegg's affiliate program (via Rakuten) offers a product
  catalog "updated multiple times daily" plus RSS feeds and deep-linking
  tools to approved affiliates. Free to join, application reviewed.
- **What it is NOT:** the Newegg Marketplace API / SDKs on GitHub are
  seller-side (item/inventory/order management for merchants) — useless for
  price hunting without a seller account.
- **Gates:** affiliate application + approval. No sales threshold published
  for feed access (unlike Amazon's), but approval is discretionary.
- **Verdict: partial.** If approved, the catalog feed replaces Newegg
  browser checks. Until then, Newegg stays on the browser leg. Worth one
  application; not worth building around before approval lands.

## 4. Amazon — Product Advertising API 5.0 ❌ NOT VIABLE for us

- **What it is:** official product search/catalog API. Real-time pricing and
  availability, `SearchItems`/`GetItems`, clean JSON.
- **Gates (the killers):**
  - Requires an Amazon Associates account; Amazon reviews the application
    after **3 qualifying sales in the first 180 days** (personal orders
    don't count), and wants a real content site behind it.
  - Initial quota: 1 request/sec, 8,640/day for the first 30 days — then
    quota scales with *shipped revenue attributed to your links*.
  - **Access is revoked after 30 consecutive days with no qualifying sales.**
- **Why it fails us:** the hunts don't drive Amazon sales; they *check
  prices*. We would get 30 days of access and then lose it. Gaming the sales
  requirement (buying through our own links) is against the Associates
  agreement and beneath us.
- **Verdict: not viable.** The gate is structural, not paperwork. Amazon
  stays on the browser leg (and the AI-agent wall stays on the block
  registry).

## 5. Best Buy — no public buyer API ❌ NOT AVAILABLE

- The old Remix product-catalog API is long dead. Best Buy's current API
  surface is seller-side (Mirakl marketplace onboarding for merchants).
- **Verdict:** nothing legitimate to use. Best Buy stays on the browser leg.

## 6. Keepa (Amazon price history) ❌ PAID — fails the free-tier rule

- The free Keepa *extension* shows price history charts on Amazon product
  pages and is genuinely useful for a human checking a deal by hand.
- The Keepa *API* starts around €49/month (20 tokens/minute); no free API
  tier is published. That violates the standing free-tier principle.
- **Verdict:** extension is a fine human tool (Dennis can install it);
  the API is not a channel we'll build on.

## 7. CamelCamelCamel — free charts, no API ⚠️ HUMAN TOOL ONLY

- Free Amazon price history, no account needed beyond an email for alerts.
- No public API — charts and alerts only.
- **Verdict:** useful for Dennis to eyeball a deal's history; not
  automatable. Same shelf as the Keepa extension.

## 8. Reddit API — deal subreddits 🔍 LEAD (not yet evaluated)

- Reddit offers an official OAuth API (free app registration; ~100
  queries/min authenticated). Subreddits like r/buildapcsales are real
  deal-discovery channels.
- reddit.com sits in our block registry as bot-walled for *browsing*; the
  API is a separate, sanctioned endpoint (`oauth.reddit.com`) — using it is
  legitimate, not circumvention.
- **Verdict: lead.** Not surveyed deeply enough to recommend yet. Worth a
  proper evaluation: register an app, pull r/buildapcsales, measure
  signal-vs-noise for the GPU/shoe targets.

---

## Verdict table

| Source | Legitimate channel | Replaces browser leg? | Gate |
|---|---|---|---|
| eBay | Browse API (official) | **Yes** — structured search, 5k calls/day free | free dev signup |
| Craigslist Sacramento | Search RSS (`?format=rss`) | **Yes** — official feed, no auth | none |
| Newegg | Affiliate catalog/RSS feeds | Partial — needs approval first | affiliate application |
| Amazon | PA-API 5.0 | **No** — sales-gated, access lapses | 3 sales/180d + ongoing sales |
| Best Buy | — | **No** — no public buyer API exists | — |
| Amazon price history | Keepa API | **No** — paid, fails free-tier rule | €49/mo |
| Amazon price history | Keepa ext / CamelCamelCamel | Human tools only, not automatable | none (manual use) |
| Deal discovery | Reddit API | Lead — evaluate properly | free app registration |

**Net for the hunts:** eBay Browse API + Craigslist RSS eliminate two of
the heaviest browser legs with zero rule-bending. Amazon and Best Buy stay
where they are. Newegg is one application away from joining the clean
channels.

---

## HARD RULES — where the line is

These are not guidelines. Every future Muse: the line is here, it does not
move, and "but it would be faster" is never a reason to cross it.

1. **No CAPTCHA solving by agents.** Standing policy: Dennis handles
   CAPTCHAs. We never solve, bypass, or farm them.
2. **No challenge bypassing.** Cloudflare "Verifying you are human",
   DataDome, Akamai walls, AI-agent interstitials — we do not defeat,
   spoof, or route around them. We log them in the block registry and use a
   legitimate channel or move on.
3. **No ToS-violating scraping.** If a site's terms prohibit automated
   access and no official API/feed exists, we don't scrape it — we note the
   gap and check it by hand or not at all.
4. **No evasion infrastructure.** No residential proxies, no IP rotation to
   dodge rate limits, no headless-detection evasion, no fake accounts to
   pass gates. If the front door needs a trick to open, it's not our door.
5. **No credential games.** One account per human, ours only with his
   explicit direction. Never create accounts to multiply quotas.
6. **APIs get used as documented.** Respect rate limits, cache aggressively,
   attribute per the license. A sanctioned channel used abusively becomes an
   unsanctioned one.
7. **When in doubt, the registry decides.** If a channel isn't clearly
   vendor-sanctioned, it doesn't go in the playbook. Ask Dennis before
   gray-area work, never after.

The principle underneath: **we go through doors, not through walls.**
Official APIs, public feeds, affiliate programs, robots-respecting fetches,
and Dennis's own browser when a human is the right tool. Everything else is
someone else's problem.

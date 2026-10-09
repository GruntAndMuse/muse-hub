# Amazon Associates path — DRAFT (prep only)

**Status:** DRAFT. Nothing published, nothing signed up. For Dennis's review only.
**Prepared:** 2026-10-09
**Why this exists:** Dennis's call — Amazon's reach dwarfs eBay's, so legitimate Amazon data access helps the most people. Worth attempting the treadmill honestly.

## What changed (verified 2026-10-09 — this matters)

Amazon's **Product Advertising API 5.0 is deprecated**. Amazon's own docs
(webservices.amazon.com, opened directly 2026-10-09) show a deprecation
notice: PA-API 5 calls now return HTTP 403, and the successor is the
**Creators API** (OAuth 2.0, endpoints at `creatorsapi.amazon/catalog/v1/`,
Python/Node/PHP/Java SDKs — confirmed in Amazon's migration guide at
affiliate-program.amazon.com, opened directly 2026-10-09).

The access bar moved with it. Multiple independent third-party sources
(getsquirrel.co, azonpress.com, a Dec 2025 builder post-mortem — all
consistent) report the Creators API requires **10 qualifying referred sales
in the trailing 30 days**, rolling window. Amazon's own pages confirm the
deprecation and the OAuth model but do not state the sales number on the
pages I could open — **re-verify the 10-sales figure inside Associates
Central before building anything on it.** Treat it as high-confidence
second-hand until then.

Bottom line: the old math (3 sales once, then don't go 30 days dry) is dead.
The new math is **~10 genuine sales every rolling 30 days, forever**. Read
the honest-math section before deciding anything.

---

## 1. Draft page copy — "Parts & tools we actually use"

*Intended home: gruntandmuse.com or the Substack. Not published until
Dennis approves.*

---

# Parts & tools we actually use

**Why this page exists, plainly:** Every link below is an Amazon affiliate
link. They exist for one reason: Amazon only opens its product-data API to
affiliates who drive real sales, and we need that API to power free,
open-source deal-tracking tools for the community. Not to get rich — the
commissions are coffee money. If you'd rather not use the links, search the
product names yourself; we list exact model numbers so you can.

Everything here is something we actually own and use. No paid placements,
no hype, no "top 10" filler.

## 3D printing

- **Creality K2** — the workhorse. Everything gets prototyped and test-fit
  on it before proven designs go out for printing in better materials.
- **Revopoint Range 2 3D scanner** — 0.1 mm precision. Bought
  manufacturer-refurbished; does the job.
- **Creality CR-Scan Raptor Pro** — factory-certified unit with the
  extended warranty. The blue laser kills scanning spray on black plastic,
  which matters more than it sounds.
- **Marker dots** — cheap, and beat spray for most jobs.
- **Eibos Cyclopes filament dryer** — wet filament is failed prints; dry it.
- **CryoGrip build plates (Frostbite + Glacier)** — what we print on.
- **MicroSwiss FlowTech hotend + Phaetus DXC2 extruder** — the upgrade
  pair, waiting on install day.
- **TH3D Tough Tube** — PTFE tube that doesn't quit.
- **Sorbothane feet/pad** — vibration damping under the printer.

## Shop & electrical

- **Tinned copper TXL/GXL wire, SAE J1128, 125°C rated** — the only wire
  spec we'll stand behind for automotive work. Oxygen-free copper is
  marketing at 12V; skip it.
- **Double-wall adhesive-lined heat shrink** — on every connection, no
  exceptions.
- **Abrasion + fire-retardant sleeving** — over all runs.
- **WZHUIDA hardware assortment** — M5/M4 flat-head bolts and nuts. Buy
  the assortment, stop making hardware runs.

## The PC that runs the local AI

- **MSI RTX 4070 Ti SUPER 16GB (VENTUS 3X OC)** — 16GB VRAM is the
  practical ceiling for local models on this box.
- **Ryzen 9 7900X · 32GB DDR5-6000 · 1TB Samsung 9100 Pro NVMe ·
  4TB TeamGroup SSD · ASUS TUF X870E-Plus WiFi7 · 850W 80+ Titanium ·
  Cooler Master Qube 540** — the full build, for anyone replicating a
  local-AI workstation.

## The rest

- **ThirdReality Smart Switch Gen3 + Hubitat C8 Pro** — remote power for
  the printer. The printer stays off when it's not working.
- **Under Armour Charged Assert 10 Wide (2E), all-black (3028816-002),
  US 11.5** — the daily driver. Two pairs in rotation.

*We buy research parts at Mouser (datasheets you can actually verify)
and buy at Amazon (best shipping). That's the whole supplier philosophy.*

---

## 2. Associates signup checklist

From Amazon's own docs (affiliate-program.amazon.com help, crawled
2026-10-07; third-party guides cross-checked 2026-10-09):

1. **Have the content property ready FIRST.** Amazon reviews the actual
   site/channel. Their bar, in their words: robust original content (~10
   posts as a rule of thumb), recent (within the last 60 days), publicly
   available, owned by you. Rejected applications can't be reassessed — do
   not apply with a thin site.
2. **Sign up** at affiliate-program.amazon.com with the existing Amazon
   customer account. Free. Takes ~15–20 minutes.
3. **Register the property:** the GruntAndMuse site or Substack URL.
   Multiple properties can be added later.
4. **Pick a Store/Tracking ID** (e.g. `gruntandmuse-20`). This goes in the
   links.
5. **Describe the traffic plan honestly** — "open-source hardware
   community; parts lists on project build logs" is a real answer.
6. **Payment + tax info** — needed for payouts (direct deposit; thresholds
   apply).
7. **Provisional approval** is fast (often ~24h). The real review happens
   after the sales bar: **at least 3 qualifying sales within the first 180
   days. Personal orders do not count.** Miss it and the account closes.
8. **Affiliate disclosure** on every page carrying links — required, not
   optional. The draft page above includes it.

## 3. Creators API eligibility (the actual gate)

- Register in Associates Central under Tools → CreatorsAPI tab → Create
  Application → Create Credential. You get a **Credential ID + Credential
  Secret** (OAuth 2.0 client-credentials; tokens valid 1 hour, cache them).
  Old PA-API keys do not work.
- Reported requirement (third-party, re-verify): **10 qualifying referred
  sales in the trailing 30 days**, rolling. Access depends on *continuing*
  to generate sales, not clearing a bar once.
- Only the primary account owner can register the application.

## 4. The honest math

**Getting in:** a real content property (the GruntAndMuse site with actual
build logs qualifies on paper) + 3 genuine sales in 180 days. Achievable —
three readers buying a $30 marker-dot pack through the links clears it.

**Staying in:** ~10 genuine referred sales **every rolling 30 days**,
indefinitely. This is the treadmill, and it's the part to be honest about:
our tools *check* prices; they don't *drive* purchases. The only engine
that feeds this is a real audience buying real parts through the links,
month after month. A "parts we use" page on a site people actually read
for build logs could plausibly do it. A page nobody visits cannot.

**What it costs if it works:** nothing but the discipline — links stay
genuine, disclosures stay up, content stays real. No dark patterns, ever.

**What it costs if it doesn't:** the Associates account lapses and the API
never materializes. Time spent: one honest page and a signup. That's the
bounded downside.

**Fallback (standing):** Amazon stays on the backoff-and-recheck browser
approach per the block registry. No circumvention, no challenge bypassing,
no ToS-violating scraping — ever. The line doesn't move because the API
didn't work out.

## 5. Open questions for Dennis

1. **Venue:** gruntandmuse.com page or Substack post (or both)? The
   Associates application needs the property URL up front.
2. **Timing:** apply now with current content, or wait until the site has
   deeper build-log content? (Amazon rejects thin applications without
   reassessment — the content bar is the real gate, not the signup form.)
3. **Item list:** the draft above is seeded from memory — red-pen it. Cut
   anything he wouldn't personally vouch for; add anything missing.
4. **eBay first:** the eBay Browse API test (no sales quota, no treadmill)
   is the nearer-term win. Amazon is the long game. Both can run in
   parallel.

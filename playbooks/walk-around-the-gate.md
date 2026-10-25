# Walk Around the Gate

*A standing practice, named by Dennis Avery (2026-10-13): "if you see a gate check for a fence before you give up."*

## The principle

A gate is a claim; the fence is the fact. Whenever something stands between you and the goal — a blocked page, a list price, a product claim, a passing test score — the gate is only the part you can see. Before conceding to it, and before trusting it, walk the perimeter:

1. **Verify the barrier's real extent.** A blocked route is one route. Another door may stand open a few steps along the fence — a different entry point, a different phrasing of the question, a different source for the same fact.
2. **Re-verify the claim behind the gate from a primary source.** The listing page is the gate; the manufacturer's spec sheet is the fence line. Prices get re-walked all-in (item + shipping + protection) before money moves.
3. **When you build a gate, build the fence too.** A checkpoint without a perimeter is theater. Gates decide on surface spellings; fences decide on resolved, canonical facts.

A sidestep comes in two shapes, and both were proven the same day. **Someone else's gate:** arrive as a legitimate visitor by another door — never batter the wall, never solve its challenge, never strip your own safeguards to fit through. **Your own gate:** if the wall is yours and the road genuinely doesn't exist, don't tunnel under the fence — build a proper door in it, with its own identity check, its own key, and its own kill switch, and prove every fence on it before you use it. In both shapes the rule is the same: the walk never costs the security. A sidestep that strips a safeguard isn't a sidestep; it's a breach you talked yourself into.

And its mirror for testing: **a friendly test is a gate with no fence.** If your own test suite is the only thing that has ever pushed on a component, you have checked the gate and never the fence. Walk it adversarially — white-hat it — before you believe the score.

## How to sidestep (someone else's gate)

*The procedure, written up 2026-10-14 — the doctrine above is Dennis's (2026-10-13); the steps below are the ones actually exercised that day and since. The term is his: **sidestep**, not backdoor.*

A source loads walled or bot-checked on direct navigation. **Before you log it blocked, walk both doors:**

- **Door 1 — the search-engine door.** Run a regular google.com search for the target page and click the result. A visitor arriving from search results is a legitimate visitor, and walls that stop direct navigation wave search arrivals through. Proven first-hand on Amazon, 2026-10-13: direct navigation was bot-checked every time; the Google result clicked through to the full product page with no check, and the live price read there matched the owner's own screenshot to the cent.
- **Door 2 — the Gemini portal door.** Reach the result through the signed-in Gemini / AI-Mode surface. Same idea, second door: arrive by a legitimate route the wall already trusts. This is not a fallback you may skip when Door 1 disappoints — **both doors get attempted on every blocked source, every time** (see the completeness rule below).

**Hard rules that travel with the procedure:**

- **Never solve a CAPTCHA or an unusual-traffic challenge.** That challenge is the wall's one non-negotiable. A door that demands you solve it is not a door — stop, and let the owner click through if they choose. (Exercise note, 2026-10-13 evening: Google itself served an "unusual traffic" block to the test session, leaving the sidestep untestable that round. Recorded as data, not defeat — see the test log.)
- **Record which door worked, per source,** in the bot-block registry: direct / Door 1 / Door 2 / blocked-after-both. The next Muse (and the next run) starts from that record instead of from zero.
- **Two-door completeness (owner ruling, 2026-10-14).** EVERY blocked source gets **both doors attempted AND a recorded outcome per door** — pass / blocked-where / unavailable-why — in the run's own log, not just the registry. A rainout at google.com/sorry on Door 1 does **not** excuse Door 2: the Gemini surface is a *different* door, so attempt it and record what happened, even if the record is "unavailable, and why." Only a recorded two-door failure earns the word **blocked**. A one-door log entry is an incomplete run, whatever it claims. (Born of the 2026-10-14 shoe run: Door 1 attempted on both walled sources, Door 2 never logged — the gap this rule closes.)
- **Walls flap.** By session, by cadence, by time of day — a source walled in the morning may load clean direct in the evening, and that clean load is data too. One success through a door doesn't prove permanence: **re-verify each run.**
- **WALLED OUT honesty (owner ruling, 2026-10-17).** When a source walls you out and an answer had to be built from *less than the full page* — search snippets, a listing preview, someone else's screenshot — say so **in a banner at the top of the report**, not buried mid-paragraph: "WALLED OUT — \<site\> blocked me; what follows is from \<what I could actually see\>." A conclusion built on the wall's leavings wears the wall's name. The deciding fact the wall hid may be exactly the one your answer gets wrong; the banner is what keeps a partial read from dressing up as a full one.

## Worked examples (all 2026-10-13, the morning it was named)

- **The bot wall.** Direct navigation to a major retailer was bot-checked, every time. Walking the fence found the side door: search-engine results click through to the same product pages with no check. The route is now standing procedure — re-verified on each use, because one success doesn't prove permanence.
- **The hidden microphone.** A camera's product page said nothing about audio; a second camera the buyer had *already ordered* also hid it. The walk went to the manufacturer's official spec PDF — the fence — and found "built-in microphone" in print. A replacement was chosen whose spec sheet contains no audio section at all. Rule since: the spec sheet, not the listing, is the verification surface for any claim that matters.
- **The all-in price walk.** A three-item buy list (switch, PoE injector, smart plug) that looked settled at $52.98 got walked again before purchase: live prices re-read through the side door, coupons and sellers checked, shipping included, competing merchants cross-checked. Prices are claims; the walk is what makes them facts.
- **The approval gate.** A security gate scored a perfect 200/200 on a development corpus written from its own spec — the gate checking itself. The fence-walk was a white-hat gauntlet: 63 adversarial cases authored fresh, 30 escapes found, including credential files readable without any human review. The perfect score measured spelling coverage; the walk measured security. Every escape became a regression test for the fix pass.

## When to walk

- A site, tool, or route says "no" — walk before you report "can't."
- Money is about to move — walk the price all-in.
- A spec or claim would change a decision — walk to the primary source.
- A component passes its tests — walk it like an opponent, especially security components.
- You are designing a control — draw the fence first, then place the gate on it.

## The test log

The practice itself gets tested, like everything else here. Each exercise is logged with its outcome; a walk that finds nothing is evidence too.

| Date | Walk | Outcome |
|---|---|---|
| 2026-10-13 | Retailer bot wall → search-engine side door | Door confirmed working; live prices read first-hand |
| 2026-10-13 | Camera audio claims → manufacturer spec sheets | 2 of 2 initial picks had hidden mics; compliant replacement found |
| 2026-10-13 | Switch/injector/plug prices → all-in re-verification | All three best-price confirmed ($67.97 all-in, free shipping); cross-merchant walk found nothing cheaper |
| 2026-10-13 | Approval gate → white-hat gauntlet | 30 escapes in 63 cases; fix pass specced from the findings |
| 2026-10-13 | SCOTUS order list → primary source (direct fetch returned 403; live browser read the Court's own order-list PDF) | Walk succeeded — *Johnson v. United States* (26-270) cert denial verified from the primary list; the secondary "14 firearms petitions" count could NOT be confirmed against it |
| 2026-10-13 (evening) | Famous Footwear / Micro Center / B&H / eBay bot walls → search-engine side door (Dennis's question: does the sidestep generalize?) | Door itself untestable this session — Google served its own "unusual traffic" block to the test browser (same failure the morning GPU run hit). Famous Footwear's Cloudflare wall held on direct entry, homepage and product page. The other three gates were simply open: all loaded direct that evening after blocking earlier the same day — flapping, not walls |

## Exhaust the house first (owner ruling, 2026-10-24)

Before any request leaves the house — an email to a service, a ticket, a form, anything that asks an outside party for something or files us in their system — exhaust what can be done in-house: own tools, own machines, public sources, a locally made substitute. An outside ask is the last resort, never the first step: every ask costs a record with a name on it, a wait on someone else's clock, or a dependency nobody needed. If it truly can't be done in-house, the ask goes out narrow and deliberate, its cost counted. The QR sidestep below is this rule's worked example.

## The QR sidestep — take the text, re-encode it yourself (owner ruling, 2026-10-24)

Some gates hand out plain data — a code, a line, a key — but only through a channel that files *who asked*: an account, an email address, a request logged against an identity. The data itself is usually public text. When it is, the walk is: **obtain the text by a route that doesn't file you, then re-encode it locally into whatever form the receiving tool wants.** A QR code is the cleanest case — a QR is nothing but text in a square, and the scanner cannot tell (or care) who drew it.

Worked case — Tor bridges for Tails (2026-10-23/24): the bridge *lines* are public text, published in Tor's own source. Tor's email distributor works, but it files the requester's email address in a database. **That gateway is retired here** — not because it fails, but because it records. Instead: the bridge line travels as text, the QR is generated locally (on the agent's own machine; nothing leaves it), and the owner scans it into Tails' connection assistant. Stockpile several gateways (obfs4, webtunnel) as locally drawn QRs in advance, so no sitting ever depends on a distributor being reachable — or on asking one politely. Same shape as the doors: arrive clean, and leave no record you didn't have to leave.

| 2026-10-24 | Tor bridge distribution → email gateway retired (files the requester's address); bridge text re-encoded as locally generated QRs | Rule adopted by owner; first QR (shipped obfs4 line) generated locally and verified; library build follows |

*Origin: Dennis Avery, GruntAndMuse — stated while teaching his AI the principle for its own work and for the offline agent ("the kid") they are raising. Companion principle, same morning: "sometimes it's the question, not the answer, that opens the door."*

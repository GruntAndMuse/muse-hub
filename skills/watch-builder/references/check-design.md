# Check Design

## The exact-method rule

The first method you try is usually the noisy one. The deed watch's first method — the site's plain simple search — OR-matched name tokens and flooded with hundreds of noise rows. The fix was the site's exact-name refinement. **Lesson: when a check returns noise, the method is wrong, not the world. Find the precise query before scheduling anything.**

Other exact-method wins from production:
- Shoe watch: Amazon variant pages silently switch colorway when you select a width — the method must RE-VERIFY the final selected colorway after every selection, or you get false positives. (One real false positive taught this.)
- GPU hunt: never report prices from text-search snippets — only from actual product/listing pages.

## Coverage list

One run = a FIXED list of sources checked every time, in a fixed order. Write it in the cron definition. No rotation, no "I'll check the important ones." The list is the contract:
- Deed watch: 4 exact-name searches, every day.
- GPU hunt: 6 retail sellers + Craigslist + Facebook Marketplace CLI, 2x daily.
- Shoe watch: 8 retailers, 2x daily.

Report coverage honestly: "6/8 checked live, 2 bot-blocked" is a completed run. Name the unchecked ones.

## Cadence

Match cadence to the threat's speed:
- Fraud / legal: daily (deed watch runs daily at 09:20).
- Deals / stock: 2x daily, timed to land before the user's digest reads (GPU/shoe/FOSS run 07:30 + 16:30 PDT, digests read at 8am/5pm).
- Slow-moving: weekly is fine. Don't check faster than the world changes — that's just burn.

## Bot-block policy

- **Note and move on.** A blocked source gets one line in the run note ("Amazon: anti-agent interstitial, ~20th straight run, no retry per policy") — never burn run budget retrying it.
- **Never solve challenges.** CAPTCHAs, human-verification checkboxes, puzzle sliders: not attempted, ever. The user handles those if they choose.
- **Back off, don't hammer.** Track consecutive blocks per source (the bot-block registry + source-health pattern): full cadence while clean, 1x/day after 3 straight blocks, 1x/week after 7, reset on success. A wall that hasn't moved in weeks doesn't need probing twice a day.
- **Skip lists are explicit.** Maintain a written list of currently-skipped sources with the block type and date. Re-probe on schedule, restore when clean.

## Timeboxing

The flaky leg gets a timebox. GPU hunt: if the browser leg hasn't returned usable results in ~20 minutes, commit what you have (Facebook CLI results + whatever retail is in hand), name the unchecked sources, end the run. **A partial committed run always beats a full timeout with nothing.**

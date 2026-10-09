# eBay Browse API — signup guide (for Dennis)

Goal: get an eBay developer keyset so the GPU hunt can query eBay through
the official API instead of a slow browser task. Read-only search only —
no buying, no bidding, nothing listed or changed on your account.

## What you need

- An eBay account (free at ebay.com if you don't have one — you only use
  it to sign in, the API never touches your buying/selling).
- About 5 minutes. Approval of the developer account can take up to ~1
  business day in some cases; the keyset itself is created instantly once
  you're in.

## Steps

1. Go to **https://developer.ebay.com/signin** and sign in with your
   eBay account. Accept the API License Agreement.
2. Open **Application Keys** (in the developer dashboard).
3. Under **Production**, click **Create a keyset**.
4. Confirm the primary contact info when asked, then **Continue to
   Create Keys**.
5. You now have a keyset with three values. You need two:
   - **App ID** → this is the Client ID
   - **Cert ID** → this is the Client Secret
   (Dev ID is not needed for this.)
6. Put them in the Secure Vault (never in chat, email, or notes):
   - App ID → saved as `EBAY_CLIENT_ID`
   - Cert ID → saved as `EBAY_CLIENT_SECRET`

That's it. Tell me "got it" and I'll run the test.

## What the test does (once credentials exist)

Runs all 10 standing GPU-hunt eBay queries through the official API:

    EBAY_CLIENT_ID=... EBAY_CLIENT_SECRET=... \
      python3 ~/workspace/browser/ebay-browse-test.py

Measures: total seconds for all queries, results per query, qualifying
listings under each all-in cap, and whether the API data covers what the
browser leg covers:

| Check | Browser leg today | API must match |
|---|---|---|
| Speed | ~15 min for eBay portion | seconds expected |
| Price + shipping | yes (product page) | yes (price + shippingOptions) |
| Seller reputation | yes (feedback page) | yes (feedbackScore/%) |
| Condition / dead cards | yes ("parts/not working") | title-keyword filter |
| Auctions + bid counts | yes | yes (buyingOptions/bidCount) |
| Protection-plan eligibility | yes (Allstate plan badge) | NO — expected gap |
| Best-offer / local pickup | partial | partial |

Decision rule: if the API is faster AND the data covers everything except
the known protection-plan gap (finalist verification stays in the
browser), it replaces the eBay browser leg. If not, the browser leg stays.

## Rate limits (for reference)

- Free tier: 5,000 API calls/day (Basic), 10,000/day (Standard, may need
  a request). ~5 calls/second.
- Our test uses ~11 calls. A twice-daily hunt run uses ~25. Nowhere near
  the ceiling.

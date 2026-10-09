#!/usr/bin/env python3
"""eBay Browse API test client for the RTX GPU hunt.

READ-ONLY search — no purchases, no bidding, no listing actions.

Credentials: read ONLY from environment variables EBAY_CLIENT_ID and
EBAY_CLIENT_SECRET. They are never printed, logged, or written to disk.

Usage:
    EBAY_CLIENT_ID=... EBAY_CLIENT_SECRET=... python3 ebay-browse-test.py [--json]

The script runs the GPU hunt's standing eBay queries through the official
Browse API (client-credentials OAuth2) and prints structured results plus
per-query timing, so the API leg can be compared against the browser leg.

Hunt targets (all-in = item price + shipping):
  Target 1 (under $500): RTX 4070, 4070 Super, 4070 Ti, 4070 Ti Super,
                         4080, 4080 Super (12GB+ only)
  Target 2: RTX 3090 ($800), 3090 Ti ($900), 4090 ($1000), 5090 ($1500)
"""

import base64
import json
import os
import sys
import time
import urllib.parse

import requests

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
MARKETPLACE_ID = "EBAY_US"
OAUTH_SCOPE = "https://api.ebay.com/oauth/api_scope"
REQUEST_TIMEOUT = 30

# (query, all-in cap USD)
HUNT_QUERIES = [
    ("RTX 4070", 500),
    ("RTX 4070 Super", 500),
    ("RTX 4070 Ti", 500),
    ("RTX 4070 Ti Super", 500),
    ("RTX 4080", 500),
    ("RTX 4080 Super", 500),
    ("RTX 3090", 800),
    ("RTX 3090 Ti", 900),
    ("RTX 4090", 1000),
    ("RTX 5090", 1500),
]

# Title keywords that mark a dead/broken card the hunt must skip.
EXCLUDE_KEYWORDS = ("parts", "not working", "as-is", "as is", "for repair",
                    "untested", "no display", "artifacting")

_cached_token = None
_cached_token_expires_at = 0.0


def _creds():
    client_id = os.environ.get("EBAY_CLIENT_ID", "")
    client_secret = os.environ.get("EBAY_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        print("ERROR: set EBAY_CLIENT_ID and EBAY_CLIENT_SECRET in the environment.",
              file=sys.stderr)
        sys.exit(2)
    return client_id, client_secret


def get_token():
    """OAuth2 client-credentials token, cached with a 60s safety margin."""
    global _cached_token, _cached_token_expires_at
    if _cached_token and time.time() < _cached_token_expires_at - 60:
        return _cached_token
    client_id, client_secret = _creds()
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    resp = requests.post(
        TOKEN_URL,
        headers={"Authorization": f"Basic {basic}",
                 "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials", "scope": OAUTH_SCOPE},
        timeout=REQUEST_TIMEOUT,
    )
    if resp.status_code in (401, 403):
        print(f"ERROR: auth failed ({resp.status_code}) — bad client ID/secret.",
              file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    body = resp.json()
    _cached_token = body["access_token"]
    _cached_token_expires_at = time.time() + int(body.get("expires_in", 7200))
    return _cached_token


def search(query, price_cap, buying_options="FIXED_PRICE|AUCTION", limit=50,
           sort="price"):
    """Run one item_summary search; return (results, elapsed_s, total)."""
    token = get_token()
    filt = (f"buyingOptions:{{{buying_options}}},"
            f"price:[1..{price_cap}],priceCurrency:USD")
    params = {
        "q": query,
        "filter": filt,
        "sort": sort,
        "limit": min(limit, 200),
    }
    t0 = time.time()
    resp = requests.get(
        SEARCH_URL,
        headers={"Authorization": f"Bearer {token}",
                 "X-EBAY-C-MARKETPLACE-ID": MARKETPLACE_ID},
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
    elapsed = time.time() - t0
    if resp.status_code == 429:
        print("ERROR: rate limited (429). Back off and retry.", file=sys.stderr)
        sys.exit(1)
    if resp.status_code in (401, 403):
        print(f"ERROR: token rejected ({resp.status_code}).", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    body = resp.json()
    items = [normalize(it) for it in body.get("itemSummaries", [])]
    return items, elapsed, body.get("total", 0)


def _shipping_cost(item):
    """Best-effort shipping cost in USD; None if unknown."""
    for opt in item.get("shippingOptions", []) or []:
        cost = (opt.get("shippingCost") or {})
        if cost.get("value") is not None:
            try:
                return float(cost["value"])
            except (TypeError, ValueError):
                continue
    return None


def normalize(item):
    """Flatten one itemSummary into the hunt's working record."""
    price = item.get("price") or {}
    seller = item.get("seller") or {}
    try:
        price_val = float(price.get("value", 0))
    except (TypeError, ValueError):
        price_val = 0.0
    ship = _shipping_cost(item)
    all_in = price_val + (ship or 0.0)
    return {
        "title": item.get("title", ""),
        "item_id": item.get("legacyItemId") or item.get("itemId"),
        "url": item.get("itemWebUrl"),
        "price": price_val,
        "currency": price.get("currency"),
        "shipping": ship,
        "all_in": round(all_in, 2),
        "condition": item.get("condition"),
        "buying_options": item.get("buyingOptions"),
        "bid_count": item.get("bidCount"),
        "seller": seller.get("username"),
        "feedback_score": seller.get("feedbackScore"),
        "feedback_pct": seller.get("feedbackPercentage"),
        "location": (item.get("itemLocation") or {}).get("country"),
    }


def dead_card(title):
    t = title.lower()
    return any(k in t for k in EXCLUDE_KEYWORDS)


def run_hunt():
    """Run all standing hunt queries; return (report, total_elapsed)."""
    report = {"queries": [], "total_elapsed_s": 0.0, "qualifying": []}
    grand_t0 = time.time()
    for q, cap in HUNT_QUERIES:
        items, elapsed, total = search(q, cap)
        qualifying = [it for it in items
                      if it["all_in"] <= cap and not dead_card(it["title"])]
        report["queries"].append({
            "query": q, "cap": cap, "total_results": total,
            "elapsed_s": round(elapsed, 2),
            "returned": len(items), "qualifying": len(qualifying),
        })
        report["qualifying"].extend(
            {"query": q, "cap": cap, **it} for it in qualifying)
        report["total_elapsed_s"] = round(time.time() - grand_t0, 2)
        time.sleep(0.5)  # polite: stay far under the ~5 calls/sec ceiling
    return report


def human_report(report):
    lines = [f"eBay Browse API — GPU hunt test run",
             f"Total API time: {report['total_elapsed_s']}s "
             f"across {len(report['queries'])} queries", ""]
    for q in report["queries"]:
        lines.append(
            f"[{q['query']}] cap ${q['cap']}: {q['total_results']} total, "
            f"{q['returned']} fetched, {q['qualifying']} qualifying "
            f"({q['elapsed_s']}s)")
    lines.append("")
    if report["qualifying"]:
        lines.append("QUALIFYING LISTINGS:")
        for it in report["qualifying"]:
            lines.append(
                f"  ${it['all_in']:.2f} all-in | {it['title'][:70]} | "
                f"{it['condition']} | seller {it['seller']} "
                f"(score {it['feedback_score']}, {it['feedback_pct']}%) | "
                f"{it['url']}")
    else:
        lines.append("No qualifying listings under the all-in caps.")
    return "\n".join(lines)


def main():
    as_json = "--json" in sys.argv[1:]
    report = run_hunt()
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print(human_report(report))


if __name__ == "__main__":
    main()

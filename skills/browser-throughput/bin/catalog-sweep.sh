#!/usr/bin/env bash
# catalog-sweep.sh — fast first-pass product sweep using Meta's catalog search.
#
# WHY: the live browser is the slowest tool in the shop (~15 min per retail
# sweep). This runs up to 8 semantic queries in ONE call (~3 sec) and returns
# a deduped, price-filtered candidate list. It does NOT verify stock, variant,
# size, or seller reputation — those still need the browser. Use this as the
# fast tier; send only finalists to the slow tier.
#
# USAGE:
#   catalog-sweep.sh --out results.json --max-price 500 \
#       --query "RTX 4070" --query "RTX 4070 Super" --query "RTX 3090"
#
# OPTIONS:
#   --out PATH        output JSON (required)
#   --query TEXT      semantic query (repeatable, max 8)
#   --brand NAME      brand constraint, e.g. "Under Armour" (repeatable ok)
#   --domain HOST     seller-domain ranking preference (repeatable ok)
#   --gender male|female|unisex
#   --currency USD    (required with --max-price/--min-price)
#   --max-price DOLLARS  price ceiling, e.g. 500
#   --min-price DOLLARS  price floor
#   --num N           results per query (default 20)
#
# OUTPUT: JSON array of {name, price, sale_price, url, product_id},
# deduped by URL, sorted by numeric price ascending, image URLs stripped.
set -euo pipefail

OUT=""; QUERIES=(); BRAND_ARGS=(); DOMAIN_ARGS=()
GENDER=""; CURRENCY=""; MAX_PRICE=""; MIN_PRICE=""; NUM=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2;;
    --query) QUERIES+=("$2"); shift 2;;
    --brand) BRAND_ARGS+=(--brand "$2"); shift 2;;
    --domain) DOMAIN_ARGS+=(--domain "$2"); shift 2;;
    --gender) GENDER="$2"; shift 2;;
    --currency) CURRENCY="$2"; shift 2;;
    --max-price) MAX_PRICE="$2"; shift 2;;
    --min-price) MIN_PRICE="$2"; shift 2;;
    --num) NUM="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

[[ -z "$OUT" ]] && { echo "--out required" >&2; exit 1; }
[[ ${#QUERIES[@]} -eq 0 ]] && { echo "at least one --query required" >&2; exit 1; }
[[ ${#QUERIES[@]} -gt 8 ]] && { echo "max 8 queries per call" >&2; exit 1; }

RAW="$(mktemp "${TMPDIR:-/tmp}/catalog-sweep.XXXXXX.json")"
trap 'rm -f "$RAW"' EXIT

CMD=(meta-catalog-search --retries 2 --num-results "$NUM" --out "$RAW")
for q in "${QUERIES[@]}"; do CMD+=(-q "$q"); done
CMD+=("${BRAND_ARGS[@]}" "${DOMAIN_ARGS[@]}")
[[ -n "$GENDER" ]] && CMD+=(--gender "$GENDER")
if [[ -n "$MAX_PRICE" || -n "$MIN_PRICE" ]]; then
  [[ -z "$CURRENCY" ]] && { echo "--currency required with price filters" >&2; exit 1; }
  CMD+=(--currency "$CURRENCY")
  [[ -n "$MAX_PRICE" ]] && CMD+=(--max-price "$(( ${MAX_PRICE%.*} * 100 ))")
  [[ -n "$MIN_PRICE" ]] && CMD+=(--min-price "$(( ${MIN_PRICE%.*} * 100 ))")
fi

"${CMD[@]}" >/dev/null

# Dedupe by URL, keep cheapest-seeming fields, sort by price ascending.
jq --argjson maxp "${MAX_PRICE:-null}" '
  [.products[]
   | select(.url != null)
   | {name, price: (.sale_price // .price), product_id, url}
  ]
  | unique_by(.url)
  | map(select(.price != null))
  | map(. + {price_num: (.price | gsub("[^0-9.]";"") | tonumber? // 1e12)})
  | (if $maxp == null then . else map(select(.price_num <= $maxp)) end)
  | sort_by(.price_num)
  | map(del(.price_num))
' "$RAW" > "$OUT"

echo "wrote $(jq 'length' "$OUT") candidates to $OUT"

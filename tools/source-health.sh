#!/usr/bin/env bash
# source-health.sh — adaptive backoff for bot-blocked / flaky web sources.
#
# WHY: hunts probe the same blocked sources 2x/day for weeks (Amazon blocked
# ~20 straight shoe-watch runs). Each probe burns minutes before the wall is
# confirmed. This tracks per-source consecutive failures and backs off the
# probe cadence instead of hammering the wall every run.
#
# BACKOFF SCHEDULE (on consecutive non-ok results):
#   0-2 failures : probe every run (no backoff yet — could be transient)
#   3-6 failures : probe at most 1x per 20h
#   7+ failures  : probe at most 1x per 6 days
# Any "ok" resets the streak. A "due" source that gets skipped stays skipped;
# only an actual probe updates the record.
#
# USAGE:
#   source-health.sh record <hunt> <source> <ok|blocked|error> [note]
#   source-health.sh due <hunt> <source>        # exit 0 = probe it, 1 = skip
#   source-health.sh status [hunt]              # human-readable table
#
# STATE: ~/workspace/browser/source-health.json
set -euo pipefail

STATE_DIR=~/workspace/browser
STATE="$STATE_DIR/source-health.json"
mkdir -p "$STATE_DIR"
[[ -f "$STATE" ]] || echo '{}' > "$STATE"

now() { date +%s; }

record() {
  local hunt="$1" source="$2" status="$3" note="${4:-}"
  local key="$hunt/$source" ts
  ts=$(now)
  python3 - "$STATE" "$key" "$ts" "$status" "$note" <<'EOF'
import json, sys
path, key, ts, status, note = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
d = json.load(open(path))
e = d.setdefault(key, {"results": []})
e["results"].append({"ts": ts, "status": status, "note": note})
e["results"] = e["results"][-30:]  # keep last 30
json.dump(d, open(path, "w"), indent=1)
EOF
  echo "recorded: $key -> $status"
}

due() {
  local hunt="$1" source="$2"
  local key="$hunt/$source"
  python3 - "$STATE" "$key" "$(now)" <<'EOF'
import json, sys
path, key, now = sys.argv[1], sys.argv[2], int(sys.argv[3])
d = json.load(open(path))
results = d.get(key, {}).get("results", [])
# consecutive trailing non-ok
streak = 0
for r in reversed(results):
    if r["status"] == "ok":
        break
    streak += 1
last_ts = results[-1]["ts"] if results else 0
age_h = (now - last_ts) / 3600 if last_ts else 1e9
if streak <= 2:
    sys.exit(0)          # probe every run
elif streak <= 6:
    sys.exit(0 if age_h >= 20 else 1)   # 1x/day
else:
    sys.exit(0 if age_h >= 144 else 1)  # 1x/week
EOF
}

status() {
  local hunt="${1:-}"
  python3 - "$STATE" "$hunt" "$(now)" <<'EOF'
import json, sys, datetime
path, hunt, now = sys.argv[1], sys.argv[2], int(sys.argv[3])
d = json.load(open(path))
print(f"{'source':45} {'streak':>6} {'last':>10} {'last probe'}")
for key in sorted(d):
    if hunt and not key.startswith(hunt + "/"):
        continue
    results = d[key]["results"]
    streak = 0
    for r in reversed(results):
        if r["status"] == "ok":
            break
        streak += 1
    last = results[-1]
    age = datetime.datetime.fromtimestamp(last["ts"]).strftime("%m-%d %H:%M")
    print(f"{key:45} {streak:>6} {last['status']:>10} {age}")
EOF
}

case "${1:-}" in
  record) shift; record "$@";;
  due) shift; due "$@";;
  status) shift; status "$@";;
  *) echo "usage: $0 {record|due|status} ..." >&2; exit 1;;
esac

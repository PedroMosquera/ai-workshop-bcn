#!/usr/bin/env bash
# Checks that every slide of each deck fits its viewport, at four screen sizes, in both themes.
# Usage: tools/fit-check.sh [deck.html ...]   (default: build.html playbook.html)
# Needs Google Chrome and python3. Set CHROME to override the Chrome binary path.
set -euo pipefail
cd "$(dirname "$0")/.."

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PORT="${PORT:-8767}"
decks=("$@"); [ ${#decks[@]} -eq 0 ] && decks=(build.html playbook.html)

# The checker reads the deck through an iframe, which file:// URLs block, so serve over http.
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
server=$!
trap 'kill $server 2>/dev/null' EXIT
for _ in $(seq 20); do curl -s -o /dev/null "http://127.0.0.1:$PORT/" && break; sleep 0.25; done

run() {
  "$CHROME" --headless=new --disable-gpu --virtual-time-budget=10000 --window-size="$2,$3" --dump-dom \
    "http://127.0.0.1:$PORT/tools/fit-check.html?deck=../$1&w=$2&h=$3&theme=$4${5:-}" 2>/dev/null \
    | sed -n '/<pre id="out">/,/<\/pre>/p' | sed -e 's/<[^>]*>//g' -e '/^$/d'
}

fail=0
for deck in "${decks[@]}"; do
  for size in 1280x720 1920x1080 1024x640 1366x768; do
    w=${size%x*}; h=${size#*x}
    for theme in dark light; do
      out=$(run "$deck" "$w" "$h" "$theme")
      bad=$(grep -v ': ok$' <<<"$out" || true)
      echo "$deck $size $theme: $(grep -c ': ok$' <<<"$out") ok"
      [ -n "$bad" ] && { echo "$bad"; fail=1; }
    done
  done
done

# A checker that cannot fail proves nothing: plant an oversized block and expect a report.
grep -q -v ': ok$' <<<"$(run "${decks[0]}" 1280 720 dark '&inject=1')" \
  && echo "sanity: planted overflow detected" \
  || { echo "sanity: FAILED, the checker missed a planted overflow"; fail=1; }

exit $fail

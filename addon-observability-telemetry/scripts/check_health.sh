#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8000/healthz}"
EXPECT_SUBSTRING="${2:-}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-10}"

if command -v curl >/dev/null 2>&1; then
  RESPONSE="$(curl --fail --silent --show-error --max-time "$TIMEOUT_SECONDS" "$URL")"
elif command -v wget >/dev/null 2>&1; then
  RESPONSE="$(wget -qO- --timeout="$TIMEOUT_SECONDS" "$URL")"
else
  printf "Neither curl nor wget is available.\n" >&2
  exit 1
fi

if [ -n "$EXPECT_SUBSTRING" ] && ! printf "%s" "$RESPONSE" | grep -Fq "$EXPECT_SUBSTRING"; then
  printf "Health response did not contain expected substring: %s\n" "$EXPECT_SUBSTRING" >&2
  printf "Response: %s\n" "$RESPONSE" >&2
  exit 1
fi

printf "Health check passed for %s\n" "$URL"

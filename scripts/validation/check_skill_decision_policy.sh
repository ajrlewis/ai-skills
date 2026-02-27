#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
status=0

while IFS= read -r -d '' dir; do
  skill_md="$dir/SKILL.md"
  base="$(basename "$dir")"

  if [[ ! -f "$skill_md" ]]; then
    echo "ERROR: missing SKILL.md in $dir"
    status=1
    continue
  fi

  if ! rg -q '^## Decision Justification Rule$' "$skill_md"; then
    echo "ERROR: $base missing '## Decision Justification Rule' section"
    status=1
  fi

  if ! rg -q 'Every non-trivial decision must include a concrete justification\.' "$skill_md"; then
    echo "ERROR: $base missing mandatory decision-justification line"
    status=1
  fi

  if ! rg -q 'If justification is missing, treat the task as incomplete and surface it as a blocker\.' "$skill_md"; then
    echo "ERROR: $base missing mandatory blocker rule"
    status=1
  fi
done < <(find "$ROOT" -maxdepth 1 -type d \( -name "architect-*" -o -name "addon-*" -o -name "ui-*" \) -print0 | sort -z)

if [[ "$status" -eq 0 ]]; then
  echo "OK: all skills include the decision-justification policy."
fi

exit "$status"


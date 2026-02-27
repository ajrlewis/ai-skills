#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
status=0

while IFS= read -r -d '' dir; do
  base="$(basename "$dir")"
  skill_md="$dir/SKILL.md"

  if [[ ! -f "$skill_md" ]]; then
    echo "ERROR: missing SKILL.md in $dir"
    status=1
    continue
  fi

  if [[ ! "$base" =~ ^(architect|addon|ui)-[a-z0-9-]+$ ]]; then
    echo "ERROR: invalid skill directory name '$base' (expected architect-|addon-|ui- prefix)"
    status=1
  fi

  frontmatter_name="$(awk '
    BEGIN {in_frontmatter=0}
    /^---$/ {in_frontmatter = !in_frontmatter; next}
    in_frontmatter && /^name:[[:space:]]*/ {
      sub(/^name:[[:space:]]*/, "", $0);
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $0);
      print $0;
      exit
    }
  ' "$skill_md")"

  if [[ -z "$frontmatter_name" ]]; then
    echo "ERROR: missing frontmatter name in $skill_md"
    status=1
    continue
  fi

  if [[ "$frontmatter_name" != "$base" ]]; then
    echo "ERROR: frontmatter name '$frontmatter_name' does not match folder '$base'"
    status=1
  fi

  if [[ ! "$frontmatter_name" =~ ^(architect|addon|ui)-[a-z0-9-]+$ ]]; then
    echo "ERROR: frontmatter name '$frontmatter_name' must start with architect-|addon-|ui-"
    status=1
  fi
done < <(find "$ROOT" -maxdepth 1 -type d \( -name "architect-*" -o -name "addon-*" -o -name "ui-*" \) -print0 | sort -z)

if [[ "$status" -eq 0 ]]; then
  echo "OK: skill frontmatter names and prefixes are valid."
fi

exit "$status"

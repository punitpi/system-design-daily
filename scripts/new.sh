#!/usr/bin/env bash
# Create a new practice entry from a template and log it in the README.
# Usage: ./scripts/new.sh <concept|design|teardown> <slug> [issue-number]
set -euo pipefail

usage() {
  echo "Usage: $0 <concept|design|teardown> <slug> [issue-number]" >&2
  echo "  slug: lowercase letters, digits and hyphens, e.g. consistent-hashing" >&2
  exit 1
}

[[ $# -lt 2 || $# -gt 3 ]] && usage

type="$1"
slug="$2"
issue="${3:-}"

case "$type" in
  concept|design|teardown) ;;
  *) echo "Error: unknown type '$type'" >&2; usage ;;
esac

[[ "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo "Error: invalid slug '$slug'" >&2; usage; }
[[ -z "$issue" || "$issue" =~ ^[0-9]+$ ]] || { echo "Error: issue must be a number, got '$issue'" >&2; usage; }

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
date="$(date +%F)"
title="$(echo "$slug" | tr '-' ' ' | awk '{ for (i = 1; i <= NF; i++) $i = toupper(substr($i, 1, 1)) substr($i, 2); print }')"
issue_ref="${issue:+#$issue}"
issue_ref="${issue_ref:-—}"

case "$type" in
  concept)  rel="concepts/$date-$slug.md" ;;
  teardown) rel="teardowns/$date-$slug.md" ;;
  design)   rel="designs/$date-$slug/README.md" ;;
esac

target="$root/$rel"
if [[ -e "$target" ]]; then
  echo "Error: $rel already exists, refusing to overwrite" >&2
  exit 1
fi

mkdir -p "$(dirname "$target")"
# Write via redirect rather than `sed -i`, whose syntax differs between BSD (macOS) and GNU sed.
sed -e "s|{{TITLE}}|$title|g" \
    -e "s|{{DATE}}|$date|g" \
    -e "s|{{ISSUE}}|$issue_ref|g" \
    "$root/templates/$type.md" > "$target"

# Design entries link to their folder; others link to the file.
link="$rel"
[[ "$type" == design ]] && link="designs/$date-$slug/"

readme="$root/README.md"
# Make sure the table row starts on its own line.
[[ -n "$(tail -c 1 "$readme")" ]] && echo >> "$readme"
echo "| $date | $type | $title | $issue_ref | [$rel]($link) |" >> "$readme"

echo "$rel"

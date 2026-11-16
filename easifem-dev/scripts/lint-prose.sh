#!/usr/bin/env bash
# Usage: lint-prose.sh [--lines A-B[,C-D...]] <file> [<file> ...]
#
# Checks documentation prose with Vale and the EASIFEM rules in
# ../vale/: long sentences, passive voice, long asides in parentheses,
# code words not in backticks.
#
# - .md files are checked as they are.
# - .F90/.f90 files: the FORD docblock and `!!` prose is extracted first
#   (f90doc2md.py), so reported line numbers match the Fortran source.
#
# --lines limits the output to alerts on those line ranges (in every
# file), e.g. `--lines 850-1200` for the docblocks just edited. Use it on
# large files to keep the output short.
#
# Output: one alert per line, `file:line:col:rule:message`. Exits 0 when
# there are no warnings, 1 when there are warnings or errors, 2 on bad
# usage, 3 when vale is not installed (callers should skip the check and
# say so).
#
# Styles from Vale packages (write-good, Readability) are synced once into
# ${XDG_CACHE_HOME:-~/.cache}/easifem-dev/vale; this needs network access
# the first time.

usage="usage: lint-prose.sh [--lines A-B[,C-D...]] <file> [<file> ...]"
ranges=""
if [ "$1" = "--lines" ]; then
  ranges="$2"
  shift 2
  if ! printf '%s' "$ranges" | grep -Eq '^[0-9]+-[0-9]+(,[0-9]+-[0-9]+)*$'; then
    echo "$usage" >&2
    exit 2
  fi
fi
if [ "$#" -eq 0 ]; then
  echo "$usage" >&2
  exit 2
fi
if ! command -v vale >/dev/null 2>&1; then
  echo "lint-prose: vale not installed; prose check skipped" >&2
  exit 3
fi

here=$(cd "$(dirname "$0")" && pwd -P)
src="$here/../vale"
cache="${XDG_CACHE_HOME:-$HOME/.cache}/easifem-dev/vale"
mkdir -p "$cache/styles" || exit 2

# Refresh our own config and rules on every run; sync packages if missing.
cp "$src/vale.ini" "$cache/.vale.ini"
rm -rf "$cache/styles/EASIFEM"
cp -r "$src/EASIFEM" "$cache/styles/EASIFEM"
if [ ! -d "$cache/styles/write-good" ] || [ ! -d "$cache/styles/Readability" ]; then
  if ! (cd "$cache" && vale sync >/dev/null 2>&1); then
    echo "lint-prose: 'vale sync' failed (network?); prose check skipped" >&2
    exit 3
  fi
fi

tmp=$(mktemp -d "${TMPDIR:-/tmp}/lint-prose.XXXXXX") || exit 2
trap 'rm -rf "$tmp"' EXIT

status=0
for file in "$@"; do
  if [ ! -f "$file" ]; then
    echo "$file: not found"
    status=1
    continue
  fi
  case "$file" in
    *.F90 | *.f90)
      md="$tmp/$(basename "$file").md"
      python3 -I "$here/f90doc2md.py" "$file" "$md" || { status=1; continue; }
      ;;
    *.md) md="$file" ;;
    *)
      echo "$file: skipped (only .md and .F90)"
      continue
      ;;
  esac
  out=$(vale --config "$cache/.vale.ini" --output line --no-exit "$md")
  if [ -n "$ranges" ] && [ -n "$out" ]; then
    # Keep only alerts whose line (field 2) is inside one of the ranges.
    out=$(printf '%s\n' "$out" | awk -F: -v r="$ranges" '
      BEGIN { n = split(r, rr, ",")
              for (i = 1; i <= n; i++) { split(rr[i], ab, "-"); lo[i] = ab[1]; hi[i] = ab[2] } }
      { for (i = 1; i <= n; i++) if ($2 + 0 >= lo[i] && $2 + 0 <= hi[i]) { print; next } }')
  fi
  if [ -n "$out" ]; then
    # Report the original file name, not the extracted copy.
    printf '%s\n' "$out" | sed "s|^$md:|$file:|"
    if printf '%s\n' "$out" | grep -vq ':Readability\.'; then
      status=1
    fi
  fi
done
exit $status

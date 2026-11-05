#!/usr/bin/env bash
# Usage: build.sh <lib>
#
# Wraps `easifem dev <lib>`. Prints only error lines and a one-line result.
# Exits 1 on any compile or link failure, 2 on bad usage. The full log is
# kept only on failure, and its path is printed.

if [ "$#" -ne 1 ]; then
  echo "usage: build.sh <lib>" >&2
  exit 2
fi
lib=$1

log=$(mktemp "${TMPDIR:-/tmp}/easifem-build.XXXXXX") || exit 1
easifem dev "$lib" --verbose >"$log" 2>&1
rc=$?

# The exit status alone is not trusted, so the output is scanned as well.
awk '
  {
    gsub(/\033\[[0-9;?]*[A-Za-z]/, ""); sub(/\r$/, ""); sub(/^[ \t]+/, "")
  }
  /^-- / || /^[0-9]* *\|/ { next }           # CMake status, echoed source
  /:[0-9]+:[0-9]+:$/ { loc = $0; next }      # location before an Error: line
  /^(Fatal )?Error:/ || /(^|[ :])(fatal )?error:/ || /^FAILED:/ ||
  /ninja: build stopped/ || /undefined reference/ || /^CMake Error/ ||
  /^easifem: / || /\[err\]/ {
    if (loc != "") print loc
    loc = ""; print; found = 1
  }
  END { exit found ? 1 : 0 }
' "$log"
found=$?

if [ "$rc" -ne 0 ] || [ "$found" -ne 0 ]; then
  echo "build $lib: FAILED (easifem exit $rc), full log: $log"
  exit 1
fi
rm -f "$log"
echo "build $lib: ok"

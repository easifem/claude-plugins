#!/usr/bin/env bash
# Usage: run-test.sh <file> [<file> ...]
#
# Wraps `easifem run <file> --rebuild --cache-clean`, one file at a time, from
# each file's own directory (where its runner.toml lives). Prints only error
# lines and ok/not-ok counts per file. Exits 1 on any compile, link, crash or
# "not ok", 2 on bad usage. Full logs are kept only for failing files.

if [ "$#" -eq 0 ]; then
  echo "usage: run-test.sh <file> [<file> ...]" >&2
  exit 2
fi

failed=0
for file in "$@"; do
  name=$(basename "$file")
  if ! dir=$(cd "$(dirname "$file")" 2>/dev/null && pwd -P) || [ ! -f "$dir/$name" ]; then
    echo "$file: FAILED, file not found"
    failed=$((failed + 1))
    continue
  fi
  # Without runner.toml the CLI defaults write build/ here and link base only.
  if [ ! -f "$dir/runner.toml" ]; then
    echo "$file: FAILED, no runner.toml in $dir"
    failed=$((failed + 1))
    continue
  fi

  log=$(mktemp "${TMPDIR:-/tmp}/easifem-run.XXXXXX") || exit 1
  (cd "$dir" && easifem run "$name" --rebuild --cache-clean) >"$log" 2>&1
  rc=$?

  # Build patterns stop applying once the executable starts: tests may print
  # text such as "relative error: 1e-5".
  awk -v file="$file" -v rc="$rc" -v log_path="$log" '
    function report() {
      if (loc != "") print loc
      loc = ""; print; bad = 1
    }
    {
      gsub(/\033\[[0-9;?]*[A-Za-z]/, ""); sub(/\r$/, ""); sub(/^[ \t]+/, "")
    }
    /\[err\]/ { report(); next }
    /running cmd: +\[cmake / { next }
    /running cmd:/ { running = 1; next }
    !running {
      if (/^-- / || /^[0-9]* *\|/) next        # CMake status, echoed source
      if (/:[0-9]+:[0-9]+:$/) { loc = $0; next }
      if (/^(Fatal )?Error:/ || /(^|[ :])(fatal )?error:/ || /^FAILED:/ ||
          /ninja: build stopped/ || /undefined reference/ || /^CMake Error/)
        report()
      next
    }
    /^At line [0-9]+ of file / { loc = $0; next }
    /Fortran runtime error:/ || /^Program received signal/ ||
    /^ERROR STOP/ || /^Bail out!/ { report(); next }
    /^(not ok|ok)([ \t]|$)/ {
      if (toupper($0) ~ /#[ \t]*(SKIP|TODO)([ \t]|$)/) skipped++
      else if ($1 == "ok") ok++
      else { print; notok++; bad = 1 }
    }
    END {
      if (!running) bad = 1                    # the program never started
      if (rc != 0) bad = 1
      line = sprintf("%s: ok=%d not_ok=%d", file, ok, notok)
      if (skipped) line = line sprintf(" skipped=%d", skipped)
      if (bad) line = line sprintf(" FAILED (easifem exit %d), full log: %s", rc, log_path)
      print line
      exit bad ? 1 : 0
    }
  ' "$log"
  if [ "$?" -ne 0 ]; then
    failed=$((failed + 1))
  else
    rm -f "$log"
  fi
done

[ "$failed" -eq 0 ] || exit 1

---
name: fix-bug
description: >
  Use for "/fix-bug #N", "move to #12", "fix the next bug" or "mark it
  fixed" while working through GitHub bug issues of an EASIFEM library.
---

# /fix-bug

Arguments: a GitHub issue number (`#12`) in the current repository, or
"next" (the oldest open issue for the module being worked on, from
`gh issue list --state open --search "<Module>"`; prefer High, then
Medium, then Low, as given in the title).

Load `easifem-conventions`. Work on exactly one bug at a time.

## Steps

1. **Read** the issue (`gh issue view <N> --comments`) and the current
   code (it may have changed since the issue was filed).
2. **Explain** the bug briefly, starting with its location
   (`File.F90:ProcedureName`), with options `(a)`, `(b)`, `(c)` and a
   recommendation (mention performance or API impact). "Docs only" is a
   valid option. **Wait for the user's choice.**
3. **Failing test first** (unless "docs only"): add or update a
   regression test `<MethodName>_test_<N>.F90` that fails with the current
   code. If existing tests all pass, say so and write one that exposes
   the bug. Run it or ask the user to run it,
   and confirm it fails.
4. **Fix** with the chosen option. Keep the change minimal.
5. **Docs:** update the FORD docblock (behaviour, defaults, edge cases)
   and add a link to the new regression test under `Examples`. Remove any
   `! @bug` ... `! @endbug` admonition for this bug.
6. **Verify:** `fortitude check --no-fix`,
   `${CLAUDE_PLUGIN_ROOT}/scripts/build.sh <lib>`, then run the tests with
   `${CLAUDE_PLUGIN_ROOT}/scripts/run-test.sh <File>.F90 ...` (or ask the user to run
   them if they prefer) and confirm they pass.
7. **Report** what changed (one `File.F90:ProcedureName` per changed
   procedure), major/minor and downstream steps. Commit only when the user
   says so (typically "tests pass, commit and move to #<next>"). Put
   `Fixes #<N>` in the commit message so the issue closes when it reaches
   the default branch. If only part of the bug is fixed, use
   `Refs #<N>` instead and, with the user's approval, comment on the
   issue with what remains open. Then continue with the next issue by
   returning to step 1.

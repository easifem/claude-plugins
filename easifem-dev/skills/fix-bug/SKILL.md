---
name: fix-bug
description: >
  This skill should be used when the user runs "/fix-bug ID" or says
  "move to H-03", "let's start with M-01", "fix the next bug", "explain
  this bug", or "mark it fixed" while working through a bug report in
  bug-reports/ of an EASIFEM library (base, classes, elasticity, seepage,
  diffusion).
metadata:
  version: "0.4.0"
---

# /fix-bug

Arguments: a bug ID from `bug-reports/<Module>_bug_report.md` (or "next").

Load `easifem-conventions`. Work on exactly one bug at a time.

## Steps

1. **Read** the entry and the current code (it may have changed since the
   report was written).
2. **Explain** the bug briefly, with options `(a)`, `(b)`, `(c)` and a
   recommendation (mention performance or API impact). "Docs only" is a
   valid option. **Wait for the user's choice.**
3. **Failing test first** (unless "docs only"): add or update a
   regression test `<Name>_test_<N>.F90` that fails with the current
   code. If existing tests all pass, say so and write one that exposes
   the bug. Run it (install needs approval) or ask the user to run it,
   and confirm it fails.
4. **Fix** with the chosen option. Keep the change minimal.
5. **Docs:** update the FORD docblock (behaviour, defaults, edge cases)
   and re-copy the `Examples` program from the updated test.
6. **Verify:** `fortitude check --no-fix`, `easifem dev <lib>`, then run
   the tests (or ask the user to run them if they prefer) and confirm
   they pass.
7. **Update the report:** remove the resolved entry (or reduce it to what
   remains open).
8. **Report** major/minor and downstream steps. Commit only when the user
   says so (typically "tests pass, commit and move to <next ID>"); then
   continue with the next ID by returning to step 1.

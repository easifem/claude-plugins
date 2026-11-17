---
name: write-test
description: >
  This skill should be used when the user runs "/write-test" or asks to
  "write a test for a method", "add an example program", "test this
  routine", or "create a MethodName_test_N.F90 file" in an EASIFEM library (base,
  classes, elasticity, seepage, diffusion).
---

# /write-test

Arguments: the routine (or generic/type-bound method) to test, optionally
what to cover. Ask if ambiguous.

Load `easifem-conventions` and use the test template in
`references/templates.md` (full example: `references/test-example.md`).

## Steps

1. **Understand the routine.** Read its interface and implementation.
   List the behaviours to check: normal cases, edge cases (empty, zero,
   negative, boundary sizes), and mathematical identities that give exact
   expected values.
2. **Pick the file.** `src/modules/<Module>/examples/<MethodName>_test_<N>.F90`
   with the next unused `<N>`. Read one existing test there to match
   style.
3. **Write the program.**
   - Starts with the `!> author:` / `date:` / `summary:` docblock; no GPL
     header.
   - `PROGRAM main` … `END PROGRAM main`, `IMPLICIT NONE`, one item per
     `USE ..., ONLY:` line, `USE Test_Method, ONLY: OK`.
   - `CALL e%SetQuietMode(math%yes)` after the declarations (classes,
     kernels).
   - Group checks in `BLOCK ... END BLOCK`, one behaviour or method per
     block, each preceded by a `! Test N: ...` comment; shared objects
     are declared and initiated before the blocks, deallocated at the end.
   - One `CALL OK(condition, "label")` per behaviour. Compare reals with
     a tolerance (e.g. `ABS(a - b) .LT. 1.0E-10_DFP`) unless the result is
     exact.
   - Kind-overloaded routines: test `REAL(DFP)` and `INTEGER(I4B)` only.
   - Helpers after `CONTAINS`. Lines ≤ 78 characters.
   - The docblock's `Examples` links to this file, so make it readable
     on its own: a reader opens it to learn how to call the routine.
4. **Write.** Create the file, plus a `runner.toml` if the directory has none (see
   `references/running-examples.md`). More than 10 files → list them and
   wait for approval.
5. **Run.** If the library changed since the last install, run
   `easifem install <lib> --no-download` (shared install). Then run
   `${CLAUDE_PLUGIN_ROOT}/scripts/run-test.sh <File>.F90`.
6. **Report** every `OK` result. For a failure, decide whether the test
   or the routine is wrong. Fix a clearly wrong test; if the routine looks
   wrong, explain the bug and ask before changing library code beyond
   the scope of the request.

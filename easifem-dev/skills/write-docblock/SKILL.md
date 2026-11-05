---
name: write-docblock
description: >
  This skill should be used when the user runs "/write-docblock" or asks to
  "document this routine", "write the FORD docblock", "add documentation to
  a method", "fix the docblock", or "add an Examples section" for code in
  an EASIFEM library (base, classes, elasticity, seepage, diffusion).
---

# /write-docblock

Arguments: a routine, generic interface or type name (optionally a file).
Ask if ambiguous.

Load `easifem-conventions` and follow
`references/docblock-style.md` exactly.

## Steps

1. **Find the target.** Locate the `INTERFACE` (or `TYPE`) in
   `src/modules/...` and read its implementation in `src/submodules/...`
   so the Description and Formula describe what the code actually does.
2. **Find the example.** Look in `src/modules/<Module>/examples/` for a
   matching `<MethodName>_test_<N>.F90`.
   - If one exists, use its program (without its `!> author:` docblock)
     as the `Examples` program. If it is longer than 100 lines, write a
     short dummy example plus a `! Full example: <path>` line instead.
   - If none exists, say so and offer to run `/write-test` first. Do not
     invent an untested example silently; if the user wants to proceed
     anyway, mark that the example still needs a matching test.
3. **Draft.** Write the docblock: `!> author:` first line, `date:`,
   `summary:`, Description, `Changes:` (when revising an existing block,
   add a dated entry; never `update:`), `Returns:` (functions),
   `Formula:` (only real mathematics), `Examples`, `See also:`.
   No `Arguments:` section: fill missing `!!` comments on the dummy
   arguments instead. For classes, keep only one-line `!!` comments on
   bindings inside the `TYPE`.
4. **Check.** Every line ≤ 78 characters; `!>` only on the first line;
   example lines start with `! `; `USE` lines one item each; argument
   names match the interface exactly; no line in the Description starts
   with `word:`.
5. **Apply.** Make sure the repository is on a `-claude` branch, then
   write the docblock. If documenting many routines would touch more than
   10 files, list them and wait for approval first.
6. **Verify.** Docblock edits are minor changes; run
   `${CLAUDE_PLUGIN_ROOT}/scripts/build.sh <lib>`
   once at the end to confirm nothing broke. In classes, optionally run
   `formal` (see "Generating the docs" in `docblock-style.md`) and fix its
   metadata warnings. Report what was documented.

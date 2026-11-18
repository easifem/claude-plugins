---
name: write-docblock
description: >
  Use for "/write-docblock" or documenting a routine (FORD docblock,
  Examples section) in an EASIFEM library.
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
2. **Find the tests.** List them with
   `ls src/modules/<Module>/examples/<MethodName>_test_*`. Do not read
   them unless the Description needs a fact from one.
   - `Examples` is a list of links, one per test, with the repo alias,
     e.g. `! - [test 1](|classes|FEDOF/examples/Initiate_test_1.F90)`
     (see "Examples section" in `docblock-style.md`). Never copy the
     test program into the docblock.
   - If none exists, say so and offer to run `/write-test` first. If the
     user wants to proceed anyway, leave `Examples` out.
3. **Draft.** Write the docblock: `!> author:` first line, `date:`,
   `summary:`, Description, `Changes:` (when revising an existing block,
   add a dated entry; never `update:`), `Returns:` (functions),
   `Formula:` (only real mathematics), `Examples`, `See also:`.
   Put must-know constraints in `! @note` / `! @warning` blocks (see
   "Admonitions" in `docblock-style.md`), not in bold or capitals.
   No `Arguments:` section: fill missing `!!` comments on the dummy
   arguments instead. For classes, keep only one-line `!!` comments on
   bindings inside the `TYPE`.
4. **Check.** Every line ≤ 78 characters (test link lines excepted);
   `!>` only on the first line; `Examples` holds links only, no
   program; each test link uses the right repo alias and
   points to an existing file; argument
   names match the interface exactly; no line in the Description starts
   with `word:`. Reread the text against "Writing the text" in
   `docblock-style.md`: split long or two-action sentences, put the main
   action first, drop internals and parentheses that carry meaning, put
   every programming word in backticks.
5. **Apply.** Write the docblock. If documenting many routines would
   touch more than 10 files, list them and wait for approval first.
6. **Lint the prose.** Run
   `${CLAUDE_PLUGIN_ROOT}/scripts/lint-prose.sh --lines A-B <file>.F90`
   with the line range of the docblocks you wrote (see
   "Prose linting" in `docblock-style.md`). Fix every alert on lines of
   the docblocks you wrote or changed; ignore alerts elsewhere in the
   file. Passive voice may stay when the active form reads worse.
   Exit 3 means Vale is missing: skip and say so in the report.
7. **Verify.** Docblock edits are minor changes; run
   `${CLAUDE_PLUGIN_ROOT}/scripts/build.sh <lib>`
   once at the end to confirm nothing broke. In classes, optionally run
   `formal` (see "Generating the docs" in `docblock-style.md`) and fix its
   metadata warnings. Report what was documented.

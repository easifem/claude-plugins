---
name: review
description: >
  Use for "/review", "review my changes" or "is this ready to commit" in
  an EASIFEM library. Reports problems against the conventions; never
  edits.
---

# /review

Arguments: optional files or a git or jj range. Default: uncommitted
changes. In a jj repository use `jj diff` and `jj st`. Otherwise use
`git diff` and `git diff --cached`, plus untracked `.F90` files from
`git status`.

Load `easifem-conventions` with its reference files. **Read only. Do
not edit, build or run anything.**

## What to check (changed lines and new files only)

1. **Correctness.** Logic errors, wrong indices or bounds, uninitialised
   or unallocated variables, missing `DEALLOCATE`, intent violations,
   integer/real kind mixing, wrong results in the mathematics (check
   formulas against the docblock).
2. **Structure.** Interface in `src/modules`, implementation as
   `MODULE PROCEDURE` in the right `@Category` submodule; new submodule
   files listed in `CMakeLists.txt`; type-bound binding present (classes).
3. **Style.** `ONLY` on every `USE`, one item per line; kinds from
   `GlobalData`; `INTENT` on all dummies; `!!` argument comments
   (classes); `IMPLICIT NONE`; line length ≤ 78 (test link lines may be
   longer); naming per `references/naming.md` (PascalCase bindings, `obj_` procedures,
   numbered overloads, no type-suffixed names in new code); banners;
   debug guards (`[START]`/`[END]`, `[END]` before early `RETURN`,
   `modName`/`myName` inside `#ifdef DEBUG_VER`, `modName` in the
   submodule); `examples/CMakeLists.txt` not staged. Error checks
   belong in DEBUG mode only: **never** report missing release-mode
   error handling or fallbacks.
4. **Headers.** GPL header in new library files; none in test programs.
5. **Docblocks.** Rules in `docblock-style.md`: `Changes:` not
   `update:`, no `Arguments:` section, `!!` comment on every argument;
   `Examples` is a list of `|<repo>|` alias links, one per existing test
   file, with no inline program or snippet; no plain `Full example:`
   lines. Text follows "Writing
   the text" (short sentences, one idea each, main action first, no
   internals, code words in backticks); quote hard-to-read sentences.
   Emphasis uses `! @note` ... `! @endnote` admonitions, not bold or
   capitals; no `@history`; no stale `@bug` for a fixed bug. For
   changed methods, check the docs were updated in the same change
   ("Keeping docs in sync"). Run
   `${CLAUDE_PLUGIN_ROOT}/scripts/lint-prose.sh` on the changed `.F90`
   and `.md` files and report only alerts on changed lines (exit 3:
   note that Vale is missing).
6. **Tests.** Each new or changed public routine has a
   `<MethodName>_test_<N>.F90`; kind-overloaded tests use only DFP/I4B.
7. **Change size.** Classify as **major** (interface change, new field,
   new method) or **minor**, and state the required build steps
   (major in base → install base, then
   `${CLAUDE_PLUGIN_ROOT}/scripts/build.sh classes`).

If `fortitude` is available, run `fortitude check --no-fix <files>` and
include its findings. Never run it without `--no-fix` (the config has
`fix = true` and would rewrite files).

## Output

Group findings by severity: **Must fix**, **Should fix**, **Note**.
For each: the location as `File.F90:ProcedureName` (`File.F90:<line>` only
for code outside any procedure), the problem, and the suggested fix (as
text, not an edit). End with the major/minor verdict and build steps. If nothing is
wrong, say so plainly. Offer to apply the fixes.

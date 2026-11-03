---
name: review
description: >
  This skill should be used when the user runs "/review" or asks to
  "review my changes", "check this against the conventions", "is this
  ready to commit", or "review a file" in an EASIFEM library (base,
  classes, elasticity, seepage, diffusion). It reports problems and never
  edits files.
metadata:
  version: "0.4.0"
---

# /review

Arguments: optional files or a git range. Default: uncommitted changes
(`git diff` and `git diff --cached`, plus untracked `.F90` files from
`git status`).

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
   (classes); `IMPLICIT NONE`; line length ≤ 78; naming per
   `references/naming.md` (PascalCase bindings, `obj_` procedures,
   numbered overloads, no type-suffixed names in new code); banners;
   debug guards (`[START]`/`[END]`, `[END]` before early `RETURN`,
   `modName`/`myName` inside `#ifdef DEBUG_VER`, `modName` in the
   submodule); `examples/CMakeLists.txt` not staged. Error checks
   belong in DEBUG mode only: **never** report missing release-mode
   error handling or fallbacks.
4. **Headers.** GPL header in new library files; none in test programs.
5. **Docblocks.** Rules in `docblock-style.md`: `Changes:` not
   `update:`, no `Arguments:` section, `!!` comment on every argument;
   `Examples` present and matching an existing test (dummy example plus
   path for tests over 100 lines). For changed methods, check the docs
   were updated in the same change ("Keeping docs in sync").
6. **Tests.** Each new or changed public routine has a
   `<Name>_test_<N>.F90`; kind-overloaded tests use only DFP/I4B.
7. **Change size.** Classify as **major** (interface change, new field,
   new method) or **minor**, and state the required build steps
   (major in base → install base, then `easifem dev classes`).

If `fortitude` is available, run `fortitude check --no-fix <files>` and
include its findings. Never run it without `--no-fix` (the config has
`fix = true` and would rewrite files).

## Output

Group findings by severity: **Must fix**, **Should fix**, **Note**.
For each: `file:line`, the problem, and the suggested fix (as text, not an
edit). End with the major/minor verdict and build steps. If nothing is
wrong, say so plainly. Also report the current branch and warn if it does
not end in `-claude`. Offer to apply the fixes (on a `-claude` branch).

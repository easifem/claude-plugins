---
name: new-method
description: >
  This skill should be used when the user runs "/new-method" or asks to
  "add a new method", "add a routine to a module", "create a new
  procedure", or "add a type-bound procedure to a class" in an EASIFEM
  library (base, classes, elasticity, seepage, diffusion). It scaffolds the
  interface, the submodule implementation and a test program.
---

# /new-method

Arguments: `<Module or Class> <MethodName> [category]` plus a short
description of what the method should do. Ask for anything missing.

Load the `easifem-conventions` skill and its `references/templates.md`
and `references/docblock-style.md` first.

## Steps

1. **Locate.** Identify the repository and find:
   - the module file `src/modules/<Module>/src/*.F90`,
   - the submodule for the category
     `src/submodules/<Module>/src/*@<Category>.F90` (if the category file
     does not exist, plan to create it and to add it to that directory's
     `CMakeLists.txt` the same way neighbouring files are listed),
   - the examples directory `src/modules/<Module>/examples/`.
2. **Study.** Read the module and one or two existing methods in the same
   category. Follow `references/naming.md`: PascalCase binding,
   `obj_<Name>` procedure (`TypeName_<Name>` only on a name clash); if it is an overload of an existing generic,
   use the next number (`obj_Initiate3`, `obj_Get_3`) and add it to the
   `GENERIC` list. Match argument order, kinds, imports and banners.
3. **Design and confirm.** Show the proposed name, signature (arguments,
   kinds, intents, result) and algorithm in a few lines, and ask how the
   user wants it done before writing (one task at a time).
4. **Branch.** Make sure the repository is on a `-claude` branch (see
   the golden rules in `easifem-conventions`).
5. **Write.** Create or update:
   - the interface (with full FORD docblock, Examples taken from the new
     test),
   - for classes: the new binding line in `TYPE ... CONTAINS` and, if the
     method belongs to a generic, the generic binding change,
   - the `MODULE PROCEDURE` implementation,
   - the test program `<Name>_test_<N>.F90` (next unused `<N>`), plus a
     `runner.toml` if the examples directory has none
     (`references/running-examples.md`).
   If the work would touch more than 10 files, list them and wait for
   approval first.
6. **Build and test.** Run `easifem dev <lib>` and fix compile errors.
   To run the test, ask to `easifem install <lib> --no-download` (shared
   install), then from the examples directory `easifem run <test>.F90`.
   A new method is a **major** change: if `<lib>` is base, also (after
   install) run `easifem dev classes` (classes on its own `-claude`
   branch).
7. **Report.** Branch used, files changed, build/test results, and any
   remaining downstream steps.

## Checks before proposing

- Every line ≤ 78 characters; one item per `USE ..., ONLY:` line.
- All dummy arguments have `INTENT` (and `!!` comments in classes).
- GPL header present in new library files, absent from the test.
- Docblock `Examples` program is identical to the test body (or, for a
  test over 100 lines, a dummy example plus the test path).
- DEBUG guards: `[START]`/`[END]` (also before early `RETURN`), checks
  only inside `#ifdef DEBUG_VER`; a new submodule declares `modName`
  inside `#ifdef DEBUG_VER`.

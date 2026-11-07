---
name: refactor
description: >
  This skill should be used when the user runs "/refactor" or asks to
  "rename methods", "rename routines to the new convention", "change
  hdf5_ to obj_", "make method names uppercase", "renumber overloads",
  "move methods to another submodule", "split this submodule", "remove
  unused code", or otherwise restructure existing code in an EASIFEM
  library (base, classes, elasticity, seepage, diffusion) without
  changing behaviour.
---

# /refactor

Arguments: what to refactor and where (e.g. "HDF5File_Class: type-suffixed
overloads to numbered names"). Ask if the scope is unclear.

Load `easifem-conventions` with `references/naming.md`.

A refactor changes structure or names, never behaviour. Keep behaviour
changes (bug fixes, new features) out of it; note them for later.

## Phase 1: Inventory (read-only)

1. For each symbol, use LSP first: `findReferences` for type-aware
   callers, `goToImplementation` on the `obj_Name` interface for the
   submodule body. Grep cannot tell which type a `%Name(...)` call
   belongs to; LSP can.
2. Then find every remaining occurrence with `grep -rn` across **all**
   EASIFEM repositories available (base, classes, kernels): definitions,
   bindings, `GENERIC` lists, `MODULE PROCEDURE` lines, `END` lines,
   calls, docblocks, `See also: [[...]]`, tests, kernel examples, and
   `CMakeLists.txt` entries. LSP does not cover comments, CMake files,
   excluded paths such as `examples/`, or repositories outside
   `.fortlsrc`. For a grep hit on `%Name(...)` that LSP did not report,
   check the receiver's type before treating it as a caller.
3. Classify callers: through the public generic (unaffected by renaming
   specifics) vs. direct references (must change).

## Phase 2: Plan and approval

Present to the user:

- a **mapping table** old → new for every name (for overload renumbering,
  keep the existing order of the generic list unless told otherwise),
- the list of files to change, grouped by repository, with the count,
- open questions (helpers inside generics, order, docs wording),
- major/minor classification and the build steps afterwards.

If more than 10 files are involved (usual for refactors), wait for explicit
approval. Even when fewer, wait if any naming choice is ambiguous.

## Phase 3: Apply

1. Apply mechanically from the approved mapping. Prefer a small script
   (word-boundary regex, applied to the listed files only) over many manual
   edits; show the script before running it if it touches many files.
   Rename longer names first so prefixes don't collide
   (`obj_Read__d1` before `obj_Read_d1`).
2. Update docblocks, `!!` comments, `See also:` links and banners.
3. Keep line length ≤ 78 after renaming; rewrap continuation lines.
4. Do not change logic, argument lists or formatting elsewhere.

## Phase 4: Verify

1. `grep` again: no old names left (report any intentional leftovers).
2. `fortitude check --no-fix` on changed files.
3. `${CLAUDE_PLUGIN_ROOT}/scripts/build.sh <lib>`. Renaming specific procedures is a major
   change: if it is base, install base and then run
   `${CLAUDE_PLUGIN_ROOT}/scripts/build.sh classes`.
4. Tests: install, run the affected tests with
   `${CLAUDE_PLUGIN_ROOT}/scripts/run-test.sh <File>.F90 ...`, report.
5. Report: mapping applied, changes as `File.F90:ProcedureName`,
   build/test results.
   Commit only when the user asks (one commit per module).

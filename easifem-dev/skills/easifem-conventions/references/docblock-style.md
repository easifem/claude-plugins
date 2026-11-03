# FORD docblock style

Applies to the docblock above each `INTERFACE` (and each `TYPE`).

## Comment markers

- `!>` starts a docblock (first line only).
- `!!` documents the item directly above it (dummy argument, component,
  binding).
- External page: `!{!pages/docs-api/Module/topic.md!}`.
- Section markers inside a module: `! @SectionName`.

## Structure

1. `!>` only on the first line. All following lines use plain `!`.
2. First line: `!> author: Vikas Sharma, Ph. D.` (singular `author`,
   never `authors`). Use the actual author if someone else wrote the
   routine. No title lines (`!> Subroutine: name`, `!# Initiate`, ...).
3. Fields: `date:` and `summary:` (both mandatory). Long summaries
   continue on an indented `!` line. **No `update:` field**; FORD does
   not recognise it. Record changes in a `Changes:` list (item 4).
4. Sections, in order (omit only if not applicable):
   - Description — plain paragraphs: what it does, algorithm steps,
     rules it follows. Always comes first, before `Changes:`.
   - `Changes:` — only when the routine changed after its first version;
     list `!   - YYYY-MM-DD: description`, newest last.
   - `Returns:` — functions only.
   - `Formula:` — only for real mathematics (data layout, index rules);
     LaTeX display `$$ ... $$`, simple commands only.
   - `Examples`
   - `See also:` — `[[ProcName]]` links.
5. **No `Arguments:` section.** Each dummy argument is documented by a
   `!!` comment directly below its declaration, including array sizes
   and active ranges. Fill in missing ones. These comments are the only
   source of truth for argument meaning.
6. Wrap every line to ≤ 78 characters.
7. Be factual. When adapting text from another routine, fix argument
   names, called methods and banners.
8. Avoid Description lines that start with `word:`; FORD reads them as
   header fields.

### classes specifics

- Type-bound procedures: full docblock on the `INTERFACE` of the specific
  procedure (`obj_XXX`); inside `TYPE ... CONTAINS` each binding has only a
  one-line `!!` comment.
- The `TYPE` itself gets a docblock describing its components and layout;
  each component has a `!!` comment.

## File header docblock

After the GPL header of a library file (none in test programs):

```fortran
!> author: Vikas Sharma, Ph. D.
! date: YYYY-MM-DD
! summary: Module description
!
! Changes:
! - YYYY-MM-DD: Description of the change
```

## Examples section

- Exactly one section per docblock, written `! Examples` on its own line
  (never `Example`, no extra short `Example:` snippet).
- A complete runnable program: `PROGRAM main` … `END PROGRAM main` with all
  `USE ..., ONLY:` lines (one item per line), `IMPLICIT NONE`,
  declarations, calls, and `CALL OK(...)` checks from `Test_Method`.
- Fenced with `` !```fortran `` and `` !``` `` on their own lines; every
  line inside starts with `!` (plain `!` + one space), never `!>`.
- Normally identical to the matching test in
  `src/modules/<Module>/examples/`, minus its `!> author:` docblock (and
  minus any GPL header). Helpers go after `CONTAINS` inside the program.
- **Exception — long tests.** When the test program is longer than 100
  lines, write a short "dummy example" instead: the minimal code that
  shows the call, not meant to run by copy and paste. Below it, give the
  full test path:
  `! Full example: src/modules/<Module>/examples/<MethodName>_test_<N>.F90`.
- Kind-overloaded routines: example uses `REAL(DFP)` / `INTEGER(I4B)` only.
- Generic interfaces (`Initiate`, `Set`, `Insert`, ...): one example per
  distinct use case, not per specific procedure; thin wrappers point to
  the main one via `See also:`.
- Use only the current API. Do not copy old examples that use removed APIs
  (e.g. `ParameterList_`-based initiation) without updating them.

## Keeping docs in sync with code

Whenever a method changes, update its documentation in the same change.
A change is not complete while its docs describe the old behaviour. This
covers interface changes (arguments added, removed, renamed; intent,
optional, defaults) and behaviour changes (algorithm, modes, checks,
errors, return values). Update everything affected:

- the `INTERFACE` docblock (Description, `Returns:`, `Formula:`,
  `See also:`) plus a new `Changes:` entry;
- the `!!` comments of the dummy arguments;
- the one-line `!!` comment of the binding in `TYPE ... CONTAINS`;
- the `TYPE` docblock and component `!!` comments when defaults or the
  meaning of components change;
- the `Examples` program and the matching test (keep both the same);
- examples, docs and tests of other methods that call or refer to the
  changed method (renamed binding, new required argument);
- section banners (`!---` blocks) when a procedure is renamed.

Afterwards `grep` the module, submodules and examples for the old name or
removed argument. If some docs or tests are left for later, say so
explicitly in the report.

Do not list documentation updates in the report; they are expected with
every change. Report code and behaviour changes, checks run, and open
questions (including docs or tests not updated).

## Template

```fortran
!> author: Vikas Sharma, Ph. D.
! date: 2026-01-01
! summary: Short summary of the routine
!
! Longer description. Wrap lines to 78 characters.
!
! Changes:
!   - 2026-02-01: Added optional argument w
!
! Returns:
!   ans : REAL(DFP) - weighted sum
!
! Formula:
!   $$ ans = \sum_{i=1}^{n} x_i w_i $$
!
! Examples
!
!```fortran
! PROGRAM main
! USE GlobalData, ONLY: DFP
! USE SomeModule, ONLY: SomeFunction
! USE Test_Method, ONLY: OK
! IMPLICIT NONE
!
! REAL(DFP) :: x(3)
!
! x = [1.0_DFP, 2.0_DFP, 3.0_DFP]
! CALL OK(SomeFunction(x) .GT. 0.0_DFP, "SomeFunction is positive")
!
! END PROGRAM main
!```
!
! See also: [[RelatedRoutine]]

INTERFACE
  MODULE FUNCTION SomeFunction(x, w) RESULT(ans)
    REAL(DFP), INTENT(IN) :: x(:)
    !! input values, SIZE(x) = n
    REAL(DFP), OPTIONAL, INTENT(IN) :: w(:)
    !! weights, SIZE(w) = SIZE(x); default 1
    REAL(DFP) :: ans
    !! weighted sum
  END FUNCTION SomeFunction
END INTERFACE
```

## Generating the docs (classes)

```bash
formal generate --project doc/formal.md
```

- Needs no library build. Pages go to `docs/api/` (git-ignored).
- Only modules listed in `src_dir` of `doc/formal.md` are documented.
  When documenting a module, add `../src/modules/<Module>/` to `src_dir`
  if missing, and say so in the report.
- Check the warnings. "Ignoring unknown Ford metadata key" means a line
  was read as a header field: first line must be `!> author:`, the
  Description must come before `Changes:` / `Returns:`, and no
  Description line may start with `word:`.

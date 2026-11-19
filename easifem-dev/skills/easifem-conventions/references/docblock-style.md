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
6. Wrap every line to ≤ 78 characters (except test link lines, see
   "Examples section").
7. Be factual. When adapting text from another routine, fix argument
   names, called methods and banners.
8. Avoid Description lines that start with `word:`; FORD reads them as
   header fields.

## Writing the text

Write for a person reading the docs for the first time. Plain,
human-readable English matters more than squeezing in every fact.

- **Short sentences, one idea each.** Aim for 15 words or fewer. If a
  sentence has "or", "and" or a comma joining two actions, split it.
- **Main action first.** The first sentence says what the routine does
  for the caller. Conditions and special cases come after, each in its
  own sentence ("If addContribution is true, ...").
- **Active voice, plain verbs.** "Sets", "adds", "returns", not "become",
  "is added", "denote".
- **No parentheses carrying meaning.** Move the content into its own
  sentence.
- **Steps as a numbered list**, one step per item, when the routine does
  several things in order.
- **Code in backticks.** Every programming word goes in backticks:
  argument, variable and component names (`nbcField`, `obj`, `scale`),
  type names (`VectorField_`), procedures (`Set`, `lis_vector_copy`),
  component access (`obj%nbc_point`), keywords and literals (`.TRUE.`,
  `"HIER"`), and expressions (`scale * VALUE`). Plain English words stay
  plain: "the field", "each node". `[[...]]` FORD links need no
  backticks.
- **Explain a term the first time** it appears, or link it with `[[...]]`.
- **Leave out internals** the caller does not need (which helper it
  calls, order of internal loops). Mention a called method only in
  `See also:`.
- **Reread before finishing.** If a sentence needs a second reading,
  rewrite it.

Before:

```fortran
! All values (all components of all nodes) become scale * VALUE, or
! scale * VALUE is added with addContribution. It calls SetAll of
! AbstractNodeField_.
```

After:

```fortran
! Sets every value of the field to `scale * VALUE`.
! This covers all components at all nodes.
!
! If `addContribution` is true, it adds `scale * VALUE` to the current
! values instead.
!
! See also: [[AbstractNodeField_:SetAll]]
```

## Prose linting

`${CLAUDE_PLUGIN_ROOT}/scripts/lint-prose.sh <file> [...]` checks the
text with Vale. It takes `.F90` files (docblock and `!!` prose only,
line numbers match the source) and `.md` files. Output is one alert per
line: `file:line:col:rule:message`. On large files pass
`--lines A-B[,C-D...]` to report only the lines you edited.

| Rule | Checks |
|---|---|
| `EASIFEM.SentenceLength` | sentence over 20 words |
| `EASIFEM.CodeSpan` | camelCase, `snake_case`, `Type_`, `a%b`, `f()` outside backticks |
| `EASIFEM.Parens` | long aside in parentheses |
| `write-good.Passive` | passive voice |
| `write-good.So`, `write-good.ThereIs` | weak sentence openings |
| `Readability.FleschReadingEase` | file-level score; information only |

- Fix alerts on the lines you wrote or changed. Leave the rest of the
  file alone unless asked.
- Passive voice may stay when the active form reads worse.
- `CodeSpan` cannot see plain lowercase names (`obj`, `scale`); put
  those in backticks by hand.
- Exit codes: 0 clean, 1 alerts, 2 bad usage, 3 Vale missing or its
  styles could not be synced. On 3, skip the check and say so.

Vale only checks the mechanics. Main action first, no internals and
explained terms still need a careful reread.

## Admonitions

Use FORD admonitions for text the reader must not miss. Do not use bold
or capitals for emphasis.

| Admonition | Use for |
|---|---|
| `@note` | a constraint or surprising behaviour the caller must know |
| `@warning` | misuse that gives wrong results, a crash or lost data |
| `@bug` | a known bug not yet fixed; give its issue if one exists (`easifem/base#12`) |
| `@todo` | planned work that changes how the routine is used |

Do not use `@history`; changes go in `Changes:`.

Format: the opening and closing markers on their own lines, written
`! @note` and `! @endnote` (one space after `!`, like other lines).

```fortran
! @note
! `obj` and `VALUE` can be the same field. The two ranges must not
! overlap.
! @endnote
```

- Place an admonition in the Description, right after the paragraph it
  belongs to, and before `Changes:`.
- One point per admonition. Follow "Writing the text" inside it.
- Use them sparingly, at most two or three per docblock. Do not repeat
  the main description in a note: "Without `addContribution`, the
  values are set to `scale * VALUE`" belongs in the Description.
- Add `@bug` or `@todo` only when the user asks or a bug report lists
  the issue. Remove it in the same change that fixes the bug.

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

The tests are the examples. The docblock links to them and never
copies their code: an inline program doubles the size of the module
file and of the context needed to read it.

- Exactly one section per docblock, written `! Examples` on its own line
  (never `Example`).
- **Links only.** No inline program, no fenced code, no short snippet.
- One list item per matching test file `<MethodName>_test_<N>.F90`:
  `! - [test 1](|classes|FEDOF/examples/Initiate_test_1.F90)`.
  Link text is `test <N>`, the number of the test file. A short phrase
  saying what the test shows may follow:
  `! - [test 2](|classes|FEDOF/examples/Initiate_test_2.F90) with order 3`.
- The alias is the repository name (`|base|`, `|classes|`,
  `|elasticity|`, `|seepage|`, `|diffusion|`) and points to that
  repository's `src/modules/`, so the path starts at the module folder.
  Use the alias of the repository the file lives in.
- Always inline links; no reference-style links (`[test 1][label]`),
  because `formal` puts a whole module on one page and labels clash.
  Do not write plain `Full example: <path>` lines.
- A link line may exceed 78 characters when the path is long; it is the
  only exception to the line limit.
- Every link must point to an existing file. No matching test: leave
  `Examples` out and say so (offer `/write-test`). Never put an inline
  program in its place.
- Generic interfaces (`Initiate`, `Set`, `Insert`, ...): link the tests
  of each use case on the main specific procedure; thin wrappers point
  to it via `See also:`.
- Older docblocks may still hold an inline program. When you rewrite
  such a docblock, replace the program with links. Do not touch other
  docblocks only for this unless asked.

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
- the `Examples` links (add new tests, drop removed ones) and the
  matching tests;
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
! @note
! `w` must have the same size as `x`.
! @endnote
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
! - [test 1](|base|SomeModule/examples/SomeFunction_test_1.F90)
! - [test 2](|base|SomeModule/examples/SomeFunction_test_2.F90) with weights
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
formal generate --project ford.md --output docs/api
```

- Run it from the repository root. Needs no library build. Pages go to
  `docs/api/` (git-ignored).
- Only modules listed in `src_dir` of `ford.md` are documented. When
  documenting a module, add `src/modules/<Module>/src/` to `src_dir` if
  missing, and say so in the report.
- Check the warnings. "Ignoring unknown Ford metadata key" means a line
  was read as a header field: first line must be `!> author:`, the
  Description must come before `Changes:` / `Returns:`, and no
  Description line may start with `word:`.

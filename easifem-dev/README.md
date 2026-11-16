# easifem-dev

Claude plugin for developing and refactoring the EASIFEM Fortran finite
element libraries: easifemBase (base), easifemClasses (classes) and the
independent kernels elasticity, seepage and diffusion.

Author: Vikas Sharma, Ph. D. — <https://www.easifem.com> — License: GPL-3.0

## Components

| Component | Type | What it does |
|---|---|---|
| `easifem-conventions` | Skill (automatic) | Working style, approval rules, build commands, major/minor rules, code style, naming, HDF5 layout, linting. References: naming, running examples (`runner.toml`), templates and debug rules, a complete test example, FORD docblocks (incl. keeping docs in sync and `formal` doc generation). |
| `/new-method` | Skill | Scaffolds interface + docblock, submodule `MODULE PROCEDURE`, test and `runner.toml`. |
| `/write-docblock` | Skill | FORD docblock whose `Examples` program comes from the matching test. |
| `/write-test` | Skill | `<MethodName>_test_<N>.F90` with `CALL OK` checks; runs it. |
| `/review` | Skill | Read-only review of changes against the conventions, with a major/minor verdict. |
| `/refactor` | Skill | Inventory → mapping table → approval → mechanical rename/restructure → verify. |
| `/bug-report` | Skill | Writes `bugs-report/<Module>_bug_report.md` with H/M/L entries. |
| `/fix-bug` | Skill | One bug at a time: explain with options → failing test → fix → docs → report update. |
| `cookbook-writer` | Agent | Drafts or fixes entries in `../cookbook` following its `CLAUDE.md`, modelled on `recipes/fedof-h1-hierarchical.md`. Reads the library repos, never edits them. |
| Command guard | Hook | Denies `easifem install` without `--no-download`, and git write commands in a jj repository. Asks before `easifem clean`, deleting files, commit, push, merge, rebase, hard reset, branch deletion, global git config, and `fortitude check` without `--no-fix`. For jj, also asks before `abandon`, `restore`, `op restore`, `op abandon`, `op revert`, changing or deleting bookmarks, `config --user` and `util gc`. |
| LSP guidance | Hook | At session start, in a project root with a `.fortlsrc`, `.fortls.json` or `.fortls`, tells Claude to use LSP before grep for Fortran symbol lookups. Prints nothing elsewhere. |
| `scripts/build.sh` | Script | Wraps `easifem dev <lib>`. Prints only error lines and exits 1 on any compile or link failure. |
| `scripts/run-test.sh` | Script | Wraps `easifem run` for one or more files, each from its own directory. Prints only error lines and `ok`/`not ok` counts per file, and exits 1 on any compile, link, crash or `not ok`, or if `runner.toml` is missing. |
| `zfls` | LSP server | Fortran code intelligence for `.F90` and `.f90` files (`.lsp.json`). |

## Working rules built in

- One task at a time; explain options and let the user choose.
- Allowed without asking: edits, `scripts/build.sh <lib>`,
  `scripts/run-test.sh <File>.F90`, `easifem install <lib> --no-download`.
- Asks first: more than 10 files in one task, clean, deletes, commits (unless asked), push, merge.
- Major change = changed method interface, new field, or new method.
  Major in base → install base, then `scripts/build.sh classes`. Kernels are
  compiled only when being worked on.
- Overloads are numbered (`obj_Initiate1`, `obj_Get_1`), never named by
  type.
- `fortitude check --no-fix` only; never commit `examples/CMakeLists.txt`.
- `easifem run` and `easifem dev` can report success on failure, so the
  scripts check the output as well as the exit status. On failure they
  print the path of the full log.
- `easifem clean` deletes the install too, not just the build.

## Setup

- Requires the `easifem` CLI on PATH, plus `python3` for hooks.
- Requires `zfls` on PATH for Fortran code intelligence.
- Each repository's own `AGENTS.md` still applies.

## Usage

- `/new-method AbstractMesh_ GetBoundingBox GetMethods`
- `/write-docblock obj_GetRank`
- `/write-test ARTH`
- `/review`
- `/refactor HDF5File_Class: numbered overload names`
- `/bug-report SortUtility` then `/fix-bug H-01`
- "Write a cookbook recipe for FEDOF L2 DOFs" (runs `cookbook-writer`)

## Cookbook writer

The `cookbook-writer` agent drafts new entries in the EASIFEM cookbook
or fixes existing ones. Claude delegates to it when you ask for a
cookbook entry. Name the agent to be sure:

- "Use the cookbook-writer agent to write a recipe for FEDOF L2 DOFs"
- "Add a theory note on hierarchical bases"
- "The FEDOF recipe is wrong about tsize, fix it"

Run the session from a library repo (`base`, `classes`, `elasticity`,
`seepage`, `diffusion`) or from `cookbook`. The agent looks for the
cookbook at `<repo root>/../cookbook` and stops if it is not there.

What it does:

1. Reads `cookbook/CLAUDE.md` (its rules win) and the format model
   `recipes/fedof-h1-hierarchical.md`.
2. Looks for an existing entry in `INDEX.md`, `recipes/` and
   `theory/`, and updates it rather than adding a duplicate.
3. Regenerates `api-index/<repo>/INDEX.md` with
   `scripts/gen_api_index.py` if it is missing or older than the
   sources.
4. Checks every detail against current code and tests, using LSP
   first and grep as a fallback. Snippets are trimmed from real test
   programs. Numbers come from `CALL OK(...)` checks or the code;
   anything it cannot trace is left out or marked `(unverified)`.
5. Writes `recipes/<topic>.md` or `theory/<topic>.md` and updates
   `INDEX.md`.
6. Final checks: no line over 78 characters, no local paths
   (`/home/`, `Dropbox`, `~/`), every `<repo>:<path>` link resolves,
   and the entry is listed in `INDEX.md`.

Limits:

- Never edits the library repos. Writes only under `cookbook/`, and
  does not build or run examples.
- Never commits, describes, pushes or moves bookmarks. Review the
  result and run `jj describe` yourself.
- Cannot ask questions while it runs. If the request is vague, it
  writes only what it is sure of and lists open questions. Name the
  repo, say recipe or theory note, and give the scope.

It reports the files it changed, the source checked for each claim,
claims left out or marked `(unverified)`, disagreements between
entries and code, open questions, and the results of the final checks.

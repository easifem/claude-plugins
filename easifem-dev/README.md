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
| Command guard | Hook | Denies `easifem install` without `--no-download`. Asks before `easifem clean`, deleting files, commit, push, merge, rebase, hard reset, branch deletion, global git config, and `fortitude check` without `--no-fix`. |
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

# Running examples and tests

## Where examples live

- base, classes: `src/modules/<Module>/examples/<MethodName>_test_<N>.F90`.
- Kernels (elasticity, seepage, diffusion):
  `examples/<Kernel>/<example-N>/main.F90` with `config.toml`, a `mesh/`
  subdirectory (its own `runner.toml`), and other inputs. seepage also has
  `tests/<Kernel>/testN/`.

## runner.toml (required in practice)

`easifem run` reads `runner.toml` from the current directory. Without it
the CLI defaults are wrong for EASIFEM tests: `BuildDir = "build"` (a
`build/` folder inside the examples directory), `BuildType = "Release"`,
`TargetLibs = ["easifemBase"]` (classes/kernel programs fail to link).
So always make sure one exists:

```toml
BuildType = "Debug"
BuildDir = "/tmp/easifemClasses/MeshField/"
TargetLibs = ["easifemClasses"]
```

| Key | Value |
|---|---|
| `BuildType` | `"Debug"` (keys are matched case-insensitively, so the old `Buildtype` in base also works; prefer `BuildType`) |
| `BuildDir` | scratch dir under `/tmp`, one per module/example: `/tmp/<LibName>/<Module>/` or `/tmp/<kernel>/examples/<Kernel>/<example-N>/` |
| `TargetLibs` | `["easifemBase"]`, `["easifemClasses"]`, `["easifemElasticity"]`, ... — the library the program uses. Mesh-generation programs in kernel `mesh/` dirs use `["easifemClasses"]`. |

Optional keys (rarely needed): `ExtraFileNames` (extra source files
compiled into the same executable), `ExtraLibs`, `ExtraCMakePrefixPath`,
`TargetName` (default `main.out`).

Before running in a directory without `runner.toml`, create one in this
format (it counts as a file change), copying the closest existing
`runner.toml` in the same repository, and tell the user.

## Running

```bash
cd src/modules/<Module>/examples
easifem run <MethodName>_test_<N>.F90
# run batch test:
easifem test <Examples directory path>
```

- The installed library is what gets linked: after library changes, ask
  to `easifem install <lib> --no-download` first.
- After an interface change, use `easifem run --rebuild <File>.F90`
  (cleans the build dir first) or `touch` the test source; otherwise stale
  objects are re-linked and the program crashes. `--cache-clean` re-runs
  CMake from scratch; `--no-run` only builds.
- `easifem run a.F90 b.F90` compiles both files into **one** executable;
  to run several tests, loop over them one at a time.
- **Do not trust the exit status.** `easifem run` returns success even
  when compilation fails or the program crashes. Read the output: look
  for `Error`, `error:`, `FAILED:`, `ninja: build stopped`, `not ok`,
  backtraces.
- `easifem run` regenerates `examples/CMakeLists.txt`; never commit it.
- Report `ok` / `not ok` counts per file, and the failing labels.

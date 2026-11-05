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
${CLAUDE_PLUGIN_ROOT}/scripts/run-test.sh src/modules/<Module>/examples/<MethodName>_test_<N>.F90
# run batch test:
easifem test <Examples directory path>
```

- The installed library is what gets linked: after library changes,
  run `easifem install <lib> --no-download` first.
- `run-test.sh` runs `easifem run <File> --rebuild --cache-clean` from the
  file's own directory, so stale objects are not a concern. It runs each
  file as its own executable, in turn.
- It prints only error lines and `ok`/`not ok` counts per file, and exits 1
  on any compile, link, crash or `not ok`, or if `runner.toml` is missing.
  On failure it prints the path of the full log; read that for backtraces.
- `easifem run` regenerates `examples/CMakeLists.txt`; never commit it.
- Report `ok` / `not ok` counts per file, and the failing labels.

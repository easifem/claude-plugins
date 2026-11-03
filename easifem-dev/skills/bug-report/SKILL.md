---
name: bug-report
description: >
  This skill should be used when the user runs "/bug-report" or asks to
  "generate a bug report", "write up the bugs you found", "report unused
  code", "save the report in bugs-report", or "update the bug report" for
  an EASIFEM library (base, classes, elasticity, seepage, diffusion).
---

# /bug-report

Arguments: the module or class, and the source of findings (this
conversation, a code read, a review). Ask if unclear.

## Location and format

- Directory: `bugs-report/` at the repository root (git-ignored; if the
  directory or the ignore entry is missing, propose adding them).
- File: `bugs-report/<Module>_bug_report.md` (or
  `<Module>-<topic>.md`, e.g. `UStfemLinearElasticity_Class-unused-code.md`).
- Keep only open entries; resolved entries are removed when fixed.

Entry IDs by severity: `H-01`, `H-02`, … (High: wrong results, crashes,
memory errors), `M-01`, … (Medium: wrong edge cases, misleading
interfaces, inconsistent behaviour), `L-01`, … (Low: missing overloads,
style, lint, docs). Never reuse an ID in the same report.

Each entry:

```markdown
### H-01 — <short title>

- **Where:** `src/.../File.F90:<line>` (`ProcedureName`)
- **Problem:** what is wrong and when it happens.
- **Evidence:** minimal input / failing test idea / reasoning.
- **Suggested fix:** options (a), (b) … with a recommendation.
```

## Steps

1. Collect findings. If the user said to use the conversation only, do
   not re-read the code.
2. Write or update the report (new IDs continue after the highest
   existing one). Ensure the branch rule from `easifem-conventions`.
3. Show a summary table (ID, title, location) to the user.
4. Do not fix anything here; fixing is `/fix-bug <ID>`.

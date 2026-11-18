---
name: bug-report
description: >
  Use for "/bug-report" or requests to file found bugs or unused code
  as GitHub issues in an EASIFEM library repository.
---

# /bug-report

Arguments: the module or class, and the source of findings (this
conversation, a code read, a review). Ask if unclear.

Files one GitHub issue per finding with `gh`, in the repository of the
current library (`gh repo view --json nameWithOwner`). The fields match
the org issue form `easifem/.github/ISSUE_TEMPLATE/bug_report.yml`, so
issues from people and from Claude look the same.

## Title

```text
[<UserType>] <Module>: <Severity>: <short title>
```

- `<UserType>`: the type name without the trailing `_` (`Mesh_` →
  `Mesh`). Drop `[<UserType>] ` when the module has no type (many base
  modules): `SortUtility: Low: <short title>`.
- `<Module>`: the module name (`Mesh_Class`, `SortUtility`).
- `<Severity>`:
    - `High`: wrong results, crashes, memory errors.
    - `Medium`: wrong edge cases, misleading interfaces, inconsistent
      behaviour.
    - `Low`: missing overloads, style, lint, docs, unused code.
- Short title: what is wrong, in a few words, no final period.

Example: `[Mesh] Mesh_Class: High: GetNodeCoord returns wrong size for mixed meshes`

## Label

One label only: the UserType (`Mesh`), or the module name when there is
no type (`SortUtility`). No `bug` label. Labels belong to each
repository: check with `gh label list --search <Label>` and create a
missing one with `gh label create <Label>`.

## Body

```markdown
### Location

`File.F90:ProcedureName` (`File.F90:<line>` only for code outside any
procedure; see "Reporting code locations" in `easifem-conventions`)

### Problem

What is wrong and when it happens.

### Minimal reproducer

Fortran code, a failing test idea, or the reasoning.

### Expected vs actual

What should happen and what happens.

### Suggested fix

Options (a), (b) … with a recommendation. Write "None" if there is none.

### Environment

Compiler and version, OS, commit (`git rev-parse --short HEAD`).
```

## Steps

1. Collect findings. If the user said to use the conversation only, do
   not re-read the code.
2. Check for duplicates: `gh issue list --state open --search "<Module>"`.
   Mention any open issue that already covers a finding and skip it.
3. Show the proposed issues as a table (title, label, location) and
   wait for approval. Creating issues is outward-facing; never skip
   this step.
4. Create the missing labels, then each issue with
   `gh issue create --title ... --label ... --body-file <file>` (body
   file in the scratchpad).
5. Report the issue numbers and links.
6. Do not fix anything here; fixing is `/fix-bug #<number>`.

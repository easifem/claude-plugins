#!/usr/bin/env python3
"""PreToolUse hook for file edits.

Denies edits to files inside an EASIFEM git repository unless the current
branch name ends in '-claude'. Files outside EASIFEM repositories are not
affected.
"""
import json
import os
import subprocess
import sys


def git(cwd, *args):
    try:
        out = subprocess.run(["git", "-C", cwd, *args],
                             capture_output=True, text=True, timeout=5)
    except Exception:
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    ti = payload.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("notebook_path") or ""
    if not path:
        return 0
    if not os.path.isabs(path):
        path = os.path.join(payload.get("cwd") or os.getcwd(), path)
    d = os.path.dirname(path)
    while d and not os.path.isdir(d):
        d = os.path.dirname(d)
    if not d:
        return 0
    top = git(d, "rev-parse", "--show-toplevel")
    if not top:
        return 0
    remote = git(top, "remote", "get-url", "origin")
    if "easifem" not in (top + " " + remote).lower():
        return 0
    branch = git(top, "branch", "--show-current")
    if branch.endswith("-claude"):
        return 0
    name = branch or "a detached HEAD"
    reason = (f"easifem-dev: {top} is on {name}. Edits are allowed only on "
              f"a branch ending in '-claude'. Run `git switch -c "
              f"{(branch or 'work')}-claude` (or switch to the existing "
              f"one), tell the user, then retry.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""PreToolUse hook for shell commands.

`easifem dev`, `easifem run` and `easifem install --no-download` are
allowed. Denies `easifem install` without --no-download, and git write
commands inside a jj repository. Asks the user before `easifem clean`,
file deletion and risky git and jj commands.
"""
import json
import os
import re
import shlex
import sys

SEP = r"(?:^|[\s;&|()`'\"])"
# `git` or `jj` plus any global options before the subcommand
GIT = SEP + r"git(?:\s+-[Cc]\s+\S+|\s+--[\w-]+(?:=\S+)?)*\s+"
JJ = SEP + r"jj(?:\s+-[^\s;&|]+(?:\s+[^\s;&|-][^\s;&|]*)?)*\s+"

RULES = [
    (SEP + r"easifem\s+clean\b", "easifem clean"),
    (SEP + r"(?:rm|rmdir|unlink)\s", "deleting files"),
    (GIT + r"commit\b", "git commit"),
    (GIT + r"push\b", "git push"),
    (GIT + r"merge\b", "git merge"),
    (GIT + r"rebase\b", "git rebase"),
    (GIT + r"reset\s+[^;&|]*--hard\b", "git reset --hard"),
    (GIT + r"branch\s+[^;&|]*-[dD]\b", "deleting a branch"),
    (GIT + r"(?:clean|stash\s+drop)\b", "discarding git changes"),
    (GIT + r"config\s+[^;&|]*--global\b", "global git config"),
    (SEP + r"fortitude\s+check\b(?![^;&|]*--no-fix)", "fortitude check without --no-fix (rewrites files)"),
]

JJ_RULES = [
    (JJ + r"commit\b", "jj commit"),
    (JJ + r"git\s+push\b", "jj git push"),
    (JJ + r"rebase\b", "jj rebase"),
    (JJ + r"abandon\b", "jj abandon"),
    (JJ + r"restore\b", "jj restore (discards changes)"),
    (JJ + r"(?:operation|op)\s+(?:restore|abandon|revert)\b", "changing jj operation history"),
    (JJ + r"(?:bookmark|b)\s+(?:delete|d|forget|f|move|m|set|s|rename|r|advance|a)\b", "changing a jj bookmark"),
    (JJ + r"config\s+(?:set|unset|edit)\s+[^;&|]*--user\b", "global jj config"),
    (JJ + r"util\s+gc\b", "jj util gc"),
]

# git commands that write to a repository. In a jj repository use jj.
GIT_WRITE = GIT + (
    r"(commit|checkout|switch|rebase|reset|merge|cherry-pick|revert|pull"
    r"|push|am|restore|clean|stash(?!\s+(?:list|show)\b))\b"
)
JJ_INSTEAD = {
    "commit": "jj commit -m, or jj describe -m then jj new",
    "checkout": "jj new <rev> or jj edit <rev>",
    "switch": "jj new <rev> or jj edit <rev>",
    "rebase": "jj rebase",
    "reset": "jj restore, jj abandon or jj undo",
    "merge": "jj new <rev1> <rev2>",
    "cherry-pick": "jj duplicate",
    "revert": "jj revert",
    "pull": "jj git fetch",
    "push": "jj git push",
    "restore": "jj restore",
    "clean": "jj restore",
    "stash": "jj new (changes stay in their own change)",
}


def strip_quoted(command: str) -> str:
    """Remove heredoc bodies and quoted text, such as commit messages."""
    text = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?^\s*\1\s*$", " ", command,
                  flags=re.S | re.M)
    return re.sub(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"", " ", text)


def in_jj_repo(path: str) -> bool:
    path = os.path.abspath(path)
    while True:
        if os.path.isdir(os.path.join(path, ".jj")):
            return True
        parent = os.path.dirname(path)
        if parent == path:
            return False
        path = parent


def targets_jj_repo(command: str, cwd: str) -> bool:
    """True if the command runs in a jj repository.

    A `cd` or `git -C` in the command takes priority over the session's
    working directory.
    """
    dirs = re.findall(r"(?:\bcd|\bgit\s+-C)\s+(\S+)", command)
    dirs = [os.path.expanduser(d.strip("'\"")) for d in dirs]
    return any(in_jj_repo(os.path.join(cwd, d)) for d in dirs or [cwd])


def is_jj_merge(command: str) -> bool:
    """True for `jj new` with two or more parents, which is a merge."""
    for m in re.finditer(JJ + r"new\b([^;&|]*)", command):
        try:
            args = shlex.split(m.group(1))
        except ValueError:
            continue
        parents, skip = 0, False
        for arg in args:
            if skip:
                skip = False
            elif arg in ("-o", "--onto", "-r"):
                parents, skip = parents + 1, True
            elif arg in ("-m", "--message", "-A", "--insert-after",
                         "--after", "-B", "--insert-before", "--before"):
                skip = True
            elif not arg.startswith("-"):
                parents += 1
        if parents >= 2:
            return True
    return False


def respond(decision: str, reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not isinstance(command, str):
        return 0
    m = re.search(SEP + r"easifem\s+install\b([^;&|]*)", command)
    if m and "--no-download" not in m.group(1):
        respond("deny", (
            "easifem-dev: `easifem install` without --no-download "
            "would download sources over the local tree. Add "
            "--no-download."))
        return 0
    # `jj git push` must not count as `git push`
    git_text = re.sub(JJ + r"git\b", " jj-git", command)
    cwd = payload.get("cwd") or os.getcwd()
    m = re.search(GIT_WRITE, re.sub(JJ + r"git\b", " jj-git",
                                    strip_quoted(command)))
    if m and targets_jj_repo(command, cwd):
        respond("deny", (
            f"easifem-dev: this is a jj repository, where git is "
            f"read-only. Instead of `git {m.group(1)}` use: "
            f"{JJ_INSTEAD[m.group(1)]}."))
        return 0
    hits = [label for pat, label in RULES if re.search(pat, git_text)]
    hits += [label for pat, label in JJ_RULES if re.search(pat, command)]
    if is_jj_merge(command):
        hits.append("jj merge")
    if not hits:
        return 0
    respond("ask", ("easifem-dev: " + ", ".join(hits) + " needs your "
                    "approval. Command: " + command.strip()[:300]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

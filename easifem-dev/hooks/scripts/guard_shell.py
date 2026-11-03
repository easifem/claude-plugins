#!/usr/bin/env python3
"""PreToolUse hook for shell commands.

`easifem dev` and `easifem run` are allowed. Asks the user before
`easifem install` (shared install), `easifem clean`, file deletion and
risky git commands.
"""
import json
import re
import sys

SEP = r"(?:^|[\s;&|()`])"
RULES = [
    (SEP + r"easifem\s+install\b", "easifem install (writes the shared install)"),
    (SEP + r"easifem\s+clean\b", "easifem clean"),
    (SEP + r"(?:rm|rmdir|unlink)\s", "deleting files"),
    (SEP + r"git\s+commit\b", "git commit"),
    (SEP + r"git\s+push\b", "git push"),
    (SEP + r"git\s+merge\b", "git merge"),
    (SEP + r"git\s+rebase\b", "git rebase"),
    (SEP + r"git\s+reset\s+[^;&|]*--hard\b", "git reset --hard"),
    (SEP + r"git\s+branch\s+[^;&|]*-[dD]\b", "deleting a branch"),
    (SEP + r"git\s+(?:clean|stash\s+drop)\b", "discarding git changes"),
    (SEP + r"git\s+config\s+[^;&|]*--global\b", "global git config"),
    (SEP + r"fortitude\s+check\b(?![^;&|]*--no-fix)", "fortitude check without --no-fix (rewrites files)"),
]


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
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "easifem-dev: `easifem install` without --no-download "
                "would download sources over the local tree. Add "
                "--no-download."),
        }}))
        return 0
    hits = [label for pat, label in RULES if re.search(pat, command)]
    if not hits:
        return 0
    reason = ("easifem-dev: " + ", ".join(hits) + " needs your approval. "
              "Command: " + command.strip()[:300])
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

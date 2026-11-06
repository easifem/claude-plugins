#!/usr/bin/env python3
"""SessionStart hook: tell Claude how to use the Fortran LSP.

Adds context only when the session root has a fortls/zfls config file,
because zfls reads that file from its root and other sessions would not
benefit. Prints nothing elsewhere, so non-Fortran projects are unaffected.
"""
import json
import os
import sys

CONFIG_FILES = (".fortlsrc", ".fortls.json", ".fortls")

CONTEXT = (
    "Fortran code navigation (EASIFEM): for symbol lookups in .F90 files, "
    "use the LSP tool before grep, rg or Grep. If LSP is a deferred tool, "
    "load it first with ToolSearch query 'select:LSP'. "
    "To locate a symbol by name without knowing its position, call "
    "workspaceSymbol with the name as query before using grep; if it finds "
    "nothing, fall back to grep. documentSymbol lists a module's types, bindings and interfaces. "
    "hover gives a signature. goToDefinition jumps from a USE or call site "
    "to the declaration. To reach a submodule body, use goToImplementation "
    "on the obj_Name interface (the MODULE FUNCTION or MODULE SUBROUTINE "
    "line), not on the type-bound name. findReferences is type-aware, so "
    "use it for callers. Keep grep for text search: comments, strings, "
    "macros, CMake files, repositories outside this config's source_dirs, "
    "and the final check that a rename left nothing behind."
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    root = payload.get("cwd") or os.getcwd()
    if not any(os.path.isfile(os.path.join(root, f)) for f in CONFIG_FILES):
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": CONTEXT,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

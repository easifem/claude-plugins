"""Extract FORD documentation prose from a Fortran file as Markdown.

Usage: f90doc2md.py <input.F90> <output.md>

Writes one output line per input line, so Vale's line numbers match the
Fortran source. Kept as prose:

- docblock lines: the `!>` line starts a block, plain `!` lines continue
  it until the first non-comment line;
- `!!` comments on arguments, components and bindings.

Blanked: code, the `!>` line, `date:` / `summary:` fields, fenced code in
`Examples`, `! @note` / `! @endnote` style markers, `!---` banners and
`! @SectionName` markers.
"""

import re
import sys

FIELD = re.compile(r"^(author|date|summary)\s*:", re.IGNORECASE)
MARKER = re.compile(r"^@\w+\s*$")
FORDLINK = re.compile(r"\[\[[^\]]+\]\]")


def convert(lines):
    out = []
    inblock = False
    infence = False
    for line in lines:
        s = line.strip()
        if s.startswith("!!"):
            out.append(s[2:].strip())
            continue
        if s.startswith("!>"):
            inblock, infence = True, False
            out.append("")
            continue
        if not s.startswith("!"):
            inblock = infence = False
            out.append("")
            continue
        if not inblock or s.startswith("!---"):
            out.append("")
            continue
        text = s[1:].strip()
        if text.startswith("```"):
            infence = not infence
            out.append("")
            continue
        if infence or FIELD.match(text) or MARKER.match(text):
            out.append("")
            continue
        out.append(text)
    # FORD links [[name]] need no backticks; hide them from Vale.
    return [FORDLINK.sub(r"`\g<0>`", s) for s in out]


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: f90doc2md.py <input.F90> <output.md>")
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        out = convert(f.read().splitlines())
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

"""The Meeting That Should Have Been an Email — entry generator.

Writes exactly one funny, specific line to <output dir>/entry.txt:
the meeting's only outcome was a calendar invite for the exact same
meeting next week. Stdlib only, deterministic, no network, no secrets.
"""

import os
import sys

LINE = (
    "Forty-five minutes, zero decisions — the meeting's only outcome "
    "was a calendar invite for the exact same meeting next week, same "
    "people, same 'quick sync'."
)


def check_line(line):
    """Gate: one line, 1-200 chars, stripped, valid UTF-8."""
    if line != line.strip():
        return "line has leading/trailing whitespace"
    if "\n" in line or "\r" in line:
        return "line is not a single line"
    if not 1 <= len(line) <= 200:
        return "length %d outside 1-200" % len(line)
    line.encode("utf-8")
    return None


def verify_output(path, expected):
    """Re-read the written file and confirm it matches the gate."""
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        content = f.read()
    if not content.endswith("\n") or content.count("\n") != 1:
        return "file must be exactly one line plus trailing newline"
    if content[:-1] != expected:
        return "file content does not match the generated line"
    return check_line(content[:-1])


def main():
    line = LINE.strip()
    err = check_line(line)
    if err:
        print("gate failed: " + err, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    err = verify_output(path, line)
    if err:
        print("verify failed: " + err, file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

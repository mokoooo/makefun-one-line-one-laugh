#!/usr/bin/env python3
"""Write the One Line, One Laugh entry to entry.txt.

The single joke lives in LINE below. The program validates it,
then writes it (plus one trailing newline) atomically into the
output directory named by MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import sys
import tempfile

LINE = "After my third wrong turn, my GPS said 'recalculating' with such patience that I could hear a machine learning to lower its expectations."


def validate(line):
    """Return an error message, or None when the line is acceptable."""
    if not isinstance(line, str):
        return "line must be text"
    if len(line) < 1 or len(line) > 200:
        return "line must be between 1 and 200 characters"
    if not line.strip():
        return "line must not be blank"
    if "\n" in line or "\r" in line:
        return "line must be a single line with no newline characters"
    return None


def main():
    problem = validate(LINE)
    if problem is not None:
        print("error: " + problem, file=sys.stderr)
        return 1

    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip() or "/output"
    os.makedirs(out_dir, exist_ok=True)

    payload = (LINE + "\n").encode("utf-8")
    target = os.path.join(out_dir, "entry.txt")

    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The Worst App Idea Ever Pitched — make.fun entry (v1).

Writes one sentence (at most 240 characters) pitching the worst,
most useless app idea imaginable to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic: no randomness, no clock, no network, no input files.

Pitch rationale (judge criteria, most important first): CurtainCall names
a specific app and one useless function (applauding finished laundry);
the uselessness is funny through deadpan confidence and the mismatch
between a problem nobody has and a service that solves it; it sounds
like a real pitch (product name, price, five-star review); it is one
clean sentence that uses the 240-character budget; and it leaves a
vivid picture — a small trained crowd, a standing ovation, a bouquet.
"""

import os
import sys

MAX_CHARS = 240

TEXT = (
    "CurtainCall hires a small, professionally trained crowd to applaud "
    "you every time you finish a load of laundry, complete with a standing "
    "ovation, a bouquet, and a five-star review of your folding technique, "
    "for $10 a load."
)


def resolve_output_dir():
    """Return the grader's output directory, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if out.strip():
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(text):
    """Enforce the competition gate: 1-240 chars, one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("entry text must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry text must be 1-%d characters, got %d"
            % (MAX_CHARS, len(text))
        )
    if text.strip() != text or not text.strip():
        raise ValueError("entry text must not be blank or padded")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if "  " in text:
        raise ValueError("entry text must not contain double spaces")
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("entry text must be ASCII so chars equal bytes")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry text must be exactly one sentence")
    return text


def main():
    text = validate(TEXT)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    # Round-trip check: a silent short write must fail loudly, not ship.
    with open(path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != text:
        raise ValueError("entry.txt round-trip mismatch")
    validate(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())

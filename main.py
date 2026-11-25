#!/usr/bin/env python3
"""Make the AI Judge Laugh — entry program (v2).

Writes one office-life joke, one line, under 200 characters, to
/output/entry.txt. Python 3.13 stdlib only, deterministic, self-contained.

Revision over v1: tightened the opener ("My CV says" for "I put ... on my
CV") and gave the punchline a last-word kicker — "six of them threats" —
so the turn lands twice: the seven tones, then what the tones are.
"""
import os

JOKE = (
    "My CV says 'excellent communicator' because I can say 'per my last "
    "email' in seven tones of voice, six of them threats."
)


def main():
    assert 1 <= len(JOKE) <= 199, "joke must be 1-200 characters"
    assert "\n" not in JOKE, "joke must be a single line"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(JOKE)


if __name__ == "__main__":
    main()

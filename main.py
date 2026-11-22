#!/usr/bin/env python3
"""Copy the bundled front-page image to the output directory.

The entry image lives in this repository as entry.png; this program only
moves a copy of it to the place the competition reads from. It uses the
standard library only, never touches the network, and writes the same
bytes on every run.
"""

import os
import shutil


def main():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(target, "entry.png"),
    )


if __name__ == "__main__":
    main()

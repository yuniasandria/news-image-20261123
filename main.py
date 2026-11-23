#!/usr/bin/env python3
"""news-image-20261123 entry: write the bundled front page to /output/entry.png.

Deterministic and offline: copies the exact bytes of entry.png shipped in
this repository. No network, no randomness, no timestamps.
"""
import os
import shutil
import sys


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")


if __name__ == "__main__":
    sys.exit(main())

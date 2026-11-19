#!/usr/bin/env python3
"""Entry point for the make.fun 'news-image-20261119' bounty.

Writes the pre-rendered front page (frontpage.png, committed next to
this file) to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
The asset is copied byte-for-byte, so every run produces identical
output. No network, no dependencies beyond the stdlib: the grader
installs nothing before running this, so main.py must never import
Pillow or render.py. The page itself was drawn by render.py (kept in
the repo for provenance; it needs Pillow and is never run here).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "frontpage.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")


if __name__ == "__main__":
    main()

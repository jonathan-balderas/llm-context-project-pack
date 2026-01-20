#!/usr/bin/env python3
"""
Build a Project Pack ZIP from Context/ folder.

Usage:
  python scripts/build_project_pack.py --out Project_Pack.zip
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Context", help="Context root folder")
    ap.add_argument("--out", default="Project_Pack.zip", help="Output zip filename")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"Context root not found: {root}")

    out = Path(args.out)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_dir():
                continue
            arc = p.as_posix()
            z.write(p, arcname=arc)

    print(f"Built: {out} (from {root})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

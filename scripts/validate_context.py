#!/usr/bin/env python3
"""
Validate a Context/ directory:
- Every *.md has Version + LastUpdated within the first 30 lines
- Context_Index.md has unique DocIDs and FilePaths
- Each Doc entry has Owns:
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADER_MAX_LINES = 30
VERSION_RE = re.compile(r"^Version:\s*\d+\s*$", re.MULTILINE)
LASTUPDATED_RE = re.compile(r"^LastUpdated:\s*.+\s*$", re.MULTILINE)

DOCID_RE = re.compile(r"^\s*-\s*DocID:\s*(\S+)\s*$")
FILEPATH_RE = re.compile(r"^\s*FilePath:\s*(\S+)\s*$")
OWNS_RE = re.compile(r"^\s*Owns:\s*(.+)\s*$")


def check_headers(md_path: Path) -> list[str]:
    txt = md_path.read_text(encoding="utf-8", errors="replace")
    head = "\n".join(txt.splitlines()[:HEADER_MAX_LINES])
    errs = []
    if not VERSION_RE.search(head):
        errs.append(f"{md_path}: missing Version header in first {HEADER_MAX_LINES} lines")
    if not LASTUPDATED_RE.search(head):
        errs.append(f"{md_path}: missing LastUpdated header in first {HEADER_MAX_LINES} lines")
    return errs


def check_index(index_path: Path) -> list[str]:
    txt = index_path.read_text(encoding="utf-8", errors="replace").splitlines()
    errs = []
    docids = set()
    paths = set()

    cur_docid = None
    cur_path = None
    has_owns = False

    def flush():
        nonlocal cur_docid, cur_path, has_owns
        if cur_docid is not None:
            if cur_docid in docids:
                errs.append(f"{index_path}: duplicate DocID {cur_docid}")
            else:
                docids.add(cur_docid)

            if cur_path is None:
                errs.append(f"{index_path}: DocID {cur_docid} missing FilePath")
            else:
                if cur_path in paths:
                    errs.append(f"{index_path}: duplicate FilePath {cur_path}")
                else:
                    paths.add(cur_path)

            if not has_owns:
                errs.append(f"{index_path}: DocID {cur_docid} missing Owns:")

        cur_docid = None
        cur_path = None
        has_owns = False

    for line in txt:
        m = DOCID_RE.match(line)
        if m:
            flush()
            cur_docid = m.group(1)
            continue

        m = FILEPATH_RE.match(line)
        if m and cur_docid:
            cur_path = m.group(1)
            continue

        if OWNS_RE.match(line) and cur_docid:
            has_owns = True

    flush()
    return errs


def main() -> int:
    root = Path("Context")
    if not root.exists():
        print("ERROR: Context/ not found")
        return 2

    errs: list[str] = []
    for p in root.rglob("*.md"):
        errs.extend(check_headers(p))

    index = root / "System" / "Context_Index.md"
    if index.exists():
        errs.extend(check_index(index))
    else:
        errs.append("Context/System/Context_Index.md not found")

    if errs:
        print("Validation failed:")
        for e in errs:
            print("-", e)
        return 1

    print("Validation OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

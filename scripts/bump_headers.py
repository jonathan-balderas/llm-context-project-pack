#!/usr/bin/env python3
"""
bump_headers.py

Updates markdown file headers:
- Version: <int>  (increment by 1 when an update is needed)
- LastUpdated: <ISO8601 datetime>  (or date-only if requested)

- Files under Context/** typically contain Version/LastUpdated near the top.
- Context_Index.md may start with CHATGPT_CONTEXT_INDEX_CANONICAL marker; headers may appear after it.

Modes:
1) Explicit files: --files path1 path2 ...
2) Git changed files: --from-git
3) Auto-scan Context/: --auto-scan (default if no --files/--from-git)

"Update needed" definition (default):
- file mtime > parsed LastUpdated timestamp + margin_seconds
or
- --force

Optionally set file mtime to the new LastUpdated stamp (default: on) to avoid repeated bumps.

Usage examples:
  python bump_headers.py --files Context/System/ChatGPT_Operating_Guide.md Context/System/New_Chat_Start_Templates.md
  python bump_headers.py --from-git
  python bump_headers.py --auto-scan
  python bump_headers.py --dry-run --from-git
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional, Tuple, List


VERSION_RE = re.compile(r"^\s*Version:\s*(\d+)\s*$")
LASTUPDATED_RE = re.compile(r"^\s*LastUpdated:\s*(.+?)\s*$")
CANONICAL_MARKER_RE = re.compile(r"^\s*CHATGPT_CONTEXT_INDEX_CANONICAL\b")


@dataclass
class HeaderInfo:
    version_idx: Optional[int]
    lastupdated_idx: Optional[int]
    version_val: Optional[int]
    lastupdated_raw: Optional[str]


def _parse_lastupdated(value: str) -> Optional[datetime]:
    """
    Accepts:
    - YYYY-MM-DD
    - ISO-8601 datetime, e.g. 2026-01-17T16:23:11-06:00 or Z
    """
    v = value.strip()

    # Date-only
    try:
        dt = datetime.strptime(v, "%Y-%m-%d")
        # interpret date-only as local midnight (naive)
        return dt
    except ValueError:
        pass

    # ISO datetime (Python can parse many ISO formats via fromisoformat)
    # Normalize trailing 'Z' -> '+00:00'
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
        return dt
    except ValueError:
        return None


def _dt_to_stamp(dt: datetime, date_only: bool) -> str:
    if date_only:
        # Use local date from dt
        if dt.tzinfo is not None:
            return dt.astimezone().date().isoformat()
        return dt.date().isoformat()

    # ISO datetime with timezone if available; otherwise localize
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc).astimezone()
    else:
        dt = dt.astimezone()
    return dt.isoformat(timespec="seconds")


def _find_headers(lines: List[str], search_limit: int = 40) -> HeaderInfo:
    """
    Find Version/LastUpdated near the top to avoid accidental matches deep in file.
    """
    v_idx = None
    lu_idx = None
    v_val = None
    lu_raw = None

    for i, line in enumerate(lines[:search_limit]):
        m = VERSION_RE.match(line)
        if m and v_idx is None:
            v_idx = i
            v_val = int(m.group(1))
            continue
        m = LASTUPDATED_RE.match(line)
        if m and lu_idx is None:
            lu_idx = i
            lu_raw = m.group(1).strip()
            continue

    return HeaderInfo(v_idx, lu_idx, v_val, lu_raw)


def _insertion_index_for_missing_headers(lines: List[str]) -> int:
    """
    If file starts with CHATGPT_CONTEXT_INDEX_CANONICAL marker, insert headers after it
    (and after an optional blank line).
    Otherwise insert at the top.
    """
    if not lines:
        return 0

    # Find first non-empty line
    first_nonempty = None
    for i, line in enumerate(lines[:10]):
        if line.strip():
            first_nonempty = i
            break
    if first_nonempty is None:
        return 0

    if CANONICAL_MARKER_RE.match(lines[first_nonempty]):
        # Insert after marker line
        idx = first_nonempty + 1
        # If next line is blank, keep it and insert after it
        if idx < len(lines) and not lines[idx].strip():
            idx += 1
        return idx

    return 0


def _get_mtime_dt(path: Path) -> datetime:
    ts = path.stat().st_mtime
    # Convert to local timezone-aware datetime
    return datetime.fromtimestamp(ts).astimezone()


def _get_git_changed_files(repo_root: Path) -> List[Path]:
    """
    Returns files changed vs HEAD (staged or unstaged), using git.
    """
    try:
        # Includes staged+unstaged vs HEAD:
        # - name-only for HEAD.. (staged) plus working tree changes
        # We'll union:
        # 1) git diff --name-only
        # 2) git diff --name-only --cached
        unstaged = subprocess.check_output(
            ["git", "diff", "--name-only"], cwd=str(repo_root), text=True
        ).splitlines()
        staged = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"], cwd=str(repo_root), text=True
        ).splitlines()
    except Exception as e:
        raise RuntimeError(f"Failed to read git changes. Are you in a git repo? ({e})")

    paths = {repo_root / p for p in (unstaged + staged) if p.strip()}
    return sorted(paths)


def _should_update(mtime_dt: datetime, last_dt: Optional[datetime], margin_seconds: int) -> bool:
    if last_dt is None:
        return True

    # If last_dt is naive (date-only parsed), compare using local timezone at midnight
    if last_dt.tzinfo is None:
        last_dt_local = last_dt.replace(tzinfo=mtime_dt.tzinfo)
    else:
        last_dt_local = last_dt.astimezone(mtime_dt.tzinfo)

    delta = (mtime_dt - last_dt_local).total_seconds()
    return delta > margin_seconds


def bump_file(
    path: Path,
    date_only: bool,
    margin_seconds: int,
    force: bool,
    sync_mtime: bool,
    dry_run: bool,
) -> Tuple[bool, str]:
    """
    Returns: (changed?, message)
    """
    if not path.exists() or not path.is_file():
        return False, f"SKIP (missing): {path}"

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    header = _find_headers(lines)
    mtime_dt = _get_mtime_dt(path)
    last_dt = _parse_lastupdated(header.lastupdated_raw) if header.lastupdated_raw else None

    needs_update = force or _should_update(mtime_dt, last_dt, margin_seconds)

    if not needs_update:
        return False, f"OK (no bump): {path}"

    # Determine new stamp.
    # Use "now" so editors reliably detect an external change (mtime advances),
    # and to avoid resetting mtime back to an older timestamp.
    new_stamp_dt = datetime.now().astimezone()
    new_stamp = _dt_to_stamp(new_stamp_dt, date_only=date_only)


    # If headers missing, insert
    if header.version_idx is None or header.lastupdated_idx is None:
        insert_at = _insertion_index_for_missing_headers(lines)
        insert_block = [
            f"Version: 1\n",
            f"LastUpdated: {new_stamp}\n",
            "\n",
        ]
        new_lines = lines[:insert_at] + insert_block + lines[insert_at:]
        # If Version exists but LastUpdated doesn't (or vice versa), we'll still increment logic below
        lines = new_lines
        header = _find_headers(lines)

    # Update Version (increment)
    v_idx = header.version_idx
    lu_idx = header.lastupdated_idx
    if v_idx is None or lu_idx is None:
        return False, f"SKIP (header parse failed): {path}"

    v_val = header.version_val if header.version_val is not None else 0
    new_version = v_val + 1

    # Replace lines
    lines[v_idx] = re.sub(VERSION_RE, f"Version: {new_version}", lines[v_idx]).rstrip("\n") + "\n"
    lines[lu_idx] = re.sub(LASTUPDATED_RE, f"LastUpdated: {new_stamp}", lines[lu_idx]).rstrip("\n") + "\n"

    new_text = "".join(lines)

    if dry_run:
        return True, f"DRY-RUN bump: {path} -> Version {new_version}, LastUpdated {new_stamp}"

    path.write_text(new_text, encoding="utf-8")

    # Sync file mtime to the stamp (prevents immediate re-bump on next run)
    if sync_mtime:
        ts = new_stamp_dt.timestamp()
        os.utime(path, (ts, ts))

    return True, f"BUMPED: {path} -> Version {new_version}, LastUpdated {new_stamp}"


def _iter_context_markdown(repo_root: Path) -> Iterable[Path]:
    ctx = repo_root / "Context"
    if not ctx.exists():
        return []
    return sorted(ctx.rglob("*.md"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".", help="Repo root (default: .)")
    ap.add_argument("--files", nargs="*", help="Explicit file list (relative to repo-root)")
    ap.add_argument("--from-git", action="store_true", help="Use git to find changed files")
    ap.add_argument("--auto-scan", action="store_true", help="Scan Context/**.md (default if no files/from-git)")
    ap.add_argument("--force", action="store_true", help="Bump even if mtime <= LastUpdated")
    ap.add_argument("--date-only", action="store_true", help="LastUpdated as YYYY-MM-DD (default: ISO datetime)")
    ap.add_argument("--margin-seconds", type=int, default=2, help="mtime vs LastUpdated threshold (default: 2s)")
    ap.add_argument("--no-sync-mtime", action="store_true", help="Do not sync file mtime to LastUpdated")
    ap.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    sync_mtime = not args.no_sync_mtime

    # Resolve targets
    targets: List[Path] = []
    if args.files:
        targets = [ (repo_root / f).resolve() for f in args.files ]
    elif args.from_git:
        targets = _get_git_changed_files(repo_root)
    else:
        # Default to auto-scan Context/**.md unless explicitly disabled
        targets = list(_iter_context_markdown(repo_root))

    # Filter: only .md files (safe) and ignore non-existent
    targets = [p for p in targets if p.suffix.lower() == ".md" and p.exists()]

    changed = 0
    for p in targets:
        did_change, msg = bump_file(
            p,
            date_only=args.date_only,
            margin_seconds=args.margin_seconds,
            force=args.force,
            sync_mtime=sync_mtime,
            dry_run=args.dry_run,
        )
        print(msg)
        if did_change:
            changed += 1

    print(f"\nDone. Files bumped: {changed} / {len(targets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

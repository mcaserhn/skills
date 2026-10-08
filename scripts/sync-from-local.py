#!/usr/bin/env python3
"""Mirror whitelisted skills from the local skills directory into ./skills.

Single source of truth: the local skills directory (default
~/.workbuddy/skills). This repository is the published mirror, so the copy
direction is local -> repo. Only skills listed in WHITELIST are touched;
everything else under ./skills is left alone.

The script never commits or pushes - it only writes files. Review the diff,
run validate.py, then commit manually.

Usage:
    python scripts/sync-from-local.py            # sync whitelist
    python scripts/sync-from-local.py --dry-run  # report only
"""
import argparse
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_LOCAL = pathlib.Path.home() / ".workbuddy" / "skills"

# Only skills authored by me are published. Never add marketplace-installed
# or third-party skills here.
WHITELIST = [
    "spp-source-principle",
    "de-ai-flavor",
    "devils-advocate",
]

SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "__pycache__"}


def iter_files(base):
    for p in sorted(base.rglob("*")):
        if p.is_file() and p.name not in SKIP_NAMES and "__pycache__" not in p.parts:
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local-dir", default=str(DEFAULT_LOCAL),
                    help="source skills directory (default: %(default)s)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    local = pathlib.Path(args.local_dir)
    dest_root = ROOT / "skills"

    if not local.is_dir():
        print("FAIL  local skills directory not found: %s" % local)
        return 1

    print("Source : %s" % local)
    print("Target : %s" % dest_root)
    print("Scope  : %s\n" % ", ".join(WHITELIST))

    failures = 0
    for name in WHITELIST:
        src = local / name
        if not src.is_dir():
            print("FAIL  %-28s source missing" % name)
            failures += 1
            continue

        dst = dest_root / name
        src_files = list(iter_files(src))

        if args.dry_run:
            print("DRY   %-28s %d file(s) -> %s" % (name, len(src_files), dst))
            continue

        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst,
                        ignore=shutil.ignore_patterns(*SKIP_NAMES, "__pycache__"))

        dst_files = list(iter_files(dst))
        diff = 0
        src_map = {p.relative_to(src).as_posix(): p.stat().st_size for p in src_files}
        dst_map = {p.relative_to(dst).as_posix(): p.stat().st_size for p in dst_files}
        for k in set(src_map) | set(dst_map):
            if src_map.get(k) != dst_map.get(k):
                diff += 1

        status = "OK  " if (len(src_files) == len(dst_files) and diff == 0) else "FAIL"
        if status == "FAIL":
            failures += 1
        print("%s  %-28s SRC=%d DST=%d DIFF=%d"
              % (status, name, len(src_files), len(dst_files), diff))

    print("")
    if failures:
        print("RESULT: FAIL (%d skill(s))" % failures)
        return 1
    print("RESULT: OK - review the diff, then run validate.py and commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

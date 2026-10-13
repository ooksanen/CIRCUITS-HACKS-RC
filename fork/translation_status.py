"""Which English translations are behind upstream.

    python fork/translation_status.py            # one line per source: up to date / N commits behind
    python fork/translation_status.py -d         # also the diff of each stale source since its translated commit
    python fork/translation_status.py --ref REF  # compare with REF instead of upstream/main

A translated file declares its sources in its first lines:
    <!-- translated-from: docs/NOTAS.md @ 36c99f1 -->
After updating a translation, set the hash to the upstream commit it now matches (`git rev-parse --short upstream/main`).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = re.compile(r"<!--\s*translated-from:\s*(\S+)\s*@\s*([0-9a-f]{7,40})\b")
HEAD_LINES = 5


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def sources(path: Path):
    try:
        head = path.read_text(encoding="utf-8").splitlines()[:HEAD_LINES]
    except (UnicodeDecodeError, OSError):
        return []
    return [m.groups() for line in head for m in [HEADER.search(line)] if m]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-d", "--diff", action="store_true", help="show the upstream diff of stale sources")
    ap.add_argument("--ref", default="upstream/main", help="upstream ref to compare with (default upstream/main)")
    args = ap.parse_args()

    try:
        git("rev-parse", "--verify", "--quiet", args.ref)
    except subprocess.CalledProcessError:
        print(f"{args.ref} not found: run `git fetch upstream` (and fork/setup.sh)", file=sys.stderr)
        return 2

    stale = 0
    for name in git("ls-files", "--cached", "--others", "--exclude-standard", "*.md", "*.html").splitlines():
        for src, sha in sources(ROOT / name):
            behind = int(git("rev-list", "--count", f"{sha}..{args.ref}", "--", src).strip())
            state = "up to date" if behind == 0 else f"{behind} upstream commit(s) behind"
            print(f"{name:28s} <- {src:20s} @ {sha}  {state}")
            if behind:
                stale += 1
                if args.diff:
                    print(git("diff", "--stat", sha, args.ref, "--", src) + git("diff", sha, args.ref, "--", src))
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())

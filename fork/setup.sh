#!/usr/bin/env bash
# Per-clone setup of this fork (safe to run again). Nothing here is committed: git keeps it in .git/.
#   - remote `upstream` = the original Spanish repository; remote `fork` = the public GitHub fork (main only)
#     (`origin` is the private ooksanen/ctplay, set by cloning it)
#   - CLAUDE.md merges with the `ours` driver: merging upstream (into main) or main (into slim) keeps the branch's own CLAUDE.md
#   - .venv/ ignored locally (upstream's .gitignore is left untouched)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

UPSTREAM=https://github.com/Ghillermo/CIRCUITS-HACKS-RC.git
FORK=https://github.com/ooksanen/CIRCUITS-HACKS-RC.git
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "$UPSTREAM"
git remote get-url fork >/dev/null 2>&1 || git remote add fork "$FORK"

git config merge.ours.driver true

add_line() {  # add_line FILE LINE: append LINE unless already present
    mkdir -p "$(dirname "$1")"; touch "$1"
    grep -qxF "$2" "$1" || echo "$2" >> "$1"
}
add_line "$(git rev-parse --git-path info/attributes)" "CLAUDE.md merge=ours"
add_line "$(git rev-parse --git-path info/exclude)" ".venv/"

echo "upstream: $(git remote get-url upstream)"
echo "fork: $(git remote get-url fork)"
echo "merge.ours.driver: $(git config merge.ours.driver)"
echo "CLAUDE.md attributes: $(git check-attr merge -- CLAUDE.md)"

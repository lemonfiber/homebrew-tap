# Task runner for the lemonfiber/homebrew-tap repo. `just` with no argument lists tasks.
default:
    @just --list

# Turn on the repository's own git hooks. Once per clone.
#
# This repository has no package manager, so there is no `npm ci` or `composer
# install` to hang the setting on the way the other repos do — it is this recipe
# or nothing, and `ci` depends on it so that running the checks once turns the
# hooks on for good.
hooks:
    git config core.hooksPath .githooks
    @echo "hooks on: .githooks/"

# The formula this tap serves, read the way CI reads it — all five rules,
# `brew style` among them.
#
# It needs `ruby` and `brew` on the machine, because two of the five rules *are*
# those programs. Neither is skipped where it is absent: a formula nobody parsed
# and a formula with no objection are the same green tick otherwise, so the rule
# refuses and says which of its two answers it could not give.
#
# It is not CI and does not say it is. These are not here:
#
#   commitlint, dco, attribution,   `.githooks/commit-msg` refuses all four
#   the citation gate               before the push, and `hooks` turns it on
#   hygiene                         actionlint, links, markdown, the invite
#                                   check and shared-files; `typos` below is
#                                   the one of them that is here
#   pins, workflow-pins             ask the forge which commits a pin has not
#                                   taken
#   CodeQL, gitleaks, osv-scanner,  forge-side
#   label, the reference comment
ci: hooks
    # First, because a name that does not resolve is a gate that cannot judge
    # anything, and the Python here is what does the judging.
    uvx ruff@0.16.4 check scripts/
    python3 scripts/check_formula.py --self-test
    python3 scripts/check_formula.py
    typos

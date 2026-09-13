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

# Everything CI runs bar `brew style`, which needs Homebrew on the machine.
#
# The formula this tap serves, read the way CI reads it.
ci: hooks
    python3 scripts/check_formula.py --self-test
    python3 scripts/check_formula.py
    typos

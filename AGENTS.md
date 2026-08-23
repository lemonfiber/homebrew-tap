# AGENTS.md — homebrew-tap

> **Common rules for every lemonfiber repo are canonical in the spec:**
> [50-governance/ai-contributors.md](https://github.com/lemonfiber/spec/blob/main/50-governance/ai-contributors.md).

## What this repo is

Homebrew formulae. The formula is **generated** by `lemonfiber`'s release CI — do
not edit `Formula/*.rb` by hand. A change to the generator is a `lemonfiber`
change following the normal lifecycle (`REPO-R28`). Spec:
[`30-repos/homebrew-tap.md`](https://github.com/lemonfiber/spec/blob/main/30-repos/homebrew-tap.md).

There is almost nothing to do here directly. If you're tempted to edit the
formula, the change probably belongs in `lemonfiber`'s release pipeline instead.

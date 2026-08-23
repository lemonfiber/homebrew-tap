<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/logo-on-ink.svg">
    <img alt="lemonfiber" src=".github/logo.svg" height="72">
  </picture>
</p>

<h1 align="center">Lemonfiber &mdash; homebrew-tap</h1>

<p align="center">Homebrew formulae for lemonfiber.</p>

<p align="center">
  <a href="https://github.com/lemonfiber/homebrew-tap/actions/workflows/ci.yml"><img alt="ci" src="https://github.com/lemonfiber/homebrew-tap/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/lemonfiber/homebrew-tap"><img alt="OpenSSF Scorecard" src="https://api.scorecard.dev/projects/github.com/lemonfiber/homebrew-tap/badge"></a>
</p>

---

> **Status: placeholder.** `lemonfiber` has been shipping tagged releases since
> v0.1.0, but none of them wrote this formula — the release pipeline builds the
> shell installer and the platform archives only. The Homebrew publish job turns
> on at 1.0.0 (`L1-R3`), once the tap has a `HOMEBREW_TAP_TOKEN`. From then on
> the formula is written by CI and must not be edited by hand.

## Install

```
brew install lemonfiber/tap/lemonfiber
```

Not yet — the formula is a placeholder, so this resolves to nothing
installable. Until 1.0.0, use the shell installer attached to each
[`lemonfiber` release](https://github.com/lemonfiber/lemonfiber/releases).

## How this repo works

`Formula/lemonfiber.rb` is written by
[`lemonfiber`](https://github.com/lemonfiber/lemonfiber)'s release pipeline
(cargo-dist), never by hand. That publish job is off until 1.0.0, so the file
holds the scaffold placeholder rather than pipeline output.

This repo exists because a Homebrew tap must be a repository named
`homebrew-<name>`. That requirement set the floor at two repos; the org has since
grown to eleven for reasons of its own. See spec
[`30-repos/homebrew-tap.md`](https://github.com/lemonfiber/spec/blob/main/30-repos/homebrew-tap.md).

Note: Lemonfiber is licensed Hippocratic 3.0 (not OSI-approved), so it lives in
this tap rather than homebrew-core.

## Licence

[Hippocratic License 3.0](LICENSE).

---

<p align="center">
  <a href="https://nightworks.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/nightworks-white.png">
      <img alt="NightWorks.io" src=".github/nightworks-dark.png" height="20">
    </picture>
  </a>
  &nbsp;&middot;&nbsp;<a href="https://discord.nightworks.io"><img alt="Discord" src=".github/discord.svg" height="20"></a>
</p>

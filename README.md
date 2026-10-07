<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/logo-on-ink.svg">
    <img alt="lemonfiber" src=".github/logo.svg" height="72">
  </picture>
</p>

<h1 align="center">Lemonfiber &mdash; homebrew-tap</h1>

<p align="center">The Homebrew tap for lemonfiber, the tool that sets up and runs a self-hosted media stack.</p>

<p align="center">
  <a href="https://github.com/lemonfiber/homebrew-tap/actions/workflows/ci.yml"><img alt="ci" src="https://github.com/lemonfiber/homebrew-tap/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/lemonfiber/homebrew-tap"><img alt="OpenSSF Scorecard" src="https://api.scorecard.dev/projects/github.com/lemonfiber/homebrew-tap/badge"></a>
</p>

---

## You cannot install lemonfiber from here yet

The formula in this tap is a placeholder. It declares version `0.0.0` and names
no download, so this command fails:

```sh
brew install lemonfiber/tap/lemonfiber
```

No lemonfiber release publishes to this tap. Every release ships a shell
installer and an archive per platform instead:
[Install lemonfiber](https://docs.lemonfiber.app/start/install/) explains both.

## How this tap works

[`Formula/lemonfiber.rb`](Formula/lemonfiber.rb) is not edited by hand:
lemonfiber's release pipeline owns it. A change to what the formula
contains is a change to that pipeline, in the
[`lemonfiber`](https://github.com/lemonfiber/lemonfiber) repository.

lemonfiber is licensed under the Hippocratic License 3.0, which is not
OSI-approved, so it cannot go into homebrew-core. Homebrew requires a tap to be
a repository named `homebrew-<name>`, which is why this one exists.

## Contributing and security

Read the [contributing guide](https://github.com/lemonfiber/spec/blob/main/50-governance/contributing.md)
before opening a pull request. Report a vulnerability as the
[security policy](https://github.com/lemonfiber/.github/blob/main/SECURITY.md)
describes, not in a public issue.

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

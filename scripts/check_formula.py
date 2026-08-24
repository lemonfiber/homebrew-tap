#!/usr/bin/env python3
"""Check the formula this tap serves.

`brew` reads `Formula/<name>.rb` from this repository and runs it. That file is
the whole of the tap's runtime surface, and until this ran nothing in CI read
it: the shared gates check governance, spelling, links and workflows, and none
of them parses Ruby.

Five rules run over every formula in `Formula/`:

  parses             `ruby -c` accepts the file
  style              `brew style` reports no offence
  class-name         the class is the one `brew install lemonfiber/tap/<name>`
                     resolves to, derived from the file name the way
                     `Formulary.class_s` derives it
  describes          `desc` and `homepage` are declared
  tests-the-version  the `test` block asserts the binary reports the version the
                     formula declares (`REPO-R26`)

`--self-test` runs every rule against a formula that satisfies it and against one
built to violate it, and fails unless each rule accepts the first and refuses the
second. It runs beside the real check, on the same runner, with the same tools.

Usage:
  check_formula.py [--formula-dir DIR]
  check_formula.py --self-test
Exit 0 = every rule passes, 1 = at least one does not, 2 = usage error.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

CLASS_LINE = re.compile(r"^class\s+(\w+)\s*<\s*Formula\b", re.MULTILINE)
VERSION_LINE = re.compile(r'^\s*version\s+"([^"]+)"', re.MULTILINE)
TEST_BLOCK = re.compile(r"^ {2}test do\n(.*?)^ {2}end$", re.MULTILINE | re.DOTALL)


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, capture_output=True, text=True, check=False)


def declares(text: str, field: str) -> bool:
    return re.search(rf'^\s*{field}\s+"[^"]+"', text, re.MULTILINE) is not None


def class_s(stem: str) -> str:
    """The class name Homebrew derives from a file name (`Formulary.class_s`)."""
    name = stem.capitalize()
    name = re.sub(r"[-_.\s]([a-zA-Z0-9])", lambda m: m.group(1).upper(), name)
    name = name.replace("+", "x")
    return re.sub(r"(.)@(\d)", r"\1AT\2", name, count=1)


def rule_parses(path: pathlib.Path) -> list[str]:
    done = run(["ruby", "-c", str(path)])
    if done.returncode == 0:
        return []
    return [f"ruby rejects the file: {done.stderr.strip() or done.stdout.strip()}"]


def rule_style(path: pathlib.Path) -> list[str]:
    done = run(["brew", "style", str(path)])
    if done.returncode == 0:
        return []
    return [f"brew style objects: {done.stdout.strip() or done.stderr.strip()}"]


def rule_class_name(path: pathlib.Path) -> list[str]:
    found = CLASS_LINE.search(path.read_text(encoding="utf-8"))
    if not found:
        return ["no `class <Name> < Formula` here, so brew has nothing to load"]
    want = class_s(path.stem)
    if found.group(1) != want:
        return [f"the class is {found.group(1)}, and brew loads {path.name} as {want}"]
    return []


def rule_describes(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [
        f"no `{field}` line, which `brew info` and the tap listing both read"
        for field in ("desc", "homepage")
        if not declares(text, field)
    ]


def rule_tests_the_version(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    version = VERSION_LINE.search(text)
    if not version:
        return ["no `version` line, so there is no version for the test to assert"]
    block = TEST_BLOCK.search(text)
    if not block:
        return ["no `test do` block, so `brew test` proves nothing"]
    body = block.group(1)
    problems = []
    if "--version" not in body:
        problems.append("the test block never runs the binary with `--version`")
    if version.group(1) not in body:
        problems.append(
            f"the test block does not assert the declared version {version.group(1)}, "
            "so a formula carrying the wrong build would pass it"
        )
    return problems


RULES = {
    "parses": rule_parses,
    "style": rule_style,
    "class-name": rule_class_name,
    "describes": rule_describes,
    "tests-the-version": rule_tests_the_version,
}

GOOD = '''\
class Lemonfiber < Formula
  desc "Self-hosted media automation stack, run in slices"
  homepage "https://github.com/lemonfiber/lemonfiber"
  version "0.0.0"

  def install
    bin.install "lemonfiber"
  end

  test do
    assert_match "0.0.0", shell_output("#{bin}/lemonfiber --version")
  end
end
'''

# One formula per rule, each built to violate that rule and nothing else.
BROKEN = {
    "parses": GOOD + "end\n",
    "style": GOOD.replace('  version "0.0.0"', '   version "0.0.0"'),
    "class-name": GOOD.replace("class Lemonfiber", "class Lemonfibre"),
    "describes": GOOD.replace(
        '  desc "Self-hosted media automation stack, run in slices"\n', ""
    ),
    "tests-the-version": GOOD.replace(
        '    assert_match "0.0.0", shell_output("#{bin}/lemonfiber --version")',
        '    system "#{bin}/lemonfiber", "--version"',
    ),
}


def report(objections: list[str], line: str) -> None:
    print(f"  {'FAIL' if objections else 'ok  '}  {line}")


def check(path: pathlib.Path) -> list[str]:
    problems = []
    for name, rule in RULES.items():
        objections = rule(path)
        report(objections, name)
        problems.extend(f"{path}: {name}: {p}" for p in objections)
    return problems


def written(source: str, into: pathlib.Path) -> pathlib.Path:
    """A formula on disk under a `Formula/` directory, which is where brew reads."""
    path = into / "Formula" / "lemonfiber.rb"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def self_test() -> int:
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        good = written(GOOD, root / "good")
        for name, rule in RULES.items():
            objections = rule(good)
            report(objections, f"{name} accepts a formula that satisfies it")
            problems.extend(f"{name}: {p}" for p in objections)

        for name, source in BROKEN.items():
            rule = RULES[name]
            path = written(source, root / name)
            found = []
            if not rule(path):
                found.append(f"{name} accepts the formula built to violate it")
            elif rule is not rule_parses and rule_parses(path):
                found.append(
                    f"the {name} fixture is not valid Ruby, so its refusal says "
                    f"nothing about {name}"
                )
            report(found, f"{name} refuses the formula built to violate it")
            problems.extend(found)

    for problem in problems:
        print(f"::error::{problem}")
    if problems:
        print("\nA rule that cannot fail is not a gate.")
        return 1
    print(f"\nall {len(RULES)} rules refuse what they exist to refuse")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--formula-dir", default="Formula")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    directory = pathlib.Path(a.formula_dir)
    formulae = sorted(directory.glob("*.rb"))
    if not formulae:
        print(f"::error::no formula in {directory}/ — brew would find nothing here")
        return 1

    problems = []
    for path in formulae:
        print(f"{path}")
        problems.extend(check(path))

    for problem in problems:
        print(f"::error::{problem}")
    if problems:
        return 1
    print(f"\n{len(formulae)} formula, {len(RULES)} rules, no objection")
    return 0


if __name__ == "__main__":
    sys.exit(main())

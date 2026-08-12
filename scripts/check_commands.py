"""Verify the project's documented commands still resolve.

**A commit that breaks `make docs` should fail before it lands, not the next time
someone runs `make docs`.** The interface is the part of a PoC everyone touches and
nobody tests, because testing it means running it -- which is slow.

So this checks the interface *statically*, fast enough for a pre-commit hook:

1. Every target with a `##` description resolves. `make -n` expands the target and
   its prerequisites without executing anything, so a deleted target or a renamed
   prerequisite fails here.
2. Every script a recipe invokes exists. `make -n` prints a recipe without running
   it, so a deleted `scripts/foo.py` would otherwise pass.
3. Every `python -m module` a recipe invokes is importable.
4. Every documented target is in `.PHONY`. Without it the target silently stops
   working the day a file of that name appears.
5. Every declared CLI answers `--help`.

**What this does NOT do:** run the commands. `make -n` prints a recipe; a command
that fails *inside* passes here. This proves the interface exists and resolves, not
that it works -- that is `make check` in CI, which runs the real thing.

Usage:
    uv run python scripts/check_commands.py            # exit 1 on any breakage
    uv run python scripts/check_commands.py --verbose  # list what was checked
    uv run python scripts/check_commands.py --root .   # verify a different project

`--root` exists because the harness runs this very file against *itself* rather than
keeping a second copy. Inside a PoC the default is right -- the script sits in
`scripts/`, so the project root is one level up. Run from the harness the same
arithmetic lands on `template/`, which has no Makefile, so the harness passes
`--root .` explicitly.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: A target counts as documented only with a `##` description -- the same rule the
#: harness auditor uses, because a target absent from `make help` does not exist as
#: far as a newcomer is concerned.
_DOCUMENTED_TARGET = re.compile(r"^([a-z][a-z0-9-]*):.*?##", re.MULTILINE)

_PHONY = re.compile(r"^\.PHONY:(.*)$", re.MULTILINE)

#: A script path in a recipe. Restricted to `.py` on purpose: matching every token
#: that looks like a path reports directories, make variables and URLs.
_SCRIPT = re.compile(r"(?<![\w./-])((?:[\w.-]+/)*[\w.-]+\.py)(?![\w/])")

#: `python -m harness.audit` and friends.
_MODULE = re.compile(r"-m\s+([a-z_][\w.]*)")

#: Entry points to smoke-test with `--help`. A CLI that stops starting at all is a
#: different failure from a target that stops resolving, and neither implies the other.
CLI_ENTRY_POINTS: tuple[tuple[str, ...], ...] = (
    ("python", "scripts/check_snippets.py", "--help"),
    ("python", "scripts/sync_docs_pages.py", "--help"),
    ("python", "scripts/check_commands.py", "--help"),
)

#: Targets never dry-run: `make -n` on a recursive target re-invokes make for real.
#: None today; kept so the reason is on record if one appears.
SKIP_DRY_RUN: frozenset[str] = frozenset()


def documented_targets(makefile: Path) -> list[str]:
    """Targets carrying a `## description`, in the order they appear."""
    if not makefile.is_file():
        return []
    return _DOCUMENTED_TARGET.findall(makefile.read_text())


def phony_targets(makefile: Path) -> set[str]:
    """Everything listed in `.PHONY`, across however many declarations there are."""
    if not makefile.is_file():
        return set()
    return {name for line in _PHONY.findall(makefile.read_text()) for name in line.split()}


def _recipe_lines(makefile: Path) -> list[str]:
    """Only the recipe lines -- the tab-indented ones make hands to the shell.

    Comments are excluded: a comment naming a script that was later deleted is
    stale prose, not a broken command, and reporting it would train people to
    ignore this check.
    """
    return [
        line
        for line in makefile.read_text().split("\n")
        if line.startswith("\t") and not line.lstrip().startswith("#")
    ]


def missing_scripts(makefile: Path, repo_root: Path) -> list[str]:
    """Script paths a recipe invokes that are not on disk."""
    referenced = {match for line in _recipe_lines(makefile) for match in _SCRIPT.findall(line)}
    return sorted(path for path in referenced if not (repo_root / path).is_file())


def unimportable_modules(makefile: Path, repo_root: Path) -> list[str]:
    """Modules a recipe runs with `-m` that cannot be imported."""
    referenced = {match for line in _recipe_lines(makefile) for match in _MODULE.findall(line)}
    broken: list[str] = []
    for module in sorted(referenced):
        probe = subprocess.run(
            [sys.executable, "-c", f"import importlib.util as u; assert u.find_spec({module!r})"],
            cwd=repo_root,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if probe.returncode != 0:
            broken.append(module)
    return broken


def unresolvable_targets(makefile: Path, repo_root: Path) -> list[str]:
    """Documented targets that `make -n` cannot expand."""
    broken: list[str] = []
    for target in documented_targets(makefile):
        if target in SKIP_DRY_RUN:
            continue
        result = subprocess.run(
            ["make", "-n", target],
            cwd=repo_root,
            capture_output=True,
            check=False,
            timeout=120,
        )
        if result.returncode != 0:
            broken.append(target)
    return broken


def undeclared_phony(makefile: Path) -> list[str]:
    """Documented targets missing from `.PHONY`."""
    return sorted(set(documented_targets(makefile)) - phony_targets(makefile))


def removed_targets(repo_root: Path) -> list[str]:
    """Documented targets that `HEAD` has and the working tree does not.

    The static checks above cannot see this: a deleted target is no longer
    documented, so there is nothing left to resolve. Yet deleting a command is the
    plainest way to break one, which is the whole point of this script.

    **Reported as a warning, not a failure.** Removing a target is often deliberate,
    and a hook that blocks it would have to grow an escape hatch that everyone
    learns to use reflexively. Removing a target the *standard* requires is a
    different matter and stays an error -- the harness auditor's `make-targets` rule
    covers that, and it should, because there the answer is never "yes, on purpose".

    Silent when there is no previous state to compare against: a fresh repo with no
    commit, or no git at all.
    """
    previous = subprocess.run(
        ["git", "-C", str(repo_root), "show", "HEAD:Makefile"],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if previous.returncode != 0:
        return []

    before = set(_DOCUMENTED_TARGET.findall(previous.stdout))
    after = set(documented_targets(repo_root / "Makefile"))
    return sorted(before - after)


def broken_entry_points(repo_root: Path) -> list[str]:
    """Declared CLIs that do not answer `--help` cleanly.

    Skipped rather than reported when the script is absent: `missing_scripts`
    already covers a recipe pointing at a file that is gone, and a PoC is free not
    to ship one of these.
    """
    broken: list[str] = []
    for command in CLI_ENTRY_POINTS:
        script = next((part for part in command if part.endswith(".py")), None)
        if script and not (repo_root / script).is_file():
            continue
        resolved = [sys.executable if part == "python" else part for part in command]
        result = subprocess.run(
            resolved, cwd=repo_root, capture_output=True, check=False, timeout=120
        )
        if result.returncode != 0:
            broken.append(" ".join(command))
    return broken


def check(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return one description per broken command. Empty means the interface holds."""
    makefile = repo_root / "Makefile"
    if not makefile.is_file():
        return ["no Makefile -- there is no command interface to verify"]

    problems: list[str] = []
    for target in unresolvable_targets(makefile, repo_root):
        problems.append(
            f"`make {target}` does not resolve -- deleted target, or a broken prerequisite"
        )
    for path in missing_scripts(makefile, repo_root):
        problems.append(f"a recipe runs {path}, which does not exist")
    for module in unimportable_modules(makefile, repo_root):
        problems.append(f"a recipe runs `-m {module}`, which is not importable")
    for target in undeclared_phony(makefile):
        problems.append(
            f"`{target}` is documented but not in .PHONY -- it breaks the day a file "
            f"of that name exists"
        )
    for command in broken_entry_points(repo_root):
        problems.append(f"`{command}` exits non-zero")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the documented commands resolve.")
    parser.add_argument("--verbose", action="store_true", help="list what was checked")
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="project to verify (default: the directory above this script)",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    makefile = root / "Makefile"
    problems = check(root)

    if args.verbose:
        targets = documented_targets(makefile)
        print(f"{root}: {len(targets)} documented target(s): {', '.join(targets)}")
        # Counted, not assumed: in the harness none of these scripts sit at the root,
        # so all three are skipped. Reporting "3 entry points" there would be a lie
        # in a line whose whole job is to say what was covered.
        present = [
            " ".join(command)
            for command in CLI_ENTRY_POINTS
            if all((root / part).is_file() for part in command if part.endswith(".py"))
        ]
        skipped = len(CLI_ENTRY_POINTS) - len(present)
        print(f"{len(present)} CLI entry point(s) checked, {skipped} absent and skipped")
        for command in present:
            print(f"  {command}")

    for target in removed_targets(root):
        print(
            f"note: `make {target}` existed in HEAD and is gone. Deliberate? "
            f"If the standard requires it, `make audit` will say so.",
            file=sys.stderr,
        )

    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"\n{len(problems)} broken command(s)", file=sys.stderr)
        return 1

    print("all documented commands resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

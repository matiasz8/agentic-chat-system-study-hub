"""Keep docs-site MDX snippets byte-identical to the code that actually runs.

Python files mark named regions:

    # --8<-- [start:create-edge]
    ...
    # --8<-- [end:create-edge]

MDX declares which region a fence shows, immediately above the fence:

    {/* snippet: mypackage/module.py#create-edge */}

    ```python
    ...
    ```

Usage:
    uv run python scripts/check_snippets.py          # verify, exit 1 on drift
    uv run python scripts/check_snippets.py --fix    # rewrite fences from source

Note: ruff is configured NOT to format Markdown (see pyproject.toml). Two
formatters fighting over these fences would make this check unfixable.

Proven in graph-pocs, where 18 tests cover it. Kept verbatim on purpose -- do not
rename `--fix` or the marker syntax, since the docs-site pages reference both.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = Path("docs-site") / "content"

_START = "# --8<-- [start:{region}]"
_END = "# --8<-- [end:{region}]"

_DECLARATION = re.compile(
    r"\{/\*\s*snippet:\s*(?P<path>[^#\s]+)#(?P<region>[\w-]+)\s*\*/\}"
    r"\s*\n\s*\n"
    r"```(?P<lang>[\w-]*)\n"
    r"(?P<code>.*?)"
    r"```",
    re.DOTALL,
)


class RegionNotFoundError(ValueError):
    """The named region does not exist in the source file."""


@dataclass(frozen=True, slots=True)
class SnippetRef:
    mdx_path: Path
    line: int
    source_path: str
    region: str
    fenced_code: str


def extract_region(source: str, region: str) -> str:
    """Return the code between the region's markers, dedented and stripped."""
    start_marker = _START.format(region=region)
    end_marker = _END.format(region=region)

    lines = source.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == start_marker), None)
    end = next((i for i, line in enumerate(lines) if line.strip() == end_marker), None)

    if start is None or end is None or end < start:
        raise RegionNotFoundError(
            f"region {region!r} not found (expected {start_marker!r} and {end_marker!r})"
        )

    return dedent("\n".join(lines[start + 1 : end])).strip("\n")


def find_refs(mdx_text: str, mdx_path: Path) -> list[SnippetRef]:
    """Find every snippet declaration and the fence that follows it."""
    return [
        SnippetRef(
            mdx_path=mdx_path,
            line=mdx_text[: match.start()].count("\n") + 1,
            source_path=match.group("path"),
            region=match.group("region"),
            fenced_code=match.group("code").strip("\n"),
        )
        for match in _DECLARATION.finditer(mdx_text)
    ]


def _mdx_files(repo_root: Path) -> list[Path]:
    content = repo_root / CONTENT_DIR
    return sorted(content.rglob("*.mdx")) if content.is_dir() else []


def check(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return one description per drifted or unresolvable snippet."""
    problems: list[str] = []

    for mdx_path in _mdx_files(repo_root):
        for ref in find_refs(mdx_path.read_text(), mdx_path):
            source_file = repo_root / ref.source_path
            location = f"{ref.mdx_path.relative_to(repo_root)}:{ref.line}"

            if not source_file.is_file():
                problems.append(f"{location}: source file not found: {ref.source_path}")
                continue

            try:
                expected = extract_region(source_file.read_text(), ref.region)
            except RegionNotFoundError as error:
                problems.append(f"{location}: {error}")
                continue

            if expected != ref.fenced_code:
                problems.append(
                    f"{location}: snippet '{ref.source_path}#{ref.region}' is out of date "
                    f"(run: uv run python scripts/check_snippets.py --fix)"
                )

    return problems


def fix(repo_root: Path = REPO_ROOT) -> list[Path]:
    """Rewrite every drifted fence from its source. Returns the changed files."""
    changed: list[Path] = []

    def replace(match: re.Match[str]) -> str:
        source_file = repo_root / match.group("path")
        if not source_file.is_file():
            return match.group(0)
        try:
            expected = extract_region(source_file.read_text(), match.group("region"))
        except RegionNotFoundError:
            return match.group(0)

        declaration = match.group(0).split("```")[0]
        lang = match.group("lang") or "python"
        return f"{declaration}```{lang}\n{expected}\n```"

    for mdx_path in _mdx_files(repo_root):
        original = mdx_path.read_text()
        updated = _DECLARATION.sub(replace, original)
        if updated != original:
            mdx_path.write_text(updated)
            changed.append(mdx_path)

    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check docs-site snippets against source.")
    parser.add_argument("--fix", action="store_true", help="rewrite drifted MDX fences from source")
    args = parser.parse_args(argv)

    if args.fix:
        changed = fix()
        for path in changed:
            print(f"updated {path.relative_to(REPO_ROOT)}")
        print(f"{len(changed)} file(s) updated")
        return 0

    problems = check()
    for problem in problems:
        print(problem, file=sys.stderr)

    if problems:
        print(f"\n{len(problems)} snippet(s) out of sync", file=sys.stderr)
        return 1

    print("all docs-site snippets match the source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

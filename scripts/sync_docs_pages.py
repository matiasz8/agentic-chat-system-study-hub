"""Generate the documentation site's pages from the Markdown in `docs/`.

**`docs/` is the source of truth. The site is a build artefact.**

You write plain Markdown. This turns it into the site's MDX. Two reasons that
split is worth the script:

1. You never author MDX. MDX v3 is strict in ways plain prose trips over (see
   `_escape_for_mdx`), and hitting those while writing about something else is
   a bad use of anyone's afternoon.
2. **The generator becomes replaceable.** Nothing in `docs/` is Nextra-specific,
   so swapping the site generator later does not mean rewriting content.

Usage:
    uv run python scripts/sync_docs_pages.py           # verify, exit 1 on drift
    uv run python scripts/sync_docs_pages.py --write   # regenerate the pages

`make check` runs the verify form, so a stale page fails the build.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
CONTENT = REPO_ROOT / "docs-site" / "content"

#: Documents that are not study material and do not belong on the site.
EXCLUDE = ("README.md",)

#: Directories under docs/ that are process artefacts, not content.
EXCLUDE_DIRS = ("superpowers", "decisions")

#: `<` immediately before a digit starts a JSX tag in MDX v3, so "<10MB" is a
#: parse error. Real case, found by a build failure.
_LT_DIGIT = re.compile(r"<(?=\d)")

#: MDX v3 evaluates `{...}` as JavaScript. "{Jan, Feb, Mar}" in prose becomes
#: `ReferenceError: Jan is not defined` at prerender. Only escape brace groups
#: that look like prose -- no quotes, dots or parens.
_PROSE_BRACE = re.compile(r"\{([A-Za-z][A-Za-z0-9 ,_/-]*)\}")


def _escape_for_mdx(markdown: str) -> str:
    """Make plain Markdown safe for an MDX parser, leaving code fences alone.

    Every rule here exists because a build failed on real prose, not on a
    hypothetical.
    """
    out: list[str] = []
    in_fence = False
    in_comment = False
    for line in markdown.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        # An HTML comment is not a comment in MDX -- `<!` starts a broken JSX tag and
        # the build dies on "Unexpected character `!`". Rewrite the delimiters and
        # leave the body alone: inside `{/* */}` nothing needs escaping. Tracked as
        # state rather than a plain replace so a `-->` arrow in prose survives.
        if in_comment:
            if "-->" in line:
                line = line.replace("-->", "*/}", 1)
                in_comment = False
            out.append(line)
            continue
        if "<!--" in line:
            line = line.replace("<!--", "{/*", 1)
            if "-->" in line:
                line = line.replace("-->", "*/}", 1)
            else:
                in_comment = True
            out.append(line)
            continue

        line = _LT_DIGIT.sub("&lt;", line)
        line = _PROSE_BRACE.sub(lambda m: "\\{" + m.group(1) + "\\}", line)
        out.append(line)
    return "\n".join(out)


def _banner(source: str) -> str:
    """An MDX comment marking the file as generated.

    Built by concatenation, not str.format: the MDX comment opener `{/*` looks
    like a format field and would raise KeyError.
    """
    return (
        "{/* GENERATED FILE -- do not edit.\n"
        f"    Source: {source}\n"
        "    Regenerate: uv run python scripts/sync_docs_pages.py --write */}\n"
    )


def source_pages(docs: Path = DOCS) -> list[Path]:
    """Every Markdown file under docs/ that belongs on the site."""
    if not docs.is_dir():
        return []
    return sorted(
        p
        for p in docs.rglob("*.md")
        if p.name not in EXCLUDE
        and not any(part in EXCLUDE_DIRS for part in p.relative_to(docs).parts)
    )


def render(source: Path, docs: Path = DOCS) -> str:
    """Return the MDX body for one source document."""
    relative = source.relative_to(docs)
    return f"{_banner(f'docs/{relative}')}\n{_escape_for_mdx(source.read_text())}"


def target_for(source: Path, docs: Path = DOCS, content: Path = CONTENT) -> Path:
    """Where a source document's page lives on the site."""
    return (content / source.relative_to(docs)).with_suffix(".mdx")


def check(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return one description per page that is missing or out of date."""
    docs, content = repo_root / "docs", repo_root / "docs-site" / "content"
    problems: list[str] = []
    for source in source_pages(docs):
        target = target_for(source, docs, content)
        expected = render(source, docs)
        if not target.is_file():
            problems.append(f"{target.relative_to(repo_root)}: missing (run --write)")
        elif target.read_text() != expected:
            problems.append(
                f"{target.relative_to(repo_root)}: out of date with "
                f"docs/{source.relative_to(docs)} (run --write)"
            )
    return problems


def write(repo_root: Path = REPO_ROOT) -> list[Path]:
    """Regenerate every page. Returns the ones that changed."""
    docs, content = repo_root / "docs", repo_root / "docs-site" / "content"
    changed: list[Path] = []
    for source in source_pages(docs):
        target = target_for(source, docs, content)
        expected = render(source, docs)
        if not target.is_file() or target.read_text() != expected:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected)
            changed.append(target)
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync docs-site pages from docs/.")
    parser.add_argument("--write", action="store_true", help="regenerate the pages")
    args = parser.parse_args(argv)

    if args.write:
        changed = write()
        for path in changed:
            print(f"wrote {path.relative_to(REPO_ROOT)}")
        print(f"{len(changed)} page(s) updated")
        return 0

    problems = check()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"\n{len(problems)} page(s) out of sync with docs/", file=sys.stderr)
        return 1

    print("all generated docs-site pages match docs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

---
name: docs-site
description: Add or edit pages on this PoC's Nextra documentation site, and show real code on them without it drifting. Use when writing documentation for this PoC, adding a page, or putting a code snippet on the site.
---

# Working on the docs site

The site lives in `docs-site/`. **Node lives only there** — the Python side has no Node
dependency, and adding one to the repo root breaks that boundary.

```bash
make docs          # dev server on http://localhost:3000
make docs-build    # production build; also builds the search index
```

Search (Pagefind) indexes the **built** HTML, so it is silently empty in `make docs`.
That is expected. Use `make docs-build` to test search.

## Adding a page

1. Create the MDX file under `docs-site/content/`, e.g. `content/model.mdx`.
2. **Add it to the `_meta.js` in that directory.** Nextra uses `_meta.js` for ordering
   and titles; a page missing from it still renders but loses its place in the
   navigation, which is how pages quietly become unreachable.

```javascript
export default {
  index: 'Overview',
  model: 'The model'
}
```

3. Subdirectories get their own `_meta.js`.

This is Nextra 4 with the **App Router** and the `content/` directory convention. Do
not follow Nextra 2/3 tutorials — they use the Pages Router, `theme.config.jsx`, and a
`pages/` directory, none of which apply here.

## Showing code on the site

Never paste code into MDX by hand. Pasted code drifts from the source silently, and
documentation that describes code which does not exist is worse than no documentation.

**1. Mark a region in the Python file:**

```python
# --8<-- [start:my-region]
value = compute()
print(value)
# --8<-- [end:my-region]
```

**2. Declare it in the MDX**, immediately above an empty fence:

    {/* snippet: mypackage/module.py#my-region */}

    ```python
    ```

**3. Populate it from source:**

```bash
uv run python scripts/check_snippets.py --fix
```

**4. Verify:**

```bash
make check-snippets
```

`make check` runs that check, so a drifted snippet fails the build. If you change the
Python, re-run `--fix` and review the diff — the check will tell you which pages went
stale.

## Two things that will bite you

**Ruff must not format Markdown.** `pyproject.toml` sets
`extend-exclude = ["*.md", "*.mdx"]`. Ruff formats Python code blocks inside Markdown by
default, and if it does, it fights the snippet checker over the same bytes and the check
becomes unfixable. Do not remove that exclusion.

**Dependencies are pinned exactly, and the `zod` override is required.**
`nextra-theme-docs` declares a caret range for zod; a newer zod makes every page fail to
prerender with `expected nonoptional, received undefined -> at children`. The reason is
recorded in `docs-site/package.json` under `_overridesReason`. Keys inside `overrides`
must be package names only — npm rejects anything else outright.

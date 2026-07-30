# 0001 — Adopt the poc-harness standard

- **Date:** 2026-07-30
- **Status:** accepted

## Context

The repo had a Makefile and husky hooks but no linter, formatter, type checking, CI or
`.env.example`. Dependencies were a `requirements.txt` beside a committed `venv/`. The
Nextra 2 documentation site lived at the repo root, so `package.json`, `tsconfig.json`
and `node_modules` sat next to the Python code.

## Decision

Adopt the standard defined by `poc-harness-template`.

## Consequences

- `requirements.txt` → `pyproject.toml` with uv; `venv/` gitignored.
- ruff, mypy, pre-commit and CI where there were none. husky removed in favour of
  pre-commit, which needs no root `package.json`.
- The site moves to `docs-site/`, so the Python side has **no Node dependency**.
- Nextra 2 Pages Router → Nextra 4 App Router.

## Deviations

- **Documentation stays in Spanish.** Translating 66 pages is churn with no reader.
- **`.python-version` is 3.14**, matching what the project already resolved on.
- **Not an installable package** — `[tool.uv] package = false`. This is study material
  and scripts, not a library.

## What the migration cost, and what it exposed

- 11 `_meta` keys pointed at pages that do not exist. Nextra 2 ignored them; Nextra 4
  fails the build. Pruned — but the pages are still missing, see `../findings.md`.
- Two components used `next/router`, which the App Router does not have. Ported to
  `usePathname()` from `next/navigation`.
- The `validate:*` npm scripts were dropped with the root `package.json`. Nextra 4
  validates `_meta` and links at build time, which covers most of their purpose.

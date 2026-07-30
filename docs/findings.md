# Findings

## Answer to the question

**Can LangGraph-based agentic chat patterns be taught and validated in a repeatable
way?** Substantially yes: 28 tests cover the prompt and workflow validation paths and
they pass, and the study material now renders as 66 navigable pages.

## What is verified, and what is not

**Verified:**

- The Python validation suite: 28 tests, about 2 seconds. Covers prompt validation and
  the workflow fixtures.
- The documentation site builds and indexes **66 pages**.

**Not verified:**

- The example modules under `python/modulos/` are not exercised by tests. They need a
  real `ANTHROPIC_API_KEY` to run and nothing mocks them.
- Nothing has been run against a live LLM in this repo.

## What surprised us

**Nextra 4 validates `_meta` keys; Nextra 2 silently ignored dangling ones.** The
migration surfaced **11 keys across 4 files** pointing at pages that do not exist —
`00-intro` in three exercise sections, plus others. Under Nextra 2 those entries simply
never rendered and nobody noticed. Under Nextra 4 they fail the build outright, which
is the better behaviour: a navigation entry for a page nobody wrote is a broken promise
to the reader.

The missing pages are still missing. Pruning the keys made the build pass; it did not
write `00-intro`. See "Next steps".

**`next/router` does not exist in the App Router.** `RouteProgress.jsx` and
`TOCHeader.tsx` both used `useRouter().asPath` to know the current page. The App Router
equivalent is `usePathname()` from `next/navigation`. Symptom was
`NextRouter was not mounted` at prerender — a runtime error, not a compile error, so
`tsc` and the build both looked fine right up until page generation.

**The documentation site lived at the repo root**, which meant a `package.json`,
`tsconfig.json` and `node_modules` sat beside the Python code. Moving it to
`docs-site/` means the Python side has no Node dependency at all.

## Deliberate deviations from the harness standard

- **Documentation stays in Spanish.** The standard is English for new material; this
  repo predates it and translating 66 pages is churn with no reader. Decided
  2026-07-30. The tooling and code comments are English.
- **`.python-version` is 3.14**, matching the interpreter the project already resolves
  on. A tooling retrofit should not change runtime behaviour.
- **Not an installable package.** `python/modulos` and `python/validation` are study
  material and scripts, not a library, so `[tool.uv] package = false`.

## Next steps

1. **Write the pages the navigation used to promise**, or decide they are not coming:
   `00-intro` for the basic, intermediate and advanced exercise tracks, plus
   `03-nodo-simple`, `04-conditional-routing`, `05-llm-decision`, `06-error-handling`,
   `07-multi-agent`, `08-generative-ui` and `09-testing-advanced`. The prior structure
   implies these were planned.
2. **Cover `python/modulos/` with tests** using a mock LLM. `python/validation/mock_llm.py`
   already exists and is the obvious starting point.
3. The old `validate:routes` / `validate:links` / `validate:build` npm scripts were
   dropped with the root `package.json`. Nextra 4 validates `_meta` and links at build
   time, which covers most of what they did — but confirm before assuming.

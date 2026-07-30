# agentic-chat-system-study-hub — overview

A study hub for building agentic chat systems: LangGraph workflows, generative UI
patterns, and prompt validation — with runnable examples and a validation suite.

## The question

What does it take to build and validate an agentic chat system well enough to trust it,
and can that be taught in a repeatable way?

> This needs the real framing from whoever owns the material — what decision it informs,
> and who the audience is.

## Out of scope

- Production deployment of any agent built from the material.
- Model comparison; the examples target Anthropic models.

## How we will know it worked

Someone works through the study site, runs the examples, and can then build and
validate a small agentic workflow of their own.

**Current state:** 28 validation tests pass; the site builds with 66 pages. The example
modules under `python/modulos/` are not covered by tests and need a live API key. See
`findings.md`.

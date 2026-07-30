# Documentation for agentic-chat-system-study-hub

## The rule

**If it stops being true next week, it does not belong here.** Progress trackers and
status dashboards expire — they belong in the ticket.

Removed when this repo adopted the harness standard: `PLAN.md`,
`PROGRESS_TRACKING.md`, `PROJECT_STATUS.md` and the `archived/` directory. All
recoverable from git history.

## What lives here

| Path | Holds |
|---|---|
| `00-overview.md` | what this study hub is, and what it is not |
| `decisions/` | one decision per file, with its reasoning |
| `reference/` | architecture, performance, structure and the validation notes |
| `findings.md` | **what we learned — the deliverable** |

The study material itself is the documentation site (`docs-site/`), 66 pages. Run it
with `make docs`.

## A note on language

The study material and these reference documents are in **Spanish**, deliberately. The
harness standard asks for English on new material; this repo predates it and
translating 66 pages would be churn with no reader. Tooling, code comments and commit
messages are English.

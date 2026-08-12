.DEFAULT_GOAL := help
UV ?= uv
NPM ?= npm

.PHONY: help setup check check-commands test lint fmt typecheck compile-examples docs docs-build check-snippets check-docs-pages sync-docs-pages clean

help: ## Show the available targets
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and git hooks, and generate the site's pages
	# `--all-groups`, not the template's `--extra dev`: this project keeps its
	# dependencies in dependency-groups.
	$(UV) sync --all-groups
	$(UV) run pre-commit install
	cd docs-site && $(NPM) install
	# The site is a build artefact, so the template ships no pages -- it ships the
	# `docs/` they come from. Without this line `make check` is red on a fresh
	# scaffold, which is how it shipped until 2026-07-31.
	$(UV) run python scripts/sync_docs_pages.py --write

check: lint typecheck check-commands compile-examples check-snippets check-docs-pages test ## Everything CI runs

test: ## Run the test suite
	$(UV) run python -m pytest -v

lint: ## Lint and format-check
	$(UV) run ruff check .
	$(UV) run ruff format --check .

fmt: ## Apply formatting and safe fixes
	$(UV) run ruff format .
	$(UV) run ruff check --fix .

typecheck: ## Static type check (validation code; examples are standalone scripts)
	$(UV) run mypy python/validation test_setup.py

compile-examples: ## Syntax-check the study modules mypy deliberately skips
	$(UV) run python -m compileall -q python/modulos

check-commands: ## Verify every documented command still resolves
	$(UV) run python scripts/check_commands.py

check-snippets: ## Verify docs-site snippets match the real code
	$(UV) run python scripts/check_snippets.py

check-docs-pages: ## Verify the site's pages match docs/
	$(UV) run python scripts/sync_docs_pages.py

sync-docs-pages: ## Regenerate the site's pages from docs/ (docs/ is the source)
	$(UV) run python scripts/sync_docs_pages.py --write

docs: ## Run the documentation site in dev (search needs docs-build)
	cd docs-site && $(NPM) run dev

docs-build: ## Build the docs site and its search index
	cd docs-site && $(NPM) run build

clean: ## Remove generated artefacts and caches
	rm -rf .pytest_cache .ruff_cache .mypy_cache docs-site/.next docs-site/public/_pagefind

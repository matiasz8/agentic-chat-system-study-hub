.DEFAULT_GOAL := help
UV ?= uv
NPM ?= npm

.PHONY: help setup check test lint fmt typecheck docs docs-build check-snippets check-docs-pages sync-docs-pages clean

help: ## Show the available targets
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup: ## Install Python and docs-site dependencies, plus git hooks
	$(UV) sync --all-groups
	$(UV) run pre-commit install
	cd docs-site && $(NPM) install

check: lint typecheck check-snippets check-docs-pages test ## Everything CI runs

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

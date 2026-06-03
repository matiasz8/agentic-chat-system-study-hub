.PHONY: help install run dev build lint validate clean test

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Agentic Chat System Study Hub$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

# Install targets
install: install-node install-python ## Install all dependencies

install-node: ## Install Node.js dependencies
	@echo "$(BLUE)Installing Node.js dependencies...$(NC)"
	npm install
	@echo "$(GREEN)✓ Node.js dependencies installed$(NC)"

install-python: ## Install Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	@echo "$(GREEN)✓ Python dependencies installed$(NC)"

install-husky: ## Install Husky git hooks
	@echo "$(BLUE)Installing Husky git hooks...$(NC)"
	npm run prepare
	@echo "$(GREEN)✓ Husky hooks installed$(NC)"

# Development targets
dev: ## Start development server (http://localhost:3000)
	@echo "$(BLUE)Starting development server...$(NC)"
	npm run dev

run: dev ## Alias for 'dev' - Start development server

build: ## Build for production
	@echo "$(BLUE)Building for production...$(NC)"
	npm run build
	@echo "$(GREEN)✓ Production build complete$(NC)"

start: ## Start production server
	@echo "$(BLUE)Starting production server...$(NC)"
	npm start

# Validation targets
lint: ## Run linter (ESLint)
	@echo "$(BLUE)Running linter...$(NC)"
	npm run lint

validate: ## Run all validation checks (routes, links, build)
	@echo "$(BLUE)Running all validation checks...$(NC)"
	npm run validate
	@echo "$(GREEN)✓ All validations passed$(NC)"

validate-routes: ## Validate routes
	@echo "$(BLUE)Validating routes...$(NC)"
	npm run validate:routes

validate-links: ## Validate all links
	@echo "$(BLUE)Validating links...$(NC)"
	npm run validate:links

validate-build: ## Validate build integrity
	@echo "$(BLUE)Validating build...$(NC)"
	npm run validate:build

# Testing targets
test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	npm test
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-python: ## Run Python tests
	@echo "$(BLUE)Running Python tests...$(NC)"
	python3 -m pytest python/ -v

# Cleanup targets
clean: clean-node clean-python ## Clean all build artifacts

clean-node: ## Clean Node.js artifacts
	@echo "$(BLUE)Cleaning Node.js artifacts...$(NC)"
	rm -rf .next
	rm -rf node_modules
	rm -f package-lock.json
	@echo "$(GREEN)✓ Node.js artifacts cleaned$(NC)"

clean-python: ## Clean Python artifacts
	@echo "$(BLUE)Cleaning Python artifacts...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf venv
	@echo "$(GREEN)✓ Python artifacts cleaned$(NC)"

# Setup targets
setup: install install-husky validate ## Complete setup (install all + validate)
	@echo "$(GREEN)✓ Project setup complete$(NC)"

# Info targets
info: ## Show project information
	@echo "$(BLUE)Project Information:$(NC)"
	@echo "  Project: Agentic Chat System Study Hub"
	@echo "  Node: $$(node --version)"
	@echo "  npm: $$(npm --version)"
	@echo "  Python: $$(python3 --version)"
	@echo ""
	@echo "$(BLUE)Directories:$(NC)"
	@echo "  - /pages       - Website content (MDX)"
	@echo "  - /docs        - Documentation"
	@echo "  - /components  - React components"
	@echo "  - /scripts     - Build/validation scripts"
	@echo "  - /python      - Python modules and examples"
	@echo "  - /public      - Static assets"

# Documentation
docs: ## View documentation structure
	@echo "$(BLUE)Documentation Structure:$(NC)"
	@cat docs/STRUCTURE.md

# Quick start
quickstart: ## Quick start guide
	@echo "$(GREEN)Quick Start Guide:$(NC)"
	@echo ""
	@echo "1. Setup project:"
	@echo "   $$ make setup"
	@echo ""
	@echo "2. Start development:"
	@echo "   $$ make run"
	@echo ""
	@echo "3. Validate changes:"
	@echo "   $$ make validate"
	@echo ""
	@echo "4. Build for production:"
	@echo "   $$ make build"
	@echo ""
	@echo "For more info: make help"

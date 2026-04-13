.PHONY: docs help validate check-docs

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

docs: ## Serve docs site with live reload
	@command -v uv >/dev/null 2>&1 || { echo "uv not found — install from https://docs.astral.sh/uv/"; exit 1; }
	@echo "Serving docs at http://localhost:8000 (live reload enabled)"
	@uv run scripts/serve-docs.py

validate: ## Validate all SKILL.md files
	@command -v uv >/dev/null 2>&1 || { echo "uv not found — install from https://docs.astral.sh/uv/"; exit 1; }
	@uv run scripts/validate-skills.py

check-docs: ## Check docs are in sync with skills/
	@command -v uv >/dev/null 2>&1 || { echo "uv not found — install from https://docs.astral.sh/uv/"; exit 1; }
	@uv run scripts/sync-docs.py

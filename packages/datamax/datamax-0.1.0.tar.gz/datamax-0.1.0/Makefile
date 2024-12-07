
.PHONY := format lint clean

lint:
	@echo "Running linters"
	@rye run ruff check
	@rye run isort . --check --diff

format:
	@echo "Running formatters"
	@rye run ruff format
	@rye run isort .

test:
	@echo "Running tests"
	@rye run pytest

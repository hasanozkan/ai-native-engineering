.PHONY: install check lint types test memory selfcheck

install:
	uv sync

check: lint types test memory selfcheck

lint:
	uv run ruff check . && uv run ruff format --check .

types:
	uv run mypy

test:
	uv run pytest -q

memory:
	uv run python tools/memory_lint.py examples/memory

# The repo eats its own cooking: its test gate must catch a broken rule.
selfcheck:
	uv run python tools/negative_control.py --check "uv run pytest -q tests/test_branch_name.py" \
	  --file tools/branch_name.py --replace '"--" in rest' --with '"---" in rest'

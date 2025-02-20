# All variables will be exported to child processes. Can be useful later.
.EXPORT_ALL_VARIABLES:

# So we're sure what shell we're using.
SHELL:=/bin/bash

# Directory or file to scan for tests. Can also be a single tests. Can be overridden.
TESTS_LOCATION:=.

SRC_DIRECTORIES:=sample_backend alembic_migrations

# MAIN COMMANDS
# ==============

# First-time setup of the project.
setup:
	poetry install --no-root
	pre-commit install

# Run the project.
run: _start_compose db_migration

# Run the project, reloading it on code file changes.
run_reload:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make run

# Do all the quality checks.
check: static_checks run test

test:
	@echo ================
	@echo Running tests...
	@echo ================
	poetry run pytest -n auto -v -m "not non_parallel" $(TESTS_LOCATION)
	poetry run pytest -v -m "non_parallel" $(TESTS_LOCATION)

# This doesn't use xdist to parallelize the tests like the standard "test" target.
# This allows using a debugger.
test_debug:
	@echo ==========================
	@echo Running tests for debug...
	@echo ==========================
	poetry run pytest -v $(TESTS_LOCATION)

# Observe Python files for changes, run tests when a file gets modified.
# Can be parameterized to pick the tests to run,
# e.g. `make test_reload TESTS_LOCATION=sample_backend/interface/routers/notes_test.py`
test_reload:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make test_debug

format:
	@echo ==================
	@echo Formatting code...
	@echo ==================
	poetry run ruff format $(SRC_DIRECTORIES)
	# Import sorting like isort.
	poetry run ruff check $(SRC_DIRECTORIES) --select I --fix

# UTILITY COMMANDS
# ================

destroy:
	docker compose down -v

show_api_documentation:
	xdg-open http://localhost:8080/docs

shell:
	poetry run ptpython

shell_db:
	PGPASSWORD=postgres poetry run pgcli -h localhost -p 5432 -U postgres -d postgres

shell_docker_app:
	docker compose exec api sh

# Fix everything that Ruff proposes to fix.
code_fixes:
	poetry run ruff check $(SRC_DIRECTORIES) --fix

# SUBCOMMANDS
# ===========

db_migration:
	@echo ========================
	@echo Running DB migrations...
	@echo ========================
	poetry run alembic upgrade head

# Usage make db_migration_create MESSAGE="<a message>"
db_migration_create:
	@echo ===============================
	@echo Autogenerating DB migrations...
	@echo ===============================
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

_start_compose: _export_requirements
	@echo ==========================
	@echo Starting Docker Compose...
	@echo ==========================
	docker compose up --build -d

_export_requirements:
	poetry export --output=requirements.txt

static_checks: _check_types _check_format _check_linter _check_types

_check_types:
	@echo =================
	@echo Checking types...
	@echo =================
	poetry run mypy $(SRC_DIRECTORIES)

_check_linter:
	@echo ===================
	@echo Checking linters...
	@echo ===================
	poetry run ruff check $(SRC_DIRECTORIES)

_check_format:
	@echo ======================
	@echo Checking formatting...
	@echo ======================
	poetry run ruff format --check $(SRC_DIRECTORIES)

# All variables will be exported to child processes. Can be useful later.
.EXPORT_ALL_VARIABLES:

# So we're sure what shell we're using.
SHELL:=/bin/bash

SRC_DIRECTORIES:=sample_backend tests

# MAIN COMMANDS
# ==============

setup:
	poetry install --no-root

run: _start_compose db_migration

run_reload:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make run

check: static_checks run test

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

db_shell:
	PGPASSWORD=postgres poetry run pgcli -h localhost -p 5432 -U postgres -d postgres

docker_app_shell:
	docker exec -it sample_backend_app-api-1 sh

code_fixes:
	poetry run ruff check $(SRC_DIRECTORIES) --fix

# SUBCOMMANDS
# ===========

db_migration:
	@echo "=== Running DB migrations... ==="
	poetry run alembic upgrade head

# Usage make make_migration MESSAGE="<a message>"
make_migration:
	@echo "=== Autogenerating DB migrations... ==="
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

_start_compose: _export_requirements
	@echo "=== Starting Docker Compose... ==="
	docker compose up --build -d

_export_requirements:
	poetry export --output=requirements.txt

test:
	@echo ================
	@echo Running tests...
	@echo ================
	poetry run pytest -v tests

test_reload:
	fd --exclude .git --no-ignore '\.py$$' | entr -c make test

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


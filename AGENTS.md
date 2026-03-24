# AGENTS.md - Coding Agent Guidelines

## Project Overview

This is a Moon monorepo template containing:
- `@python/` - Python project template (uv, pytest, ruff, mypy)
- `@golang/` - Go project template (go modules, gorm)
- `@proto/` - Buf protobuf project template (proto code generation)

## Build/Lint/Test Commands

### Python Projects

```bash
# Install dependencies
uv sync --all-groups          # Full dev environment
uv sync                       # Production only

# Run tests
uv run pytest tests                        # All tests
uv run pytest tests -m "stone"             # Stone tests only (core functionality)
uv run pytest tests -m "stable"            # Stable tests only
uv run pytest tests -k test_name           # Single test by name
uv run pytest tests/path/to/test.py::test_function  # Single test function

# Watch mode (auto-rerun on changes)
uv run ptw . --no-cov -m '(stone or stable or alpha or doing) and (not slow)'

# Linting
uv run ruff check .              # Lint (auto-fix: --fix)
uv run ruff format .             # Format code
uv run pre-commit run --all-files  # All pre-commit hooks

# Type checking
uv run mypy ./src

# Build
uv build

# Clean
rm -rf build dist src/*.egg-info && find src -name "*.c" -o -name "*.so" | xargs rm -f
```

### Go Projects

```bash
# Run tests
go test -v ./...           # All tests verbose
go test -v ./pkg/...       # Specific package
go test -run TestName ./... # Single test

# Race detection
go test -race ./...

# Coverage
go test -cover ./...
go test -coverprofile=coverage.out ./... && go tool cover -html=coverage.out

# Lint/Format
go fmt ./...

# Dependencies
go mod tidy

# Build
go build -v ./...
go build -ldflags='-w -s' -v ./...  # Release build
```

### Proto Projects

```bash
# Generate protobuf code
buf generate -o ../

# Using moonx (if available)
moonx proto:generate
```

### Moon Task Runner

```bash
moon run <project>:<task>   # Run specific task
moon run python:test        # Run python tests
moon run python:lint        # Run python linting
moon run python:check       # Run lint + type-check
moon run golang:test
moon run golang:build
moon run proto:generate
```

## Code Style Guidelines

### Python

**Imports:**
- Use absolute imports: `from package.module import Class`
- Group imports: stdlib → third-party → local
- Use `ruff` for automatic import sorting

**Formatting:**
- Line length: 88 characters (Black/ruff default)
- Indent: 4 spaces
- Quotes: Double quotes for strings
- Use `ruff format` for consistency

**Types:**
- Python 3.12+ type hints required
- Use `mypy` for type checking
- `no_implicit_optional = true`
- `show_error_codes = true`

**Naming:**
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

**Error Handling:**
- Use specific exceptions over bare `except:`
- Use `loguru` for logging
- Avoid bare `try/except` blocks

**Testing:**
- Use `pytest` with markers: `@pytest.mark.fast`, `@pytest.mark.smoke`
- Marker hierarchy: `stone` > `stable` > `alpha` > `beta`
- Fixtures in `conftest.py`
- Use `pytest-mock` for mocking

### Go

**Formatting:**
- Always run `go fmt ./...` before commit
- Follow standard Go conventions

**Imports:**
- Standard library first
- External packages second
- Local packages third

**Naming:**
- Variables/functions: `camelCase` or `PascalCase` (exported)
- Types/Structs: `PascalCase`
- Interfaces: `-er` suffix (e.g., `Reader`)

**Error Handling:**
- Return errors as values
- Check errors immediately
- Use `errors.New()` or `fmt.Errorf()`

**Testing:**
- Use `testify` for assertions
- Table-driven tests preferred
- Run with `-race` flag for race detection

### Proto (Buf)

**Linting:**
- Follow `STANDARD` lint rules
- Breaking changes checked against `FILE` level

**Structure:**
- `.proto` files in `proto/` directory
- Generated code in `proto/gen/go/`

## Pre-commit Hooks

Python projects use pre-commit with:
- trailing-whitespace
- end-of-file-fixer
- check-yaml/json/toml
- ruff-check (with --fix)
- ruff-format
- detect-secrets

Run manually: `uv run pre-commit run --all-files`

## Test Markers (Python)

| Marker   | Description |
|----------|-------------|
| `stone`  | Core functionality, minimal test suite |
| `stable` | Important, stable APIs |
| `alpha`  | Important but may change |
| `beta`   | In development, may change |
| `fast`   | Fast tests, no IO |
| `slow`   | Resource intensive |
| `smoke`  | Basic functionality checks |

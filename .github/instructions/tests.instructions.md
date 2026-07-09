---
description: "Use when adding, editing, or running tests and linters in this project. Covers Ruff, Pylint, yamllint, actionlint, and the invoke test task conventions."
applyTo: "tasks/tests.py"
---
# Tests Instructions

## Test Tooling
| Tool | Covers | Run With |
|------|--------|----------|
| Ruff | Python style & lint | `uv run --no-sync invoke tests.rufflint` |
| Pylint | Deeper Python static analysis (must score 10.00/10) | `uv run --no-sync invoke tests.pylint` |
| yamllint | YAML files | `uv run --no-sync invoke tests.yamllint` |
| actionlint | GitHub Actions workflow files | `uv run --no-sync invoke tests.actionlint` |

## Running Tests
```sh
uv run --no-sync invoke test          # All: ruff + pylint + yamllint + actionlint
uv run --no-sync invoke tests.rufflint
uv run --no-sync invoke tests.pylint
uv run --no-sync invoke tests.yamllint
uv run --no-sync invoke tests.actionlint
uv run --no-sync invoke fix           # Auto-correct: ruff check --fix + ruff format
```

Always include `--no-sync` — a bare `uv run` silently re-resolves the environment and can pull in a
newer dependency version before the command runs, without the change going through review.

## File Structure
```
tasks/
  tests.py   # tests.actionlint, tests.pylint, tests.rufflint, tests.yamllint
  ruff.py    # ruff.fix, ruff.format
  combos.py  # test (alias for all tests.*), fix (alias for ruff.fix + ruff.format)
```

## Adding a New Test Task
1. Add a `@task` function to `tasks/tests.py`
2. Name it after the tool it runs (e.g. `def mypy(context):`)
3. Add a call to it inside `combos.test`
4. Config for the tool lives in `pyproject.toml` (ruff/pylint) or its own dotfile (`.yamllint`, `actionlint.yml` if needed)

## Pylint
- Config lives in `pyproject.toml` under `[tool.pylint.*]`
- `fail-under = 10` in `[tool.pylint.main]` — CI fails below a perfect score
- Run with `--rcfile=pyproject.toml` explicitly (see `tasks/tests.py`)

## Ruff
- Config lives in `pyproject.toml` under `[tool.ruff]`
- `rufflint` task = `ruff check .`; `ruff.fix` task = `ruff check . --fix`; `ruff.format` = `ruff format .`

## yamllint
- Config lives in `.yamllint` at project root

## Addons
`addons/**` is excluded from Ruff (`extend-exclude`) and Pylint (`ignore-paths`) in `pyproject.toml`
— those files are only valid once copied into a consuming repo's root, so linting them here would
fail on imports/paths that don't resolve from this repo's root. `yamllint`/`actionlint` still scan
`addons/**` YAML/workflow files (nothing to exclude by root-relative path assumptions there yet).
See "Addons" in `README.md`.

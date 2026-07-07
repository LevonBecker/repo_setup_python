---
description: "Use when working on overall project structure, conventions, dependencies, or setup. Covers project layout, pyproject.toml, invoke.yml, and general organization."
---
# Project Instructions

## Overview
Python-based project using [Invoke](https://www.pyinvoke.org/) for task automation and [uv](https://docs.astral.sh/uv/) for dependency/environment management. Targets Python `>=3.14`.

## Project Structure
```
pyproject.toml    # Dependencies, ruff/pylint config
invoke.yml        # Invoke config (auto_dash_names: false)
setup.sh          # Shell-based setup script (uv venv + uv sync)
properties.yml    # Project configuration (repo path, remote)
modules/
  common/         # cli.py, properties.py, utils.py — shared helpers
  repo/           # pull.py, push.py, log.py, squash.py, rebase.py — git workflow modules
tasks/
  __init__.py     # Wires the invoke Collection (repo, ruff, tests, fix, test)
  repo.py         # repo.pull, repo.push, repo.log, repo.squash, repo.rebase
  ruff.py         # ruff.fix, ruff.format
  tests.py        # tests.actionlint, tests.pylint, tests.rufflint, tests.yamllint
  combos.py       # Top-level aliases: fix, test
.github/
  instructions/   # Copilot instruction files
  prompts/        # Copilot prompt files (/push, /pull, /squash, /rebase, /fix, /test)
  workflows/      # tests.yml (reusable), feature_branches.yml, protected_branches.yml
.vscode/
  extensions.json # Recommended VS Code extensions
  settings.json   # Ruff formatter + Python interpreter settings
```

## Key Conventions
- `tasks/__init__.py` builds the root `Collection` — all task modules are wired explicitly (no auto-glob loading, unlike the Rake-based sibling project)
- `modules/` are plain importable Python packages (`modules.common`, `modules.repo`) — imported directly by `tasks/*.py`
- Every `modules/repo/*.py` file exposes a `main()` entry point, runnable standalone via `python -m modules.repo.<name>`
- `invoke.yml` sets `auto_dash_names: false` so task names keep underscores (e.g. `repo.pull`, not `repo.pull-dash`)

## Dependencies (pyproject.toml)
- `invoke` — task runner
- `ruff` — fast Python linter/formatter
- `pylint` — deep static analysis (10/10 required to pass `invoke test`)
- `yamllint` — YAML linting
- `actionlint-py` — GitHub Actions workflow linting (pip-installed, no Homebrew required)
- `pyyaml` — reads `properties.yml`

## Running Tasks
```sh
uv run invoke          # List all tasks (or: uv run invoke -l)
uv run invoke test     # ruff + pylint + yamllint + actionlint
uv run invoke fix      # Ruff autocorrect + format
uv run invoke repo.pull   # Pull from git remote (stash → pull --rebase → restore)
uv run invoke repo.push   # Push to git remote (fix → test → commit → push)
uv run invoke repo.log    # Save a session log to logs/
uv run invoke repo.squash # Anchored squash all commits to root + optional force push
uv run invoke repo.rebase # Rebase onto remote default branch (optionally squash first)
```

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
properties.yml    # Project configuration (repo path/remote, template path/remote)
modules/
  common/         # cli.py, properties.py, utils.py — shared helpers
  repo/           # pull.py, push.py, log.py, squash.py, rebase.py, pr.py — git/PR workflow modules
  claude/         # sync.py — syncs .claude/commands/ from .github/prompts/
  template/       # pull.py, push.py, resolve.py, route.py, scope.py — sync shared tooling with the parent template repo for /template
  versioning/     # libs.py, python.py, workflows.py, upgrade.py, project.py — check pyproject.toml deps & workflow action refs vs. latest releases, bump the repo's VERSION file
tasks/
  __init__.py     # Wires the invoke Collection (claude, repo, ruff, template, tests, uv, versioning, fix, test)
  claude.py       # claude.sync
  repo.py         # repo.pull, repo.push, repo.log, repo.squash, repo.rebase, repo.pr_diff, repo.pr_notes_save, repo.pr_create
  ruff.py         # ruff.fix, ruff.format
  template.py     # template.pull
  tests.py        # tests.actionlint, tests.pylint, tests.rufflint, tests.yamllint
  uv.py           # uv.upgrade
  versioning.py   # ver.libs, ver.workflows, ver.all, ver.project_bump_build, ver.project_bump_release
  combos.py       # Top-level aliases: fix, test
.github/
  instructions/   # Copilot instruction files
  prompts/        # Copilot prompt files (/push, /pull, /squash, /rebase, /fix, /test, /pr-notes, /pr, /punch-it-chewy, /template, /versioning) — source of truth for slash commands
  workflows/      # tests.yml (reusable), feature_branches.yml, protected_branches.yml
.claude/
  commands/       # Claude Code slash commands, kept in sync with .github/prompts/ via `uv run --no-sync invoke claude.sync`
.vscode/
  extensions.json # Recommended VS Code extensions
  settings.json   # Ruff formatter + Python interpreter settings
addons/
  shopfiy_dawn_theme/ # Shopify Dawn theme addon — see "Addons" in README.md before using
```

## Key Conventions
- `tasks/__init__.py` builds the root `Collection` — all task modules are wired explicitly (no auto-glob loading, unlike the Rake-based sibling project)
- `modules/` are plain importable Python packages (`modules.common`, `modules.repo`, `modules.claude`) — imported directly by `tasks/*.py`
- Every `modules/repo/*.py` file exposes a `main()` entry point, runnable standalone via `python -m modules.repo.<name>`
- `invoke.yml` sets `auto_dash_names: false` so task names keep underscores (e.g. `repo.pull`, not `repo.pull-dash`)
- `.github/prompts/` is the source of truth for slash commands; `.claude/commands/` mirrors it — run `invoke claude.sync` to add new commands, `--force` to overwrite hand-crafted ones
- Always run `uv run --no-sync ...`, never bare `uv run ...` — without `--no-sync`, `uv run` re-resolves and may silently upgrade a dependency before the command runs. Any dependency change must go through an explicit `uv sync`/`uv lock` step that the user can review, not an implicit one buried inside a task run
- `addons/<name>/` mirrors the root layout but is not usable from this repo's root — its files must
  be copied into a consuming repo's actual root (root-relative imports, `applyTo` globs, and task
  wiring all assume that). Excluded from `ruff`/`pylint` via `pyproject.toml`
  (`extend-exclude`/`ignore-paths`) for the same reason — see "Addons" in `README.md`

## Dependencies (pyproject.toml)
- `invoke` — task runner
- `ruff` — fast Python linter/formatter
- `pylint` — deep static analysis (10/10 required to pass `invoke test`)
- `yamllint` — YAML linting
- `actionlint-py` — GitHub Actions workflow linting (pip-installed, no Homebrew required)
- `pyyaml` — reads `properties.yml`

## External Tools
- `gh` (GitHub CLI) — required for `repo.pr_create` / `/pr` / `/punch-it-chewy` (not a pip package; install via Homebrew)

## Running Tasks
```sh
uv run --no-sync invoke          # List all tasks (or: uv run --no-sync invoke -l)
uv run --no-sync invoke test     # ruff + pylint + yamllint + actionlint
uv run --no-sync invoke fix      # Ruff autocorrect + format
uv run --no-sync invoke repo.pull   # Pull from git remote (stash → pull --rebase → restore)
uv run --no-sync invoke repo.push   # Push to git remote (fix → test → commit → push)
uv run --no-sync invoke repo.log    # Save a session log to logs/
uv run --no-sync invoke repo.squash # Anchored squash all commits to root + optional force push
uv run --no-sync invoke repo.rebase # Rebase onto remote default branch (optionally squash first)
uv run --no-sync invoke repo.pr_diff       # Print current branch's commit log/diff vs. its base branch
uv run --no-sync invoke repo.pr_notes_save # Save PR notes to tmp/pull_requests/ (--content=...)
uv run --no-sync invoke repo.pr_create     # Open a GitHub PR via gh (--title=... --content=...)
uv run --no-sync invoke claude.sync # Sync .claude/commands/ from .github/prompts/ (additive; --force to overwrite)
uv run --no-sync invoke template.pull           # Resolve the parent template repo's local path for /template
uv run --no-sync invoke template.push_diff      # Diff this repo's scoped tooling against the parent template repo
uv run --no-sync invoke template.push_apply     # Copy approved files/deletions to a new branch upstream and push it
uv run --no-sync invoke template.push_create_pr # Open a PR for that branch against the parent template repo
uv run --no-sync invoke ver.libs    # Check pyproject.toml deps vs. latest releases, update version locks
uv run --no-sync invoke ver.all     # Run every version check (libs, workflows)
uv run --no-sync invoke ver.project_bump_build   # Dev deploy: new minor's first VERSION build, or next build number
uv run --no-sync invoke ver.project_bump_release # Release: drop the VERSION build suffix
uv run --no-sync invoke uv.upgrade  # Install the versions currently locked in pyproject.toml (uv sync)
```

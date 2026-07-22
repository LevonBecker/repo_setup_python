# Repo Setup (Python)
[![Tests](https://github.com/LevonBecker/template_python/actions/workflows/tests.yml/badge.svg)](https://github.com/LevonBecker/template_python/actions/workflows/tests.yml)

Skeleton setup for a repository that uses Python invoke tasks, reusable modules, uv for
environment/dependency management, and AI Copilot prompts and instructions. Drop this into any
project to get a consistent git workflow, linting, and session logging out of the box.

## Setup
```bash
./setup.sh
```

Creates a `.venv` with `uv` and installs dependencies. Update `properties.yml` with the local repo
path before running tasks.

## Project Structure
```
pyproject.toml        # Dependencies (Python >=3.14), ruff/pylint config
invoke.yml             # Invoke config (auto_dash_names: false)
setup.sh               # Initial environment setup (uv venv + uv sync)
properties.yml         # Project configuration (repo path/remote, template path/remote)
modules/
  common/               # cli.py, properties.py, utils.py — shared helpers
  repo/                 # pull.py, push.py, log.py, squash.py, rebase.py, pr.py — git/PR workflow modules
  claude/               # sync.py — syncs .claude/commands/ from .github/prompts/
  template/             # pull.py, push.py, resolve.py, route.py, scope.py — sync shared tooling with the parent template repo for /template
  versioning/           # libs.py, python.py, workflows.py, upgrade.py, project.py — check pyproject.toml deps & workflow action refs vs. latest releases, bump the repo's VERSION file
tasks/
  __init__.py           # Wires the invoke Collection (claude, repo, ruff, template, tests, uv, versioning, fix, test)
  claude.py             # claude.sync
  repo.py               # repo.pull, repo.push, repo.log, repo.squash, repo.rebase, repo.pr_diff, repo.pr_notes_save, repo.pr_create
  ruff.py               # ruff.fix, ruff.format
  template.py           # template.pull
  tests.py              # tests.actionlint, tests.pylint, tests.rufflint, tests.yamllint
  uv.py                 # uv.upgrade
  versioning.py         # ver.libs, ver.workflows, ver.all, ver.project_bump_build, ver.project_bump_release
  combos.py             # Top-level aliases: fix, test
.github/
  instructions/         # Copilot instructions per concern
  prompts/              # /push, /pull, /squash, /rebase, /fix, /test, /setup, /pr-notes, /pr, /punch-it-chewy, /template, /versioning — source of truth
  workflows/
    tests.yml            # Reusable CI: ruff + pylint + yamllint + actionlint
    feature_branches.yml # Runs tests.yml on pull_request
    protected_branches.yml # Runs tests.yml on push to main
.claude/
  commands/              # Claude Code slash commands, mirrored from .github/prompts/
.vscode/
  extensions.json       # Recommended VS Code extensions
  settings.json         # Ruff formatter + Python interpreter settings
addons/
  shopfiy_dawn_theme/    # Shopify Dawn theme addon — see Addons below before using
```

## Invoke Tasks
```sh
uv run --no-sync invoke             # List all available tasks
uv run --no-sync invoke test        # Ruff + Pylint + yamllint + actionlint
uv run --no-sync invoke fix          # Ruff autocorrect + format
uv run --no-sync invoke repo.pull    # Pull from git remote (stash → pull --rebase → restore)
uv run --no-sync invoke repo.push    # Push to git remote (fix → test → commit → push)
uv run --no-sync invoke repo.log     # Save a session log to logs/
uv run --no-sync invoke repo.squash  # Anchored squash all commits to root + optional force push
uv run --no-sync invoke repo.rebase  # Rebase onto remote default branch (optionally squash first)
uv run --no-sync invoke repo.pr_diff       # Print current branch's commit log/diff vs. its base branch
uv run --no-sync invoke repo.pr_notes_save # Save PR notes to tmp/pull_requests/ (--content=...)
uv run --no-sync invoke repo.pr_create     # Open a GitHub PR via gh (--title=... --content=...)
uv run --no-sync invoke claude.sync  # Sync .claude/commands/ from .github/prompts/ (additive; --force to overwrite)
uv run --no-sync invoke template.pull            # Resolve the parent template repo's local path for /template
uv run --no-sync invoke template.push_diff       # Diff this repo's scoped tooling against the parent template repo
uv run --no-sync invoke template.push_apply      # Copy approved files/deletions to a new branch upstream and push it
uv run --no-sync invoke template.push_create_pr  # Open a PR for that branch against the parent template repo
uv run --no-sync invoke ver.libs      # Check pyproject.toml deps vs. latest releases, update version locks
uv run --no-sync invoke ver.workflows # Check .github/workflows/ action refs vs. latest majors, update pins
uv run --no-sync invoke ver.all       # Run every version check (libs, workflows)
uv run --no-sync invoke ver.project_bump_build   # Dev deploy: new minor's first VERSION build, or next build number
uv run --no-sync invoke ver.project_bump_release # Release: drop the VERSION build suffix
uv run --no-sync invoke uv.upgrade    # Install the versions currently locked in pyproject.toml (uv sync)
```

## AI Prompts
| Prompt | Command | Description |
|--------|---------|-------------|
| `/push` | `uv run --no-sync invoke repo.push` | Fix, test, commit, and push to git |
| `/pull` | `uv run --no-sync invoke repo.pull` | Stash, pull latest, restore stash |
| `/squash` | `uv run --no-sync invoke repo.squash` | Anchored squash all commits to root |
| `/rebase` | `uv run --no-sync invoke repo.rebase` | Rebase onto remote default branch |
| `/fix` | `uv run --no-sync invoke fix` | Auto-fix Python linting issues |
| `/test` | `uv run --no-sync invoke test` | Run all tests and linters |
| `/setup` | `./setup.sh` | Run initial project setup |
| `/pr-notes` | `uv run --no-sync invoke repo.pr_diff` | Draft PR notes vs. base branch; saves to `tmp/pull_requests/` when run standalone |
| `/pr` | `uv run --no-sync invoke repo.pr_create` | Draft PR notes and open a Pull Request via `gh` (does not push) |
| `/punch-it-chewy` | — | Push, then draft notes and open a Pull Request |
| `/template` | `uv run --no-sync python -m modules.template.route` | Pull shared tooling updates from the parent template repo into this project (or push new generic tooling upstream as a PR) |
| `/versioning` | `uv run --no-sync invoke versioning.all` | Check pyproject.toml deps and workflow action refs vs. latest releases, update locks (does not install or run) |

## Modules
| Module | Purpose |
|--------|---------|
| [`modules/common/`](modules/common/README.md) | CLI helpers, `properties.yml` config reader, output/utility helpers |
| [`modules/repo/`](modules/repo/README.md) | Git workflow and session logging |
| [`modules/claude/`](modules/claude/README.md) | Sync `.claude/commands/` from `.github/prompts/` source of truth |
| [`modules/template/`](modules/template/README.md) | Sync shared, generic tooling with the parent template repo for `/template` |
| [`modules/versioning/`](modules/versioning/README.md) | Check `pyproject.toml` deps and workflow action refs vs. latest releases, update locks; bump the repo's `VERSION` file for deploys/releases |

See [modules/README.md](modules/README.md) for full details.

## Addons
Optional, project-specific extensions live under `addons/<name>/` and mirror the root layout
(`modules/`, `tasks/`, `.github/`, `.claude/`). They are **not** usable from inside
`template_python` — they only work once their files are copied into the consuming repo's
actual root, merged with what's already there, because they:
- Import via root-relative paths (e.g. `from modules.dawn import list`)
- Have `applyTo` instruction globs written for a root-level path (e.g. `modules/dawn/**`)
- Need their `tasks/*.py` task module wired into that repo's `tasks/__init__.py` `Collection` by
  hand — nothing here auto-discovers them

They're excluded from `ruff`/`pylint` here (`pyproject.toml` `extend-exclude`/`ignore-paths`) since
they aren't meant to lint clean from this repo's root.

| Addon | Adds | Move these files to the consuming repo's root |
|-------|------|------------------------------------------------|
| [`addons/shopfiy_dawn_theme/`](addons/shopfiy_dawn_theme/) | `dawn.list` / `dawn.upgrade` invoke tasks for tracking and staging upstream Shopify/dawn theme upgrades | `modules/dawn/` (`__init__.py`, `list.py`, `upgrade.py`, `README.md`), `tasks/dawn.py`, `.github/workflows/{deploy,promote,release,tests,upgrade}.yml`, `.github/instructions/dawn.instructions.md`, `.github/prompts/dawn.prompt.md`, `.claude/commands/dawn.md` |

## CI
GitHub Actions runs Ruff, Pylint, yamllint, and actionlint on every push and pull request via
`.github/workflows/tests.yml` (invoked by `feature_branches.yml` and `protected_branches.yml`).


# Repo Setup (Python)
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
properties.yml         # Project configuration (repo path, remote)
modules/
  common/               # cli.py, properties.py, utils.py — shared helpers
  repo/                 # pull.py, push.py, log.py, squash.py, rebase.py — git workflow modules
tasks/
  __init__.py           # Wires the invoke Collection (repo, ruff, tests, fix, test)
  repo.py               # repo.pull, repo.push, repo.log, repo.squash, repo.rebase
  ruff.py               # ruff.fix, ruff.format
  tests.py              # tests.actionlint, tests.pylint, tests.rufflint, tests.yamllint
  combos.py             # Top-level aliases: fix, test
.github/
  instructions/         # Copilot instructions per concern
  prompts/              # /push, /pull, /squash, /rebase, /fix, /test, /setup prompts
  workflows/
    tests.yml            # Reusable CI: ruff + pylint + yamllint + actionlint
    feature_branches.yml # Runs tests.yml on pull_request
    protected_branches.yml # Runs tests.yml on push to main
.vscode/
  extensions.json       # Recommended VS Code extensions
  settings.json         # Ruff formatter + Python interpreter settings
```

## Invoke Tasks
```sh
uv run invoke             # List all available tasks
uv run invoke test        # Ruff + Pylint + yamllint + actionlint
uv run invoke fix          # Ruff autocorrect + format
uv run invoke repo.pull    # Pull from git remote (stash → pull --rebase → restore)
uv run invoke repo.push    # Push to git remote (fix → test → commit → push)
uv run invoke repo.log     # Save a session log to logs/
uv run invoke repo.squash  # Anchored squash all commits to root + optional force push
uv run invoke repo.rebase  # Rebase onto remote default branch (optionally squash first)
```

## AI Prompts
| Prompt | Command | Description |
|--------|---------|-------------|
| `/push` | `uv run invoke repo.push` | Fix, test, commit, and push to git |
| `/pull` | `uv run invoke repo.pull` | Stash, pull latest, restore stash |
| `/squash` | `uv run invoke repo.squash` | Anchored squash all commits to root |
| `/rebase` | `uv run invoke repo.rebase` | Rebase onto remote default branch |
| `/fix` | `uv run invoke fix` | Auto-fix Python linting issues |
| `/test` | `uv run invoke test` | Run all tests and linters |
| `/setup` | `./setup.sh` | Run initial project setup |

## Modules
| Module | Purpose |
|--------|---------|
| [`modules/common/`](modules/common/README.md) | CLI helpers, `properties.yml` config reader, output/utility helpers |
| [`modules/repo/`](modules/repo/README.md) | Git workflow and session logging |

See [modules/README.md](modules/README.md) for full details.

## CI
GitHub Actions runs Ruff, Pylint, yamllint, and actionlint on every push and pull request via
`.github/workflows/tests.yml` (invoked by `feature_branches.yml` and `protected_branches.yml`).


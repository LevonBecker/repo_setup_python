---
description: "Use when creating or editing shared Python modules used by invoke tasks or prompts. Covers modules/ structure, module patterns, and helper conventions."
applyTo: "modules/**/*.py"
---
# Modules Instructions

## Purpose
Modules provide reusable Python logic consumed by invoke tasks, prompts, and scripts. They contain no task definitions — only functions.

## Locations
| Path | Purpose |
|------|---------|
| `modules/common/` | Helpers tightly coupled to invoke tasks (`cli`, `properties`, `utils`) |
| `modules/repo/` | Git/PR workflow logic (pull, push, log, squash, rebase, pr) |
| `modules/claude/` | Syncs `.claude/commands/` from `.github/prompts/` source of truth |
| `modules/skeleton/` | Locates the shared skeleton repo (repo_setup_python) for `/sync-setup` |
| `modules/versioning/` | Checks `pyproject.toml` deps and workflow action refs against latest releases, updates locks |

## Module Conventions
- One concern per file; filename matches the concern in snake_case
- Use module-level functions, not classes, unless state genuinely requires it
- `modules/repo/*.py` files each expose a `main()` entry point; a file may expose additional public
  functions (not prefixed `_`) if it backs more than one invoke task — e.g. `pr.py` exposes `main()`
  (diff context), `save_notes()`, and `create_pr()` for its three `repo.pr_*` tasks
- Private helpers are prefixed with `_` (e.g. `_stash_if_needed`)

## Method Patterns
```python
"""One-line module docstring."""

import subprocess
from pathlib import Path

from ..common import cli as click
from ..common.utils import error, success


def _helper(repo_path: Path) -> bool:
    """Docstring explaining behavior."""
    result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_path, capture_output=True, text=True, check=True)
    return bool(result.stdout.strip())


def main() -> None:
    """Entry point."""
    # implementation
```

## Common Helper Modules (`modules/common/`)
| Module | Use When |
|--------|----------|
| `cli.py` | Click-like `echo`, `prompt`, `confirm`, `is_tty`, `command`/`option` decorators |
| `properties.py` | Read `properties.yml` — `get_repo_local()`, `get_repo_remote()`, `get_skeleton_local()`, `get_skeleton_remote()` |
| `utils.py` | `success()`, `error()`, `warning()`, `info()`, `create_slug()` |

## Guidelines
- Use `subprocess.run([...], cwd=repo_path, check=...)` for shell execution — never `shell=True` or string interpolation into shell commands
- Use `modules.common.utils` for all console output; never bare `print()` in `modules/` code
- Keep functions focused and single-purpose; extract private helpers instead of writing long functions
- Add type hints to all function signatures

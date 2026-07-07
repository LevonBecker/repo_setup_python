# Repo Modules

Git workflow logic invoked by the `repo.*` invoke tasks (see [tasks/repo.py](../../tasks/repo.py)).

| Module | Purpose |
|--------|---------|
| `pull.py` | Pull from git remote (stash → `pull --rebase` → restore stash) |
| `push.py` | Push to git remote (`invoke fix` → `invoke test` → commit → push) |
| `log.py` | Save a timestamped session log markdown file to `logs/` |
| `squash.py` | Anchored squash of all commits to root, with optional force push |
| `rebase.py` | Rebase onto the remote default branch, with optional squash-first and interactive conflict resolution |
| `pr.py` | Detect the PR base branch, print commit/diff context, save PR notes to `tmp/pull_requests/`, and open the PR via `gh` |

## Conventions

- Every module exposes a module-level `main()` entry point (also runnable via `python -m modules.repo.<name>`) — `pr.py` additionally exposes `save_notes()` and `create_pr()` for its two other invoke tasks
- Shell out to `git` via `subprocess.run(..., cwd=repo_path)` — never `shell=True`
- Use `modules.common.cli` for output/prompts and `modules.common.utils` for success/error/warning messages
- Resolve the repository path via `modules.common.properties.get_repo_local()`

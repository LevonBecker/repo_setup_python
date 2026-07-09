# Modules

Reusable Python modules imported by `tasks/*.py` invoke tasks. All functions are module-level —
no classes required except small helper validators in `common/cli.py`.

## Structure

```
modules/
  common/       # cli, properties, utils helpers
  repo/         # pull, push, log, squash, rebase (git workflow)
  claude/       # sync .claude/commands/ from .github/prompts/
  skeleton/     # locate the shared skeleton repo for /sync-setup
  versioning/   # check pyproject.toml deps and workflow action refs vs. latest releases, update locks
```

## Submodules

| Directory | Purpose |
|-----------|---------|
| [`common/`](common/README.md) | CLI helpers, `properties.yml` config reader, output/utility helpers |
| [`repo/`](repo/README.md) | Git workflow, session logging, squash, and rebase |
| [`claude/`](claude/README.md) | Sync `.claude/commands/` from `.github/prompts/` source of truth |
| [`skeleton/`](skeleton/README.md) | Locate the shared skeleton repo for `/sync-setup` |
| [`versioning/`](versioning/README.md) | Check `pyproject.toml` deps and workflow action refs vs. latest releases, update locks |

## Conventions

- One module per file; filename matches the concern in snake_case
- Each `modules/repo/*.py` file exposes a `main()` entry point
- Shell out via `subprocess.run(..., cwd=repo_path)` — never `shell=True`
- Use `modules.common.utils` (`success`/`error`/`warning`/`info`) for all console output
- Resolve repo config via `modules.common.properties`

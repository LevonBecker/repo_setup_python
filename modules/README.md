# Modules

Reusable Python modules imported by `tasks/*.py` invoke tasks. All functions are module-level —
no classes required except small helper validators in `common/cli.py`.

## Structure

```
modules/
  common/       # cli, properties, utils helpers
  repo/         # pull, push, log, squash, rebase (git workflow)
  template/     # sync shared, generic tooling with the parent template repo for /template
  versioning/   # check pyproject.toml deps and workflow action refs vs. latest releases, update locks;
                # bump the repo's VERSION file for deploys/releases
```

## Submodules

| Directory | Purpose |
|-----------|---------|
| [`common/`](common/README.md) | CLI helpers, `properties.yml` config reader, output/utility helpers |
| [`repo/`](repo/README.md) | Git workflow, session logging, squash, and rebase |
| [`template/`](template/README.md) | Sync shared, generic tooling with the parent template repo for `/template` |
| [`versioning/`](versioning/README.md) | Check `pyproject.toml` deps and workflow action refs vs. latest releases, update locks; bump the repo's `VERSION` file for deploys/releases |

## Conventions

- One module per file; filename matches the concern in snake_case
- Each `modules/repo/*.py` file exposes a `main()` entry point
- Shell out via `subprocess.run(..., cwd=repo_path)` — never `shell=True`
- Use `modules.common.utils` (`success`/`error`/`warning`/`info`) for all console output
- Resolve repo config via `modules.common.properties`

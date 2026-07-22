---
description: "Use when bumping the repo's VERSION file. Covers the ver.project_bump_* invoke tasks and the Major.Minor.Patch-Build scheme."
applyTo: "modules/versioning/project.py"
---
# Version Instructions

## Purpose
The root `VERSION` file tracks this repo's release version — what gets tagged as a GitHub
Release, if this repo ships one. This is separate from `pyproject.toml`'s own `[project]
version` field (Python package metadata, unrelated) and from `modules/versioning/libs.py` and
`workflows.py`'s `ver.libs`/`ver.workflows` checks (dependency locks and GitHub Action ref pins
against external sources — a different concern entirely, despite living in the same module
directory as `project.py`).

Scheme: `Major.Minor.Patch[-Build]`
- No build suffix (e.g. `1.0.0`) — a released version.
- A build suffix (e.g. `1.1.0-003`) — build `003` toward `1.1.0`, in progress but not yet released.

Two operations, one per `ver.project_bump_*` invoke task:
- `ver.project_bump_build` — no build suffix yet -> bump the minor and start build `001`
  (`1.0.0` -> `1.1.0-001`); build suffix present -> increment the build number only
  (`1.1.0-001` -> `1.1.0-002`)
- `ver.project_bump_release` — drop the build suffix (`1.1.0-003` -> `1.1.0`)

See `modules/versioning/README.md` for full behavior/data-flow details.

## Usage
```sh
uv run --no-sync invoke ver.project_bump_build      # dev build: new minor's first build, or next build number
uv run --no-sync invoke ver.project_bump_release    # release: drop the build suffix
```
Both only rewrite `VERSION` — they don't commit, branch, or push, tag a release, or trigger any
workflow. This repo has no `deploy.yml`/`release.yml` of its own; a project that adds one should
wire it to call these tasks (see `template_shopify`'s `version.instructions.md` for a worked
example of a deploy/release pipeline built on top of the same `project.py` module).

## Module Conventions
- Same conventions as `modules.instructions.md` generally, except this file exposes
  `bump_build()`/`bump_release()` (public, no leading `_`) instead of a single `main()` — both are
  equally valid entry points, one per `ver.project_bump_*` invoke task
- Resolve the repo path via `modules.common.properties.get_repo_root()`, not `get_repo_local()`
  — these tasks may run in CI, where `get_repo_local()`'s hardcoded local-machine path doesn't exist
- `subprocess.run([...], cwd=repo_path)` never `shell=True`, output via `modules.common.utils`

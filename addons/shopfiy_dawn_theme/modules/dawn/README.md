# Dawn Module

Lists upstream Shopify/dawn version tags, and stages a Dawn upgrade onto a review branch for
manual conflict resolution. Does not install anything, and never auto-resolves conflicts or
opens a PR on its own.

## Usage

```sh
uv run --no-sync invoke dawn.list                    # list upstream Shopify/dawn tags, latest highlighted
uv run --no-sync invoke dawn.upgrade                    # stage the latest upstream tag for review
uv run --no-sync invoke dawn.upgrade --version=v15.5.0  # stage a specific tag for review
uv run --no-sync invoke dawn.upgrade --version=latest   # same as omitting --version
```

## `list.py` — `dawn.list`

1. Lists every semver tag published on upstream `Shopify/dawn` via `git ls-remote --tags --refs`
   (no clone/auth needed), sorted numerically.
2. Resolves the tag the local `dawn_vanilla` branch currently points to (`git describe --tags`)
   and marks it inline, alongside the latest upstream tag.
3. Prints the exact `version` value (e.g. `v15.5.0`) to pass to the **Upgrade** GitHub Actions
   workflow (`.github/workflows/upgrade.yml`) to sync `dawn_vanilla` to the latest release.

This is read-only — it doesn't fetch, merge, or push anything. It exists purely to answer "what's
the latest Dawn version, and what am I currently on?" before running the Upgrade workflow.

Exposes `fetch_tags()`/`sort_key()` (public, no leading `_`) so `upgrade.py` can reuse the same
tag-fetching logic without duplicating it — see Conventions below.

```
uv run --no-sync invoke dawn.list
  ↓
modules/dawn/list.py
  ↓
git ls-remote --tags Shopify/dawn   +   git describe --tags dawn_vanilla   →   printed list
```

## `upgrade.py` — `dawn.upgrade`

1. Refuses to run if the working tree has uncommitted changes.
2. If `version` is omitted or given as `"latest"`, resolves the latest upstream tag itself (via
   `list.py`'s `fetch_tags()`/`sort_key()`) — used only for the branch name, not to fetch/merge
   anything.
3. Fetches `origin/development` and `origin/dawn_vanilla`.
4. Creates `upgrade/dawn-vanilla-<version>` from `origin/dawn_vanilla`, then rebases it onto
   `origin/development` — **no `-X theirs`/`-X ours`**, so real conflicts stop the rebase rather
   than getting silently resolved.
5. Clean rebase → prints a success message and tells you to run `/push` then `/pr`.
   Conflicts → prints the conflicted file list and points at `fireball.instructions.md` for what
   Fireball customizations must be preserved, plus the `git add` / `git rebase --continue` steps.

This assumes the **Upgrade** GitHub Actions workflow has already synced `dawn_vanilla` to the
target version — it only handles bringing that content onto a `development`-based review branch.
See `dawn.instructions.md`'s "Why the Rebase-and-PR Step Isn't Automated in CI" section for why
this is a local/AI-assisted step rather than a second CI job.

```
uv run --no-sync invoke dawn.upgrade [--version=vX.Y.Z]
  ↓
modules/dawn/upgrade.py
  ↓
git checkout -b upgrade/dawn-vanilla-<version> origin/dawn_vanilla
git rebase origin/development   →   clean, or stops with conflicts to resolve by hand
```

## Conventions

- Every module exposes a module-level `main()` entry point
- Neither file takes `@click.command()`-style options — both use plain keyword arguments
  (`dawn.upgrade`'s optional `version`), matching `modules/shopify/upgrade.py`'s pattern for
  simple-argument modules
- `list.py`'s `fetch_tags()`/`sort_key()` are deliberately public (no leading `_`) since
  `upgrade.py` imports them directly — everything else in both files is a private (`_`-prefixed)
  helper
- Shell out via `subprocess.run(..., cwd=repo_path)` — never `shell=True`
- Use `modules.common.utils` (`success`/`error`/`warning`/`info`) for all console output

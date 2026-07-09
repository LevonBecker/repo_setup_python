---
description: "Use when listing upstream Shopify/dawn version tags or upgrading Dawn from upstream. Covers the dawn.* invoke tasks and their modules."
applyTo: "modules/dawn/**"
---
# Dawn Instructions

## Purpose
Two actions, both scoped to upstream `Shopify/dawn`:
- `dawn.list` — lists every tag published on upstream `Shopify/dawn`, sorted, with the latest
  highlighted and compared against what `dawn_vanilla` is currently synced to. Read-only.
- `dawn.upgrade` — creates a feature branch off `dawn_vanilla`, rebased onto `development`, for
  manual conflict resolution. Not read-only — creates a local branch and rebases.

See `modules/dawn/README.md` for full behavior/data-flow details on each.

## Usage
```sh
uv run --no-sync invoke dawn.list                       # list upstream Shopify/dawn tags, latest highlighted
uv run --no-sync invoke dawn.upgrade                    # stage the latest upstream tag for review
uv run --no-sync invoke dawn.upgrade --version=v15.5.0  # stage a specific tag for review
uv run --no-sync invoke dawn.upgrade --version=latest   # same as omitting --version
```
`/dawn [list | upgrade]` runs the same checks and walks through conflict resolution for `upgrade`.

## Relationship to Other Workflows
- `dawn.list` is purely informational — it tells you what `version` value (e.g. `v15.5.0`)
  to pass to the **Upgrade** GitHub Actions workflow (`.github/workflows/upgrade.yml`)
- `dawn.upgrade` assumes the Upgrade workflow has already synced `dawn_vanilla` to the target
  version; it only handles bringing that onto a `development`-based review branch

## The Full Dawn Upgrade Workflow
Upgrading Dawn is a three-step process split across CI and local/AI-assisted work, deliberately —
see "Why the Rebase-and-PR Step Isn't Automated in CI" below for why step 3 can't be a CI job:

1. **Run `dawn.list`** to see the latest upstream tag and what `dawn_vanilla` is currently on.
2. **Run the "Upgrade" GitHub Actions workflow** (`workflow_dispatch`, `version` input = the tag
   from step 1) — this merges that one pinned upstream tag into `dawn_vanilla` with upstream
   winning any conflict (`dawn_vanilla` is meant to stay a clean mirror, so this part is safe to
   fully automate), and pushes it.
3. **Run `dawn.upgrade`** (or `/dawn upgrade`) locally — creates `upgrade/dawn-vanilla-<version>`
   off the now-updated `dawn_vanilla`, and rebases it onto `development`.
   - Clean rebase → run `/push` then `/pr` to open the PR into `development`.
   - Conflicts → resolve each file by hand (or via `/dawn upgrade`'s AI-assisted walkthrough),
     using `fireball.instructions.md`'s tracking table to know what's ours to preserve, then
     `git rebase --continue`, then `/push` and `/pr`.

## Why the Rebase-and-PR Step Isn't Automated in CI
An earlier version of `.github/workflows/upgrade.yml` had a second job that did step 3 in CI and
opened the PR automatically. It was removed: `config/settings_data.json` and the `templates/*.json`
files conflict on nearly every real upgrade (they're large, frequently-regenerated JSON), and
several `sections/*.liquid`/`*.json` files conflict whenever upstream touches the same regions as
a Fireball customization — which happens often enough to make full automation unrealistic. Worse,
Fireball's customizations are hand-inserted *inside* Dawn's own files, so a CI job blindly picking
a side (`-X theirs`/`-X ours`) risks silently corrupting either the customization or the upstream
update. A human/AI actually reading each conflict is the safer default; `dawn.upgrade` gets you to
that point quickly without pretending the conflict-resolution step can be skipped.

## Why `dawn.list` Fetches Tags Directly Instead of Reusing `shopify.upgrade`
`modules/shopify/upgrade.py` (the local `shopify.upgrade` invoke task) also compares Dawn versions,
but via a full `git fetch upstream --tags`, which pulls every historical Dawn tag into the local
repo — this previously collided with the `.github/workflows/upgrade.yml` CI job's own fetch when a
Fireball release tag happened to share a name with an old upstream Dawn tag (e.g. `v1.0.0`).
`dawn.list` avoids that entirely by using `git ls-remote` against the upstream URL directly — no
local fetch, no tag namespace collision, safe to run anytime.

## Module Conventions
- Same conventions as `modules.instructions.md` generally — `main()` entry point per module,
  `subprocess.run([...], cwd=repo_path)` never `shell=True`, output via `modules.common.utils`
- Neither `list.py` nor `upgrade.py` uses `@click.command()`-style options — both take plain
  keyword arguments and stay undecorated (see `modules/dawn/README.md`'s Conventions section for
  why, and why `list.py`'s `fetch_tags()`/`sort_key()` are public rather than `_`-prefixed)

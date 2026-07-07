# Claude Module

Keeps `.claude/commands/` in sync with `.github/prompts/*.prompt.md`, the source of truth for all
slash commands in this repo (see [prompts.instructions.md](../../.github/instructions/prompts.instructions.md)).

## Usage

```sh
uv run --no-sync invoke claude.sync          # additive only — writes commands that don't exist yet
uv run --no-sync invoke claude.sync --force  # overwrite all, including hand-crafted commands
```

Running `uv run --no-sync python -m modules.claude.sync` directly is always additive-only — `--force` is only
wired up through the `claude.sync` invoke task.

## What It Does

For each `.github/prompts/*.prompt.md` file, writes a matching `.claude/commands/<slug>.md` with
a minimal `description` header. Existing files are left untouched unless `--force` is passed, since
hand-crafted commands often carry extra frontmatter (`allowed-tools`, `argument-hint`, etc.) that a
plain sync would otherwise clobber.

## Architecture

```
uv run --no-sync invoke claude.sync [--force]
  ↓
modules/claude/sync.py
  ↓
.github/prompts/*.prompt.md  →  .claude/commands/*.md
```

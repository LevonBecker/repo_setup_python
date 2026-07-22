# Claude Module

Generates `.claude/commands/*.md` from `.github/prompts/*.prompt.md`, the source of truth for
all slash commands.

## Overview

Claude Code reads slash commands from `.claude/commands/`, using only `description` frontmatter
(the filename is the command name; extra fields are ignored). `sync.py` reads every prompt file
via `modules/common/prompt_commands.py` and writes new command files — by default it never
overwrites a file that already exists, so hand-crafted commands survive re-syncs.

## Usage

```bash
uv run --no-sync python -m modules.claude.sync          # additive only
uv run --no-sync python -m modules.claude.sync --force   # overwrite existing files too
uv run --no-sync invoke claude.sync
uv run --no-sync invoke claude.sync --force
```

Re-run this sync after adding or modifying any `.github/prompts/*.prompt.md` file, then restart
Claude Code to pick up new commands.

## Files

- `sync.py` — reads `.github/prompts/` via `modules/common/prompt_commands.py`, writes
  `.claude/commands/*.md`
- `README.md` — this file

## Architecture

```
uv run --no-sync invoke claude.sync
  ↓
modules/claude/sync.py
  ↓
modules/common/prompt_commands.py (shared .prompt.md parser)
  ↓
.claude/commands/*.md
```

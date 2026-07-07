---
description: Pull updates from git remote. Stashes local changes, pulls with rebase, then restores stash.
subtask: false
agent: general
slash_command: /pull
allowed-tools: Bash(uv run --no-sync *)
---

!`uv run --no-sync invoke repo.pull`

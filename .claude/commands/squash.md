---
description: Anchored squash of all commits to the root commit. Prompts to review the message, confirm squash, and optionally force push.
subtask: false
agent: general
slash_command: /squash
allowed-tools: Bash(uv run --no-sync *)
---

!`uv run --no-sync invoke repo.squash`

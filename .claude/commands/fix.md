---
description: Auto-fix Python linting issues. Use when you want to run ruff check --fix and ruff format.
subtask: false
agent: general
slash_command: /fix
allowed-tools: Bash(uv run --no-sync *)
---

!`uv run --no-sync invoke fix`

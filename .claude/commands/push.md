---
description: Push changes to git remote. Runs invoke fix, invoke test, then commits and pushes.
subtask: false
agent: general
slash_command: /push
allowed-tools: Bash(uv run --no-sync *)
---

!`uv run --no-sync invoke repo.push`

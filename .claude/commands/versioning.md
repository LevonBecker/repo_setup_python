---
description: Check pyproject.toml dependencies and .github/workflows/ action refs against their latest published releases and update version locks. Does not install or run anything.
subtask: false
agent: general
slash_command: /versioning
allowed-tools: Bash(uv run --no-sync *)
---

Run `uv run --no-sync invoke ver.all --dry-run` using the Bash tool. This is read-only and makes
no changes. If it fails, show the full output to the user and ask how they'd like to proceed — do
not retry automatically.

The output has two sections: a `pyproject.toml` dependency table (from `versioning.libs`) and a
`.github/workflows/` action-ref table (from `versioning.workflows`). Either section may say everything is
already up to date — treat that section as done and move on.

## Which section(s) to act on

- Argument is `libs` → only act on the `pyproject.toml` section; ignore the workflows section.
- Argument is `workflows` → only act on the workflows section; ignore the `pyproject.toml` section.
- Argument is `all`, or no argument at all → walk through both sections (this matches
  `uv run --no-sync invoke ver.all`, which is what the check above already ran).

## Applying an update

Show the user the relevant table exactly as printed, then ask whether to apply it.

- `pyproject.toml`: this only rewrites version constraints — it does NOT install anything. If the
  user says yes, run `uv run --no-sync invoke ver.libs --yes` using the Bash tool, then tell them
  the locks were updated and that `uv run --no-sync invoke uv.upgrade_libs` will install them (do not
  run that yourself — installing is a separate, explicit step).
- `.github/workflows/`: this only rewrites `@ref` pins in the workflow files — it does NOT run any
  workflow. If the user says yes, run `uv run --no-sync invoke ver.workflows --yes` using the Bash
  tool, then tell them the workflow files were updated and suggest reviewing the diff before
  committing.

If the user declines a section, make no changes for that section.

---
name: dawn
description: List upstream Shopify/dawn version tags, or stage a Dawn upgrade onto a review branch and help resolve conflicts. Pass 'list' or 'upgrade'.
argument-hint: list | upgrade [version]
agent: agent
---

If $ARGUMENTS doesn't already specify it, ask the user: do you want to `list` available Dawn
versions, or `upgrade` (stage the latest — or a specific — version onto a review branch)?

## `list`

Run `uv run --no-sync invoke dawn.list` using the Bash tool and show the output to the user as-is.
It lists every upstream Shopify/dawn tag with the latest highlighted, and what `dawn_vanilla` is
currently synced to. Nothing to apply — stop here for this case.

## `upgrade`

1. If unclear, confirm with the user that `dawn_vanilla` has already been synced to the target
   version via the "Upgrade" GitHub Actions workflow (`.github/workflows/upgrade.yml`) — this
   command only brings that already-synced content onto a review branch, it doesn't fetch/merge
   upstream itself.
2. Run `uv run --no-sync invoke dawn.upgrade` (add `--version=<tag>` if the user gave one) using
   the Bash tool.
3. If it reports a clean rebase, there's nothing more to do — tell the user to run `/push` then
   `/pr` to open the PR into `development`.
4. If it reports conflicts, work through each conflicted file with the user:
   - Read `.github/instructions/fireball.instructions.md`'s tracking table first — it lists every
     hand-written Fireball customization and which files/lines they live in.
   - For each conflicted file, look at both sides of the conflict (`<<<<<<<` / `=======` /
     `>>>>>>>` markers) and decide whether to keep the Fireball customization, take upstream's new
     content, or hand-merge both — do not blindly prefer one side.
   - For files Dawn deleted upstream but we've modified (e.g. `.vscode/*`, `translation.yml`),
     ask the user whether to keep ours or accept the deletion rather than assuming.
   - After resolving a file, `git add` it. Once all conflicts in the current step are resolved,
     run `git rebase --continue` using the Bash tool. If more conflicts appear on a later commit,
     repeat this process for it.
5. Once the rebase completes cleanly, run `/push` then `/pr` to open the PR into `development`.

Never use `git checkout --theirs`/`--ours` or `-X theirs`/`-X ours` to blanket-resolve conflicts
here — Fireball customizations are hand-inserted inside Dawn's own files, so each conflict needs
an actual read, not a side-picking shortcut.

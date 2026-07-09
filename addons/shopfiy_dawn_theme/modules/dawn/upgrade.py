"""
Stage a Dawn upgrade for manual conflict resolution.

Assumes the "Upgrade" GitHub Actions workflow (.github/workflows/upgrade.yml) has already synced
`dawn_vanilla` to the target version. This brings those changes onto a new branch off
`development` for review — real conflicts with Fireball customizations stop here and must be
resolved by hand (or with an AI's help), never auto-resolved. See dawn.instructions.md for the
full workflow.

Usage:
    uv run --no-sync python -m modules.dawn.upgrade
    uv run --no-sync invoke dawn.upgrade [--version=v15.5.0]
    uv run --no-sync invoke dawn.upgrade [--version=latest]  # same as omitting --version
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..common import cli as click
from ..common.properties import get_repo_root
from ..common.utils import error, info, success, warning
from .list import fetch_tags, sort_key


def _run_ok(repo_path: Path, *args: str) -> bool:
    """Run a git command; return True on success (no output captured)."""
    result = subprocess.run(["git", "-C", str(repo_path), *args], check=False)
    return result.returncode == 0


def _run_out(repo_path: Path, *args: str) -> str:
    """Run a git command and return its stripped stdout."""
    result = subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True, text=True, check=False)
    return result.stdout.strip()


def _show_conflicts(repo_path: Path) -> None:
    """Print files with unresolved rebase conflicts and how to proceed."""
    conflicted = _run_out(repo_path, "diff", "--name-only", "--diff-filter=U")
    warning("Rebase hit conflicts — resolve manually:")
    for file in conflicted.splitlines():
        click.echo(f"  {file}")
    click.echo()
    click.echo("Resolve each file (see fireball.instructions.md for what Fireball customizations")
    click.echo("to preserve), then:  git add <file>...  &&  git rebase --continue")
    click.echo("Once the rebase is clean, run /push then /pr to open a PR into development.")


def main(version: str | None = None) -> None:
    """
    Create a feature branch off dawn_vanilla, rebased onto development, for manual review.

    Assumes dawn_vanilla is already synced to the target upstream version (via the "Upgrade"
    GitHub Actions workflow). This only brings those changes onto a review branch — it never
    auto-resolves conflicts or opens a PR; that's a deliberate, separate step.
    """
    repo_path = get_repo_root()

    if _run_out(repo_path, "status", "--porcelain"):
        error("Working tree has uncommitted changes — commit or stash them before running dawn.upgrade.")

    if version is None or version == "latest":
        tags = fetch_tags()
        if not tags:
            error("No version tags found on upstream Shopify/dawn.")
        tags.sort(key=sort_key)
        version = tags[-1]
        info(f"Resolved latest upstream tag for branch naming: {version}")

    info("Fetching development and dawn_vanilla from origin...")
    if not _run_ok(repo_path, "fetch", "origin", "development", "dawn_vanilla"):
        error("Failed to fetch origin/development and origin/dawn_vanilla.")

    branch = f"upgrade/dawn-vanilla-{version}"
    info(f"Creating {branch} from origin/dawn_vanilla...")
    if not _run_ok(repo_path, "checkout", "-b", branch, "origin/dawn_vanilla"):
        error(f"Failed to create branch {branch} from origin/dawn_vanilla — does it already exist locally?")

    info(f"Rebasing {branch} onto origin/development...")
    if _run_ok(repo_path, "rebase", "origin/development"):
        success(f"{branch} rebased cleanly onto development — no conflicts.")
        click.echo("Run /push then /pr to open a PR into development.")
        return

    _show_conflicts(repo_path)


if __name__ == "__main__":
    main()

"""Version-lock checks (pyproject.toml deps, workflow actions) and repo VERSION-file bumps."""

from invoke import task

from modules.versioning import libs as libs_module
from modules.versioning import project as project_module
from modules.versioning import workflows as workflows_module


@task
def libs(_context, dry_run=False, yes=False):
    """Check pyproject.toml dependencies against latest releases and update version locks"""
    libs_module.main(dry_run=dry_run, no_confirm=yes)


@task
def workflows(_context, dry_run=False, yes=False):
    """Check .github/workflows/ action refs against latest major versions and update them"""
    workflows_module.main(dry_run=dry_run, no_confirm=yes)


@task
def all(context, dry_run=False, yes=False):  # noqa: A001  # pylint: disable=redefined-builtin
    """Run every version check (libs, workflows)"""
    libs(context, dry_run=dry_run, yes=yes)
    workflows(context, dry_run=dry_run, yes=yes)


@task
def project_bump_build(_context):
    """Advance VERSION for a dev deploy (new minor's first build, or next build number)"""
    project_module.bump_build()


@task
def project_bump_release(_context):
    """Finalize VERSION for release by dropping the build suffix"""
    project_module.bump_release()

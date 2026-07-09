"""Dawn upstream version listing and upgrade-staging tasks."""

from invoke import task

from modules.dawn import list as dawn_list
from modules.dawn import upgrade as dawn_upgrade


@task(name="list")
def list_versions(_context):  # noqa: A001  # pylint: disable=redefined-builtin
    """List every version tag published on upstream Shopify/dawn, latest highlighted"""
    dawn_list.main()


@task
def upgrade(_context, version=None):
    """Create a feature branch off dawn_vanilla, rebased onto development, for manual review"""
    dawn_upgrade.main(version=version)

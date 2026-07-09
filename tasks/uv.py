"""uv sync tasks — install the dependency versions currently locked in pyproject.toml."""

from invoke import task


@task
def upgrade(context):
    """Install the dependency versions currently locked in pyproject.toml (uv sync)"""
    print("\n------------")
    print("uv sync")
    print("------------\n")
    context.run("uv sync")

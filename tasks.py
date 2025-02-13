from invoke import task


@task
def autoflake(ctx):
    """Remove all unused imports."""
    ctx.run('autoflake --remove-all-unused-imports --in-place --recursive .')


@task
def isort(ctx):
    """Sort imports."""
    ctx.run('isort .')


@task(pre=[autoflake, isort])
def format(ctx):
    """Format code by removing unused imports and sorting imports."""

# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Provide setuptools packaging task-runner."""

from typing import TYPE_CHECKING, Optional

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context

# TODO: handle setup() here?


# XXX: this is not setuptools but all builds
@task
def build(
    ctx,
    kind='wheel',
    outdir=None,
    skip_dependency_check=False,
    no_isolation=False,
):  # type: (Context, str, Optional[str], bool, bool) -> None
    """Build package."""
    args = []
    if kind == 'wheel':
        args.append('--wheel')
    elif kind == 'sdist':
        args.append('--sdist')
    else:
        raise Exception('cannot build unknown package format')
    if outdir:
        args.append(f"--outdir={outdir}")
    if skip_dependency_check:
        args.append('--skip-dependency-check')
    if no_isolation:
        args.append('--no-isolation')
    ctx.run(f"{ctx.python_path} -m build {' '.join(args)}")


tasks = Collection(build)

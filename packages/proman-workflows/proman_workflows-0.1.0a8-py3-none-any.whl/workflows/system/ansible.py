# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Deploy stack using Ansible."""

from typing import TYPE_CHECKING

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def install(
    ctx,  # type: Context
):  # type: (...) -> None
    """Install Ansible collections or roles."""
    ...


@task
def run(
    ctx,  # type: Context
):  # type: (...) -> None
    """Run Ansible deployment."""
    ...


namespace = Collection(install, run)

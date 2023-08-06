# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Run system tests using test-infra."""

from typing import TYPE_CHECKING

from invoke import Collection, task

if TYPE_CHECKING:
    from invoke import Context


@task
def run(
    ctx,  # type: Context
):  # type: (...) -> None
    """Run test-infra tests."""
    print('test-infra stub')


namespace = Collection(run)

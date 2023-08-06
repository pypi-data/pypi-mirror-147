# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Provide documentation task-runner."""

from ..collection import Collection

namespace = Collection(
    configuration={
        'plugins': [
            # {
            #     'name': 'docker',
            #     'driver_name': 'docker_compose',
            #     'driver_namespace': 'proman.workflows.container.compose',
            # },
            {
                'name': 'podman',
                'driver_name': 'podman_compose',
                'driver_namespace': 'proman.workflows.container.compose',
            },
        ]
    }
)

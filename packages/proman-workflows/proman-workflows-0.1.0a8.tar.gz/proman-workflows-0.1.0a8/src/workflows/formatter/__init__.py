# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Deploy  Task-Runner."""

import logging

from ..collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection(
    configuration={
        'plugins': [
            {
                'name': 'sort-headers',
                'driver_name': 'isort',
                'driver_namespace': 'proman.workflows.formatter',
            },
            {
                'name': 'format',
                'driver_name': 'black',
                'driver_namespace': 'proman.workflows.formatter',
            },
        ]
    }
)

__all__ = ['namespace']

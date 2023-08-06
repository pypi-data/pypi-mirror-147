# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from workflows.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection(
    configuration={
        'plugins': [
            {
                'name': 'unit-test',
                'driver_name': 'pytest',
                'driver_namespace': 'proman.workflows.qa',
            },
        ]
    }
)

__all__ = ['namespace']

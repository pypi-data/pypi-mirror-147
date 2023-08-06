# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Quality Assurance Task-Runner."""

import logging

from ..collection import Collection
from . import security

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble collections for namespace
namespace = Collection(
    configuration={
        'plugins': [
            {
                'name': 'lint',
                'driver_name': 'flake8',
                'driver_namespace': 'proman.workflows.sca',
            },
            {
                'name': 'type-checking',
                'driver_name': 'mypy',
                'driver_namespace': 'proman.workflows.sca',
            },
            # bandit = "workflows.sca.security.bandit:namespace"
            # safety = "workflows.sca.security.safety:namespace"
        ]
    }
)
namespace.add_collection(security.namespace, name='sec')

__all__ = ['namespace']

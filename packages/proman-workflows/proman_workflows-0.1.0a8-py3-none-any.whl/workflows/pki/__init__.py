# copyright: (c) 2020 by Jesse Johnson.
# license: AGPL-3.0-or-later, see LICENSE for more details.
"""Provide PKI Task-Runner."""

import logging

from workflows.collection import Collection

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Assemble namespace for namespace
namespace = Collection()
namespace.load_collection(
    'gpg', driver_name='gpg', driver_namespace='proman.workflows.pki'
)
namespace.load_collection(
    'tls', driver_name='tls', driver_namespace='proman.workflows.pki'
)

__all__ = ['namespace']

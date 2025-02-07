"""
P2Pool API module initializer.

This module provides the `P2PoolAPI` object to interact with the P2Pool API.
"""

# TODO: Fix logging
# TODO: Replace print statements
# TODO: Check version numbers and other metadata is correct
# TODO: Research pre-commit hooks to update version numbers in all relevant files

__name__ = "p2pool"
__author__ = "hreikin"
__email__ = "hreikin@gmail.com"
__version__ = "0.0.3"
__license__ = "MIT"
__description__ = "This module provides objects to interact with the P2Pool API and store collected data in a database."
__url__ = "https://hreikin.co.uk/p2pool-api"

from .api import P2PoolAPI

__all__ = ["P2PoolAPI"]

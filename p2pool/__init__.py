"""
P2Pool API module initializer.

This module provides the `P2PoolAPI` object to interact with the P2Pool API and store collected data in a database.
It includes:

Classes:
- P2PoolAPI: A class for interacting with P2Pool miner API data sources.
- P2PoolDatabase: A class for interacting with the P2Pool database.

Exceptions:
- P2PoolAPIError: General error with the P2Pool API.
- P2PoolConnectionError: Connection error with the P2Pool API.
- P2PoolDatabaseError: Database error with the P2Pool API.

ORM Models:
- Console: ORM model for the local console endpoint.
- P2P: ORM model for the local P2P endpoint.
- Stratum: ORM model for the local stratum endpoint.
- NetworkStats: ORM model for the network stats endpoint.
- PoolBlocks: ORM model for the pool blocks endpoint.
- PoolStats: ORM model for the pool stats endpoint.
- StatsMod: ORM model for the stats mod endpoint.

Helpers:
- _local_console_endpoint: API endpoint for local console.
- _local_p2p_endpoint: API endpoint for local P2P.
- _local_stratum_endpoint: API endpoint for local stratum.
- _network_stats_endpoint: API endpoint for network stats.
- _pool_blocks_endpoint: API endpoint for pool blocks.
- _pool_stats_endpoint: API endpoint for pool stats.
- _stats_mod_endpoint: API endpoint for stats mod.
- _local_console_table_name: Table name for local console.
- _local_p2p_table_name: Table name for local P2P.
- _local_stratum_table_name: Table name for local stratum.
- _network_stats_table_name: Table name for network stats.
- _pool_blocks_table_name: Table name for pool blocks.
- _pool_stats_table_name: Table name for pool stats.
- _stats_mod_table_name: Table name for stats mod.
"""

# // TODO: Test recent changes to the module.
# // TODO: Create ORM models for each endpoint.
# // TODO: Add database functionality to the module.
# // TODO: Create unittests for the module.
# // TODO: Create examples.
# // TODO: Docstrings
# TODO: Update documentation.
# TODO: Database example
# TODO: P2PoolConnectionError: is it used ?

__name__ = "p2pool"
__author__ = "hreikin"
__email__ = "hreikin@gmail.com"
__version__ = "0.1.4"
__license__ = "MIT"
__description__ = "This module provides objects to interact with the P2Pool API and store collected data in a database."
__url__ = "https://hreikin.co.uk/p2pool-api"

from .api import P2PoolAPI
from .db import P2PoolDatabase
from .exceptions import P2PoolAPIError, P2PoolConnectionError, P2PoolDatabaseError
from .models import Console, P2P, Stratum, NetworkStats, PoolBlocks, PoolStats, StatsMod
from .helpers import _local_console_endpoint, _local_p2p_endpoint, _local_stratum_endpoint, _network_stats_endpoint, _pool_blocks_endpoint, _pool_stats_endpoint, _stats_mod_endpoint, _local_console_table_name, _local_p2p_table_name, _local_stratum_table_name, _network_stats_table_name, _pool_blocks_table_name, _pool_stats_table_name, _stats_mod_table_name

__all__ = ["P2PoolAPI", "P2PoolDatabase", "P2PoolAPIError", "P2PoolConnectionError", "P2PoolDatabaseError", "Console", "P2P", "Stratum", "NetworkStats", "PoolBlocks", "PoolStats", "StatsMod", "_local_console_endpoint", "_local_p2p_endpoint", "_local_stratum_endpoint", "_network_stats_endpoint", "_pool_blocks_endpoint", "_pool_stats_endpoint", "_stats_mod_endpoint", "_local_console_table_name", "_local_p2p_table_name", "_local_stratum_table_name", "_network_stats_table_name", "_pool_blocks_table_name", "_pool_stats_table_name", "_stats_mod_table_name"]

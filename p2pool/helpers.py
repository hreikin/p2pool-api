"""
P2Pool Helpers module.

This module provides constants for various API endpoints and table names used in the P2Pool API.
It includes:

- API endpoints for local console, P2P, stratum, network stats, pool blocks, pool stats, and stats mod.
- Table names corresponding to the API endpoints.
"""

_local_console_endpoint = "local/console"
_local_p2p_endpoint = "local/p2p"
_local_stratum_endpoint = "local/stratum"
_network_stats_endpoint = "network/stats"
_pool_blocks_endpoint = "pool/blocks"
_pool_stats_endpoint = "pool/stats"
_stats_mod_endpoint = "stats_mod"
_local_console_table_name = "console"
_local_p2p_table_name = "p2p"
_local_stratum_table_name = "stratum"
_network_stats_table_name = "network_stats"
_pool_blocks_table_name = "pool_blocks"
_pool_stats_table_name = "pool_stats"
_stats_mod_table_name = "stats_mod"

# Define the public interface of the module
__all__ = ["_local_console_endpoint", "_local_p2p_endpoint", "_local_stratum_endpoint", "_network_stats_endpoint", "_pool_blocks_endpoint", "_pool_stats_endpoint", "_stats_mod_endpoint", "_local_console_table_name", "_local_p2p_table_name", "_local_stratum_table_name", "_network_stats_table_name", "_pool_blocks_table_name", "_pool_stats_table_name", "_stats_mod_table_name"]
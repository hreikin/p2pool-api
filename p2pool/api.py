"""
P2Pool API interaction library.

This module provides the `P2PoolAPI` class for interacting with various data sources in a P2Pool miner API.
"""

import json, logging, requests, traceback
from pathlib import Path
from urllib.parse import urlparse
from typing import Any
from p2pool.db import P2PoolDatabase
from p2pool.exceptions import P2PoolAPIError
from p2pool.helpers import _local_console_endpoint, _local_p2p_endpoint, _local_stratum_endpoint, _network_stats_endpoint, _pool_blocks_endpoint, _pool_stats_endpoint, _stats_mod_endpoint, _local_console_table_name, _local_p2p_table_name, _local_stratum_table_name, _network_stats_table_name, _pool_blocks_table_name, _pool_stats_table_name, _stats_mod_table_name

log = logging.getLogger("p2pool.api")

class P2PoolAPI:
    """
    A class for interacting with P2Pool miner API data sources.

    Attributes:
        _local_console (dict): Data retrieved from the `local/console` API endpoint.
        _local_p2p (dict): Data retrieved from the `local/p2p` API endpoint.
        _local_stratum (dict): Data retrieved from the `local/stratum` API endpoint.
        _network_stats (dict): Data retrieved from the `network/stats` API endpoint.
        _pool_blocks (dict): Data retrieved from the `pool/blocks` API endpoint.
        _pool_stats (dict): Data retrieved from the `pool/stats` API endpoint.
        _stats_mod (dict): Data retrieved from the `stats_mod` API endpoint.
    """

    def __init__(self, api_path: str, is_remote: bool = False, db_url: str = "sqlite:///p2pool.db"):
        """
        Initializes a P2PoolAPI instance.

        Args:
            api_path (str): The base path to the API data directory or URL.
            is_remote (bool): Indicates if the API path is a remote URL.
        """
        self._api_path = Path(api_path).resolve() if not is_remote else api_path
        self._is_remote = is_remote
        self._db_url = db_url
        self._local_console_cache = {}
        self._local_p2p_cache = {}
        self._local_stratum_cache = {}
        self._workers_full_cache = {}
        self._workers_cache = {}
        self._network_stats_cache = {}
        self._pool_blocks_cache = []
        self._pool_stats_cache = {}
        self._stats_mod_cache = {}
        if not self._validate_api_path(self._api_path, is_remote):
            raise ValueError("Invalid API path provided.")
        if self._db_url is not None:
            P2PoolDatabase._init_db(self._db_url)
        self.update_all_endpoints()

    def _validate_api_path(self, api_path: str, is_remote: bool) -> bool:
        """
        Validates the provided API path.

        Args:
            api_path (str): The API path to validate.
            is_remote (bool): Indicates if the API path is a remote URL.

        Returns:
            bool: True if the API path is valid, False otherwise.
        """
        if is_remote:
            # Validate URL
            parsed_url = urlparse(api_path)
            return all([parsed_url.scheme, parsed_url.netloc])
        else:
            # Validate local file path
            return Path(api_path).exists()

    def _fetch_data(self, endpoint: str) -> dict | bool:
        """
        Fetches data from the specified endpoint.

        Args:
            endpoint (str): The endpoint to fetch data from.

        Returns:
            dict | bool: The fetched data, or False if an error occurred.
        """
        try:
            if self._is_remote:
                response = requests.get(f"{self._api_path}/{endpoint}")
                response.raise_for_status()
                return response.json()
            else:
                with open(f"{self._api_path}/{endpoint}", "r") as reader:
                    return json.loads(reader.read())
        except requests.exceptions.RequestException as e:
            log.error(f"An error occurred fetching data from `{endpoint}`: {e}")
            return False
        except (OSError, json.JSONDecodeError) as e:
            log.error(f"An error occurred reading data from `{endpoint}`: {e}")
            return False

    def _get_data_from_cache(self, cache: dict | list, keys: list, table_name: str, selection: str) -> Any:
        """
        Retrieve data from a nested dictionary cache using a list of keys.

        Args:
            cache (dict | list): The cache dictionary to retrieve data from.
            keys (list): A list of keys to traverse the nested dictionary.

        Returns:
            Any: The retrieved data if the keys exist, otherwise "N/A".

        Raises:
            KeyError: If any key in the list of keys is not found in the cache.
        """
        data = "N/A"
        try:
            data = cache
            if len(keys) > 0:
                for key in keys:
                    data = data[key]
            return data
        except Exception as e:
            log.error(f"An error occurred fetching data from cache, trying database: {e}")
            raise P2PoolAPIError(e, traceback.format_exc(), f"An error occurred fetching data from cache: {e}") from e
        except P2PoolAPIError as e:
            return self._fallback_to_db(table_name, selection)
    
    def _fallback_to_db(self, table_name, selection):
        """
        Fallback to the database if the data is not available in the cache.

        Args:
            table_name (str): Name of the table to retrieve data from.
            selection (str): Column to select from the table.

        Returns:
            Any: The retrieved data, or a default string value of "N/A" if not available.
        """
        result = P2PoolDatabase.retrieve_data_from_db(self._db_url, table_name, selection)
        return result[0].get(selection, "N/A") if len(result) > 0 else "N/A"

    def _get_endpoint(self, endpoint: str) -> bool:
        """
        Loads data from the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to fetch data from.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        cache_attr = f"_{endpoint.replace('/', '_')}_cache"
        data = self._fetch_data(endpoint)
        if data:
            setattr(self, cache_attr, data)
            P2PoolDatabase._insert_data_into_db(data, endpoint, self._db_url)
            return True
        return False
    
    def get_from_db(self, table_name: str, selection: str) -> list:
        """
        Retrieve data from the database.

        Args:
            table_name (str): Name of the table to retrieve data from.
            selection (str): Column to select from the table.

        Returns:
            list: List of dictionaries containing the retrieved data.
        """
        return P2PoolDatabase.retrieve_data_from_db(self._db_url, table_name, selection)
    
    def update_local_console(self) -> bool:
        """
        Retrieve the data from local console endpoint.

        This method sends a request to the "local/console" endpoint and returns
        a bool representing the success or failure of the request.
        
        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_local_console_endpoint)

    def update_local_p2p(self) -> bool:
        """
        Retrieve the data from local P2P endpoint.
        
        This method sends a request to the "local/p2p" endpoint and returns
        a bool representing the success or failure of the request.

        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_local_p2p_endpoint)

    def update_local_stratum(self) -> bool:
        """
        Retrieve the data from local stratum endpoint.

        This method sends a request to the "local/stratum" endpoint and returns
        a bool representing the success or failure of the request.

        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_local_stratum_endpoint)

    def update_network_stats(self) -> bool:
        """
        Retrieve the data from network stats endpoint.
        
        This method sends a request to the "network/stats" endpoint and returns
        a bool representing the success or failure of the request.

        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_network_stats_endpoint)

    def update_pool_blocks(self) -> bool:
        """
        Retrieve the data from pool blocks endpoint.
        
        This method sends a request to the "pool/blocks" endpoint and returns
        a bool representing the success or failure of the request.

        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_pool_blocks_endpoint)

    def update_pool_stats(self) -> bool:
        """
        Retrieve the data from pool stats endpoint.

        This method sends a request to the "pool/stats" endpoint and returns
        a bool representing the success or failure of the request.

        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_pool_stats_endpoint)

    def update_stats_mod(self) -> bool:
        """
        Retrieve the data from stats mod endpoint.

        This method sends a request to the "stats_mod" endpoint and returns
        a bool representing the success or failure of the request.

        Returns:
            bool: The status of the request, True if successful, False otherwise.
        """
        return self._get_endpoint(_stats_mod_endpoint)

    def update_all_endpoints(self) -> bool:
        """
        Fetches and processes data from all API endpoints.

        Returns:
            bool: True if all data sources were successfully fetched, False otherwise.
        """
        try:
            update_local_console_success = self.update_local_console()
            update_local_p2p_success = self.update_local_p2p()
            update_local_stratum_success = self.update_local_stratum()
            update_network_stats_success = self.update_network_stats()
            update_pool_blocks_success = self.update_pool_blocks()
            update_pool_stats_success = self.update_pool_stats()
            update_stats_mod_success = self.update_stats_mod()
            if all([update_local_console_success, update_local_p2p_success, update_local_stratum_success, update_network_stats_success, update_pool_blocks_success, update_pool_stats_success, update_stats_mod_success]):
                log.info("All data fetched successfully.")
                return True
            log.error("An error occurred fetching some of the latest data, one or more endpoints failed.")
            log.error(f"update_local_console: {update_local_console_success},\nupdate_local_p2p: {update_local_p2p_success},\nupdate_local_stratum: {update_local_stratum_success},\nupdate_network_stats: {update_network_stats_success},\nupdate_pool_blocks: {update_pool_blocks_success},\nupdate_pool_stats: {update_pool_stats_success},\nupdate_stats_mod: {update_stats_mod_success}")
            return False
        except Exception as e:
            raise P2PoolAPIError(e, traceback.format_exc(), f"An error occurred fetching the latest data: {e}") from e

    @property
    def local_console(self) -> dict:
        """
        Returns the local console data.

        Returns:
            dict: The local console data.
        """
        return self._get_data_from_cache(self._local_console_cache, [], _local_console_table_name, "full_json")

    @property
    def local_p2p(self) -> dict:
        """
        Returns the local P2P data.

        Returns:
            dict: The local P2P data.
        """
        return self._get_data_from_cache(self._local_p2p_cache, [], _local_p2p_table_name, "full_json")

    @property
    def local_stratum(self) -> dict:
        """
        Returns the local stratum data.

        Returns:
            dict: The local stratum data.
        """
        return self._get_data_from_cache(self._local_stratum_cache, [], _local_stratum_table_name, "full_json")

    @property
    def network_stats(self) -> dict:
        """
        Returns the network stats data.

        Returns:
            dict: The network stats data.
        """
        return self._get_data_from_cache(self._network_stats_cache, [], _network_stats_table_name, "full_json")

    @property
    def pool_blocks(self) -> dict:
        """
        Returns the pool blocks data.

        Returns:
            dict: The pool blocks data.
        """
        return self._get_data_from_cache(self._pool_blocks_cache, [], _pool_blocks_table_name, "full_json")

    @property
    def pool_stats(self) -> dict:
        """
        Returns the pool stats data.

        Returns:
            dict: The pool stats data.
        """
        return self._get_data_from_cache(self._pool_stats_cache, [], _pool_stats_table_name, "full_json")

    @property
    def stats_mod(self) -> dict:
        """
        Returns the stats mod data.

        Returns:
            dict: The stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, [], _stats_mod_table_name, "full_json")

    @property
    def local_console_mode(self) -> str:
        """
        Returns the local console mode.

        Returns:
            str: The local console mode.
        """
        return self._get_data_from_cache(self._local_console_cache, ["mode"], _local_console_table_name, "mode")

    @property
    def local_console_tcp_port(self) -> int:
        """
        Returns the local console TCP port.

        Returns:
            int: The local console TCP port.
        """
        return self._get_data_from_cache(self._local_console_cache, ["tcp_port"], _local_console_table_name, "tcp_port")

    @property
    def local_p2p_connections(self) -> int:
        """
        Returns the number of local P2P connections.

        Returns:
            int: The number of local P2P connections.
        """
        return self._get_data_from_cache(self._local_p2p_cache, ["connections"], _local_p2p_table_name, "connections")

    @property
    def local_p2p_incoming_connections(self) -> int:
        """
        Returns the number of local P2P incoming connections.

        Returns:
            int: The number of local P2P incoming connections.
        """
        return self._get_data_from_cache(self._local_p2p_cache, ["incoming_connections"], _local_p2p_table_name, "incoming_connections")

    @property
    def local_p2p_peer_list_size(self) -> int:
        """
        Returns the size of the local P2P peer list.

        Returns:
            int: The size of the local P2P peer list.
        """
        return self._get_data_from_cache(self._local_p2p_cache, ["peer_list_size"], _local_p2p_table_name, "peer_list_size")

    @property
    def local_p2p_peers(self) -> list:
        """
        Returns the list of local P2P peers.

        Returns:
            list: The list of local P2P peers.
        """
        return self._get_data_from_cache(self._local_p2p_cache, ["peers"], _local_p2p_table_name, "peers")

    @property
    def local_p2p_uptime(self) -> int:
        """
        Returns the local P2P uptime.

        Returns:
            int: The local P2P uptime.
        """
        return self._get_data_from_cache(self._local_p2p_cache, ["uptime"], _local_p2p_table_name, "uptime")

    @property
    def local_stratum_hashrate_15m(self) -> int:
        """
        Returns the local stratum hashrate for the last 15 minutes.

        Returns:
            int: The local stratum hashrate for the last 15 minutes.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["hashrate_15m"], _local_stratum_table_name, "hashrate_15m")

    @property
    def local_stratum_hashrate_1h(self) -> int:
        """
        Returns the local stratum hashrate for the last hour.

        Returns:
            int: The local stratum hashrate for the last hour.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["hashrate_1h"], _local_stratum_table_name, "hashrate_1h")

    @property
    def local_stratum_hashrate_24h(self) -> int:
        """
        Returns the local stratum hashrate for the last 24 hours.

        Returns:
            int: The local stratum hashrate for the last 24 hours.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["hashrate_24h"], _local_stratum_table_name, "hashrate_24h")

    @property
    def local_stratum_total_hashes(self) -> int:
        """
        Returns the total number of hashes for the local stratum.

        Returns:
            int: The total number of hashes for the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["total_hashes"], _local_stratum_table_name, "total_hashes")

    @property
    def local_stratum_shares_found(self) -> int:
        """
        Returns the number of shares found by the local stratum.

        Returns:
            int: The number of shares found by the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["shares_found"], _local_stratum_table_name, "shares_found")

    @property
    def local_stratum_shares_failed(self) -> int:
        """
        Returns the number of shares failed by the local stratum.

        Returns:
            int: The number of shares failed by the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["shares_failed"], _local_stratum_table_name, "shares_failed")

    @property
    def local_stratum_average_effort(self) -> int:
        """
        Returns the average effort of the local stratum.

        Returns:
            int: The average effort of the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["average_effort"], _local_stratum_table_name, "average_effort")

    @property
    def local_stratum_current_effort(self) -> int:
        """
        Returns the current effort of the local stratum.

        Returns:
            int: The current effort of the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["current_effort"], _local_stratum_table_name, "current_effort")

    @property
    def local_stratum_connections(self) -> int:
        """
        Returns the number of connections to the local stratum.

        Returns:
            int: The number of connections to the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["connections"], _local_stratum_table_name, "connections")

    @property
    def local_stratum_incoming_connections(self) -> int:
        """
        Returns the number of incoming connections to the local stratum.

        Returns:
            int: The number of incoming connections to the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["incoming_connections"], _local_stratum_table_name, "incoming_connections")

    @property
    def local_stratum_block_reward_share_percent(self) -> int:
        """
        Returns the block reward share percentage of the local stratum.

        Returns:
            int: The block reward share percentage of the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["block_reward_share_percent"], _local_stratum_table_name, "block_reward_share_percent")

    @property
    def local_stratum_workers_full(self) -> list:
        """
        Returns the full list of workers for the local stratum.

        Returns:
            list: The full list of workers for the local stratum.
        """
        return self._get_data_from_cache(self._local_stratum_cache, ["workers"], _local_stratum_table_name, "workers")

    @property
    def local_stratum_workers_short(self) -> list:
        """
        Returns the list of workers for the local stratum.

        Returns:
            list: The short list of workers for the local stratum.
        """
        workers = self._get_data_from_cache(self._local_stratum_cache, ["workers"], _local_stratum_table_name, "workers")
        result = [w.split(",") for w in workers]
        return sorted(result, key=lambda x: int(x[3]), reverse=True)

    @property
    def network_stats_difficulty(self) -> int:
        """
        Returns the network difficulty.

        Returns:
            int: The network difficulty.
        """
        return self._get_data_from_cache(self._network_stats_cache, ["difficulty"], _network_stats_table_name, "difficulty")

    @property
    def network_stats_hash(self) -> str:
        """
        Returns the network hash.

        Returns:
            str: The network hash.
        """
        return self._get_data_from_cache(self._network_stats_cache, ["hash"], _network_stats_table_name, "hash_value")

    @property
    def network_stats_height(self) -> int:
        """
        Returns the network height.

        Returns:
            int: The network height.
        """
        return self._get_data_from_cache(self._network_stats_cache, ["height"], _network_stats_table_name, "height")

    @property
    def network_stats_reward(self) -> int:
        """
        Returns the network reward.

        Returns:
            int: The network reward.
        """
        return self._get_data_from_cache(self._network_stats_cache, ["reward"], _network_stats_table_name, "reward")

    @property
    def network_stats_timestamp(self) -> int:
        """
        Returns the network timestamp.

        Returns:
            int: The network timestamp.
        """
        return self._get_data_from_cache(self._network_stats_cache, ["timestamp"], _network_stats_table_name, "timestamp")

    @property
    def pool_blocks_heights(self) -> list[int]:
        """
        Returns the list of pool block heights.

        Returns:
            list[int]: The list of pool block heights.
        """
        heights = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [], _pool_blocks_table_name, "full_json")
            for i in pool_blocks:
                heights.append(i["height"])
            return heights
        except Exception as e:
            log.error(f"An error occurred fetching pool block heights: {e}")
            return "N/A"

    @property
    def pool_blocks_hashes(self) -> list[str]:
        """
        Returns the list of pool block hashes.

        Returns:
            list[str]: The list of pool block hashes.
        """
        hashes = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [], _pool_blocks_table_name, "full_json")
            for i in pool_blocks:
                hashes.append(i["hash"])
            return hashes
        except Exception as e:
            log.error(f"An error occurred fetching pool block hashes: {e}")
            return "N/A"

    @property
    def pool_blocks_difficulties(self) -> list[int]:
        """
        Returns the list of pool block difficulties.

        Returns:
            list[int]: The list of pool block difficulties.
        """
        difficulties = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [], _pool_blocks_table_name, "full_json")
            for i in pool_blocks:
                difficulties.append(i["difficulty"])
            return difficulties
        except Exception as e:
            log.error(f"An error occurred fetching pool block difficulties: {e}")
            return "N/A"

    @property
    def pool_blocks_total_hashes(self) -> list[int]:
        """
        Returns the list of total hashes for pool blocks.

        Returns:
            list[int]: The list of total hashes for pool blocks.
        """
        total_hashes = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [], _pool_blocks_table_name, "full_json")
            for i in pool_blocks:
                total_hashes.append(i["totalHashes"])
            return total_hashes
        except Exception as e:
            log.error(f"An error occurred fetching pool block total hashes: {e}")
            return "N/A"

    @property
    def pool_blocks_timestamps(self) -> list[int]:
        """
        Returns the list of timestamps for pool blocks.

        Returns:
            list[int]: The list of timestamps for pool blocks.
        """
        timestamps = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [], _pool_blocks_table_name, "full_json")
            for i in pool_blocks:
                timestamps.append(i["ts"])
            return timestamps
        except Exception as e:
            log.error(f"An error occurred fetching pool block timestamps: {e}")
            return "N/A"
    
    @property
    def pool_stats_pool_list(self) -> list[str]:
        """
        Returns the pool stats pool list.

        Returns:
            list[str]: The pool stats pool list.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_list"], _pool_stats_table_name, "pool_list")

    @property
    def pool_stats_payout_type(self) -> str:
        """
        Returns the pool stats payout type.

        Returns:
            str: The pool stats payout type.
        """
        result = self._get_data_from_cache(self._pool_stats_cache, ["pool_list"], _pool_stats_table_name, "pool_list")
        return result[0]
    
    @property
    def pool_stats_pool_statistics(self) -> dict:
        """
        Returns the pool stats pool statistics.

        Returns:
            dict: The pool stats pool statistics.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics"], _pool_stats_table_name, "pool_statistics")
    
    @property
    def pool_stats_hashrate(self) -> int:
        """
        Returns the pool stats hash rate.

        Returns:
            int: The pool stats hash rate.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "hashRate"], _pool_stats_table_name, "hashrate")

    @property
    def pool_stats_miners(self) -> int:
        """
        Returns the number of miners in the pool stats.

        Returns:
            int: The number of miners in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "miners"], _pool_stats_table_name, "miners")

    @property
    def pool_stats_total_hashes(self) -> int:
        """
        Returns the total number of hashes in the pool stats.

        Returns:
            int: The total number of hashes in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "totalHashes"], _pool_stats_table_name, "total_hashes")

    @property
    def pool_stats_last_block_found_time(self) -> int:
        """
        Returns the last block found time in the pool stats.

        Returns:
            int: The last block found time in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "lastBlockFoundTime"], _pool_stats_table_name, "last_block_found_time")

    @property
    def pool_stats_last_block_found(self) -> int:
        """
        Returns the last block found in the pool stats.

        Returns:
            int: The last block found in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "lastBlockFound"], _pool_stats_table_name, "last_block_found")

    @property
    def pool_stats_total_blocks_found(self) -> int:
        """
        Returns the total number of blocks found in the pool stats.

        Returns:
            int: The total number of blocks found in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "totalBlocksFound"], _pool_stats_table_name, "total_blocks_found")

    @property
    def pool_stats_pplns_weight(self) -> int:
        """
        Returns the PPLNS weight in the pool stats.

        Returns:
            int: The PPLNS weight in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "pplnsWeight"], _pool_stats_table_name, "pplns_weight")

    @property
    def pool_stats_pplns_window_size(self) -> int:
        """
        Returns the PPLNS window size in the pool stats.

        Returns:
            int: The PPLNS window size in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "pplnsWindowSize"], _pool_stats_table_name, "pplns_window_size")

    @property
    def pool_stats_sidechain_difficulty(self) -> int:
        """
        Returns the sidechain difficulty in the pool stats.

        Returns:
            int: The sidechain difficulty in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "sidechainDifficulty"], _pool_stats_table_name, "sidechain_difficulty")

    @property
    def pool_stats_sidechain_height(self) -> int:
        """
        Returns the sidechain height in the pool stats.

        Returns:
            int: The sidechain height in the pool stats.
        """
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "sidechainHeight"], _pool_stats_table_name, "sidechain_height")

    @property
    def stats_mod_config(self) -> dict:
        """
        Returns the stats mod config.

        Returns:
            dict: The stats mod config.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["config"], _stats_mod_table_name, "config")

    @property
    def stats_mod_ports(self) -> list[dict]:
        """
        Returns the list of ports in the stats mod config.

        Returns:
            list[dict]: The list of ports in the stats mod config.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["config", "ports"], _stats_mod_table_name, "ports")

    @property
    def stats_mod_port_values(self) -> list[int]:
        """
        Returns the list of ports in the stats mod config.

        Returns:
            list[int]: The list of ports in the stats mod config.
        """
        ports = []
        try:
            config_ports = self._get_data_from_cache(self._stats_mod_cache, ["config", "ports"], _stats_mod_table_name, "ports")
            for i in config_ports:
                ports.append(i["port"])
            return ports
        except Exception as e:
            log.error(f"An error occurred fetching stats mod port values: {e}")
            return "N/A"

    @property
    def stats_mod_tls(self) -> list[bool]:
        """
        Returns the list of TLS settings in the stats mod config.

        Returns:
            list[bool]: The list of TLS settings in the stats mod config.
        """
        tls = []
        try:
            config_ports = self._get_data_from_cache(self._stats_mod_cache, ["config", "ports"], _stats_mod_table_name, "ports")
            for i in config_ports:
                tls.append(i["tls"])
            return tls
        except Exception as e:
            log.error(f"An error occurred fetching stats mod TLS settings: {e}")
            return "N/A"

    @property
    def stats_mod_fee(self) -> int:
        """
        Returns the fee in the stats mod config.

        Returns:
            int: The fee in the stats mod config.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["config", "fee"], _stats_mod_table_name, "fee")

    @property
    def stats_mod_min_payment_threshold(self) -> int:
        """
        Returns the minimum payment threshold in the stats mod config.

        Returns:
            int: The minimum payment threshold in the stats mod config.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["config", "minPaymentThreshold"], _stats_mod_table_name, "min_payment_threshold")

    @property
    def stats_mod_network(self) -> dict:
        """
        Returns the network in the stats mod data.

        Returns:
            dict: The network in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["network"], _stats_mod_table_name, "network")

    @property
    def stats_mod_network_height(self) -> int:
        """
        Returns the network height in the stats mod data.

        Returns:
            int: The network height in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["network", "height"], _stats_mod_table_name, "height")

    @property
    def stats_mod_pool(self) -> dict:
        """
        Returns the pool in the stats mod data.

        Returns:
            dict: The pool in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool"], _stats_mod_table_name, "pool")
    
    @property
    def stats_mod_pool_stats(self) -> dict:
        """
        Returns the pool stats in the stats mod data.

        Returns:
            dict: The pool stats in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "stats"], _stats_mod_table_name, "stats")

    @property
    def stats_mod_last_block_found(self) -> str:
        """
        Returns the last block found in the stats mod data.

        Returns:
            str: The last block found in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "stats", "lastBlockFound"], _stats_mod_table_name, "last_block_found")

    @property
    def stats_mod_blocks(self) -> list:
        """
        Returns the list of blocks in the stats mod data.

        Returns:
            list: The list of blocks in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "blocks"], _stats_mod_table_name, "blocks")

    @property
    def stats_mod_miners(self) -> int:
        """
        Returns the number of miners in the stats mod data.

        Returns:
            int: The number of miners in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "miners"], _stats_mod_table_name, "miners")

    @property
    def stats_mod_hashrate(self) -> int:
        """
        Returns the hashrate in the stats mod data.

        Returns:
            int: The hashrate in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "hashrate"], _stats_mod_table_name, "hashrate")

    @property
    def stats_mod_round_hashes(self) -> int:
        """
        Returns the round hashes in the stats mod data.

        Returns:
            int: The round hashes in the stats mod data.
        """
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "roundHashes"], _stats_mod_table_name, "round_hashes")

# Define the public interface of the module
__all__ = ["P2PoolAPI"]
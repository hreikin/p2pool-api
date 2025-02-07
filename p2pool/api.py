"""
P2Pool API interaction library.

This module provides the `P2PoolAPI` class for interacting with various data sources in a P2Pool miner API.
"""

import json, logging, requests, traceback
from pathlib import Path
from urllib.parse import urlparse
from p2pool.exceptions import P2PoolAPIError
from typing import Any

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

    def __init__(self, api_path: str, is_remote: bool = False):
        """
        Initializes a P2PoolAPI instance.

        Args:
            api_path (str): The base path to the API data directory or URL.
            is_remote (bool): Indicates if the API path is a remote URL.
        """
        if not self._validate_api_path(api_path, is_remote):
            raise ValueError("Invalid API path provided.")
        
        self._api_path = Path(api_path).resolve() if not is_remote else api_path
        self._is_remote = is_remote
        self._local_console_cache = {}
        self._local_p2p_cache = {}
        self._local_stratum_cache = {}
        self._workers_full_cache = {}
        self._workers_cache = {}
        self._network_stats_cache = {}
        self._pool_blocks_cache = {}
        self._pool_stats_cache = {}
        self._stats_mod_cache = {}
        self.get_all_data()

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

    def _get_data_from_cache(self, cache: dict, keys: list) -> Any:
        """
        Retrieve data from a nested dictionary cache using a list of keys.

        Args:
            cache (dict): The cache dictionary to retrieve data from.
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
        except KeyError:
            log.error("Key not found in cache")
            return "N/A"
    
    def get_local_console(self) -> bool:
        """
        Loads data from the `local/console` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._local_console_cache = self._fetch_data("local/console")
        return bool(self._local_console_cache)

    def get_local_p2p(self) -> bool:
        """
        Loads data from the `local/p2p` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._local_p2p_cache = self._fetch_data("local/p2p")
        return bool(self._local_p2p_cache)

    def get_local_stratum(self) -> bool:
        """
        Loads data from the `local/stratum` API endpoint and processes worker data.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._local_stratum_cache = self._fetch_data("local/stratum")
        if self._local_stratum_cache:
            self._workers_full_cache = self._local_stratum_cache["workers"]
            self._workers_cache = []
            for w in self._workers_full_cache:
                w_list = w.split(",")
                self._workers_cache.append(w_list)
            self._workers_cache = sorted(self._workers_cache, key=lambda x: int(x[3]), reverse=True)
            return True
        return False

    def get_network_stats(self) -> bool:
        """
        Loads data from the `network/stats` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._network_stats_cache = self._fetch_data("network/stats")
        return bool(self._network_stats_cache)

    def get_pool_blocks(self) -> bool:
        """
        Loads data from the `pool/blocks` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._pool_blocks_cache = self._fetch_data("pool/blocks")
        return bool(self._pool_blocks_cache)

    def get_pool_stats(self) -> bool:
        """
        Loads data from the `pool/stats` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._pool_stats_cache = self._fetch_data("pool/stats")
        return bool(self._pool_stats_cache)

    def get_stats_mod(self) -> bool:
        """
        Loads data from the `stats_mod` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        self._stats_mod_cache = self._fetch_data("stats_mod")
        return bool(self._stats_mod_cache)

    def get_all_data(self) -> bool:
        """
        Fetches and processes data from all API endpoints.

        Returns:
            bool: True if all data sources were successfully fetched, False otherwise.
        """
        try:
            get_local_console_success = self.get_local_console()
            get_local_p2p_success = self.get_local_p2p()
            get_local_stratum_success = self.get_local_stratum()
            get_network_stats_success = self.get_network_stats()
            get_pool_blocks_success = self.get_pool_blocks()
            get_pool_stats_success = self.get_pool_stats()
            get_stats_mod_success = self.get_stats_mod()
            if all([get_local_console_success, get_local_p2p_success, get_local_stratum_success, get_network_stats_success, get_pool_blocks_success, get_pool_stats_success, get_stats_mod_success]):
                log.info("All data fetched successfully.")
                return True
            log.error("An error occurred fetching some of the latest data, one or more endpoints failed.")
            log.error(f"get_local_console: {get_local_console_success},\nget_local_p2p: {get_local_p2p_success},\nget_local_stratum: {get_local_stratum_success},\nget_network_stats: {get_network_stats_success},\nget_pool_blocks: {get_pool_blocks_success},\nget_pool_stats: {get_pool_stats_success},\nget_stats_mod: {get_stats_mod_success}")
            return False
        except Exception as e:
            raise P2PoolAPIError(e, traceback.format_exc(), f"An error occurred fetching the latest data: {e}") from e

    @property
    def local_console(self):
        return self._get_data_from_cache(self._local_console_cache, [])

    @property
    def local_p2p(self):
        return self._get_data_from_cache(self._local_p2p_cache, [])

    @property
    def local_stratum(self):
        return self._get_data_from_cache(self._local_stratum_cache, [])

    @property
    def network_stats(self):
        return self._get_data_from_cache(self._network_stats_cache, [])

    @property
    def pool_blocks(self):
        return self._get_data_from_cache(self._pool_blocks_cache, [])

    @property
    def pool_stats(self):
        return self._get_data_from_cache(self._pool_stats_cache, [])

    @property
    def stats_mod(self):
        return self._get_data_from_cache(self._stats_mod_cache, [])
    
    @property
    def local_console_mode(self):
        return self._get_data_from_cache(self._local_console_cache, ["mode"])
    
    @property
    def local_console_tcp_port(self):
        return self._get_data_from_cache(self._local_console_cache, ["tcp_port"])
    
    @property
    def local_p2p_connections(self):
        return self._get_data_from_cache(self._local_p2p_cache, ["connections"])
    
    @property
    def local_p2p_incoming_connections(self):
        return self._get_data_from_cache(self._local_p2p_cache, ["incoming_connections"])
    
    @property
    def local_p2p_peer_list_size(self):
        return self._get_data_from_cache(self._local_p2p_cache, ["peer_list_size"])
    
    @property
    def local_p2p_peers(self):
        return self._get_data_from_cache(self._local_p2p_cache, ["peers"])
    
    @property
    def local_p2p_uptime(self):
        return self._get_data_from_cache(self._local_p2p_cache, ["uptime"])
    
    @property
    def local_stratum_hashrate_15m(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["hashrate_15m"])
    
    @property
    def local_stratum_hashrate_1h(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["hashrate_1h"])
    
    @property
    def local_stratum_hashrate_24h(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["hashrate_24h"])
    
    @property
    def local_stratum_total_hashes(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["total_hashes"])
    
    @property
    def local_stratum_shares_found(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["shares_found"])
    
    @property
    def local_stratum_shares_failed(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["shares_failed"])
    
    @property
    def local_stratum_average_effort(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["average_effort"])
    
    @property
    def local_stratum_current_effort(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["current_effort"])
    
    @property
    def local_stratum_connections(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["connections"])
    
    @property
    def local_stratum_incoming_connections(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["incoming_connections"])
    
    @property
    def local_stratum_block_reward_share_percent(self):
        return self._get_data_from_cache(self._local_stratum_cache, ["block_reward_share_percent"])
    
    @property
    def local_stratum_workers_full(self):
        return self._get_data_from_cache(self._workers_full_cache, [])

    @property
    def local_stratum_workers(self):
        return self._get_data_from_cache(self._workers_cache, [])
    
    @property
    def network_stats_difficulty(self):
        return self._get_data_from_cache(self._network_stats_cache, ["difficulty"])
    
    @property
    def network_stats_hash(self):
        return self._get_data_from_cache(self._network_stats_cache, ["hash"])
    
    @property
    def network_stats_height(self):
        return self._get_data_from_cache(self._network_stats_cache, ["height"])
    
    @property
    def network_stats_reward(self):
        return self._get_data_from_cache(self._network_stats_cache, ["reward"])
    
    @property
    def network_stats_timestamp(self):
        return self._get_data_from_cache(self._network_stats_cache, ["ts"])
    
    @property
    def pool_blocks_heights(self):
        heights = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [])
            for i in pool_blocks:
                heights.append(pool_blocks[i]["height"])
            return heights
        except Exception as e:
            return "N/A"
    
    @property
    def pool_blocks_hashes(self):
        hashes = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [])
            for i in pool_blocks:
                hashes.append(pool_blocks[i]["hash"])
            return hashes
        except Exception as e:
            return "N/A"
    
    @property
    def pool_blocks_difficulties(self):
        difficulties = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [])
            for i in pool_blocks:
                difficulties.append(pool_blocks[i]["difficulty"])
            return difficulties
        except Exception as e:
            return "N/A"
    
    @property
    def pool_blocks_total_hashes(self):
        total_hashes = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [])
            for i in pool_blocks:
                total_hashes.append(pool_blocks[i]["totalHashes"])
            return total_hashes
        except Exception as e:
            return "N/A"
    
    @property
    def pool_blocks_timestamps(self):
        timestamps = []
        try:
            pool_blocks = self._get_data_from_cache(self._pool_blocks_cache, [])
            for i in pool_blocks:
                timestamps.append(pool_blocks[i]["ts"])
            return timestamps
        except Exception as e:
            return "N/A"
    
    @property
    def pool_stats_payout_type(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_list", 0])
    
    @property
    def pool_stats_hash_rate(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "hashRate"])
    
    @property
    def pool_stats_miners(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "miners"])
    
    @property
    def pool_stats_total_hashes(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "totalHashes"])
    
    @property
    def pool_stats_last_block_found_time(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "lastBlockFoundTime"])
    
    @property
    def pool_stats_last_block_found(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "lastBlockFound"])
    
    @property
    def pool_stats_total_blocks_found(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "totalBlocksFound"])
    
    @property
    def pool_stats_pplns_weight(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "pplnsWeight"])
    
    @property
    def pool_stats_pplns_window_size(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "pplnsWindowSize"])
    
    @property
    def pool_stats_sidechain_difficulty(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "sidechainDifficulty"])
    
    @property
    def pool_stats_sidechain_height(self):
        return self._get_data_from_cache(self._pool_stats_cache, ["pool_statistics", "sidechainHeight"])
    
    @property
    def stats_mod_config(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["config"])
    
    @property
    def stats_mod_ports(self):
        ports = []
        try:
            config_ports = self._get_data_from_cache(self._stats_mod_cache, ["config", "ports"])
            for i in config_ports:
                ports.append(config_ports[i]["port"])
            return ports
        except Exception as e:
            return "N/A"
    
    @property
    def stats_mod_tls(self):
        tls = []
        try:
            config_ports = self._get_data_from_cache(self._stats_mod_cache, ["config", "ports"])
            for i in config_ports:
                tls.append(config_ports[i]["tls"])
            return tls
        except Exception as e:
            return "N/A"
    
    @property
    def stats_mod_fee(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["config", "fee"])
    
    @property
    def stats_mod_min_payment_threshold(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["config", "minPaymentThreshold"])
    
    @property
    def stats_mod_network_height(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["network", "height"])
    
    @property
    def stats_mod_last_block_found(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "stats", "lastBlockFound"])
    
    @property
    def stats_mod_blocks(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "blocks"])
    
    @property
    def stats_mod_miners(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "miners"])
    
    @property
    def stats_mod_hashrate(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "hashrate"])
    
    @property
    def stats_mod_round_hashes(self):
        return self._get_data_from_cache(self._stats_mod_cache, ["pool", "roundHashes"])

# Define the public interface of the module
__all__ = ["P2PoolAPI"]
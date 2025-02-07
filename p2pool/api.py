"""
P2Pool API interaction library.

This module provides the `P2PoolAPI` class for interacting with various data sources in a P2Pool miner API.
"""

import json, logging, requests
from pathlib import Path
from urllib.parse import urlparse

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
    def local_console(self) -> dict | bool:
        """
        The data from the `local/console` endpoint.

        Returns:
            dict |: The data from the `local/console` endpoint, False otherwise
        """
        try:
            log.debug(self._local_console_cache)
            return self._local_console_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `local_console` data: {e}")
            return False

    @property
    def local_p2p(self) -> dict | bool:
        """
        The data from the `local/p2p` endpoint.

        Returns:
            dict |: The data from the `local/p2p` endpoint, False otherwise
        """
        try:
            log.debug(self._local_p2p_cache)
            return self._local_p2p_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `local_p2p` data: {e}")
            return False

    @property
    def local_stratum(self) -> dict | bool:
        """
        The data from the `local/stratum` endpoint.

        Returns:
            dict |: The data from the `local/stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache)
            return self._local_stratum_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `local_stratum` data: {e}")
            return False

    @property
    def network_stats(self) -> dict | bool:
        """
        The data from the `network/stats` endpoint.

        Returns:
            dict |: The data from the `network/stats` endpoint, False otherwise
        """
        try:
            log.debug(self._network_stats_cache)
            return self._network_stats_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `network_stats` data: {e}")
            return False

    @property
    def pool_blocks(self) -> dict | bool:
        """
        The data from the `pool/blocks` endpoint.

        Returns:
            dict |: The data from the `pool/blocks` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_blocks_cache)
            return self._pool_blocks_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `pool_blocks` data: {e}")
            return False

    @property
    def pool_stats(self) -> dict | bool:
        """
        The data from the `pool/stats` endpoint.

        Returns:
            dict |: The data from the `pool/stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache)
            return self._pool_stats_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `pool_stats` data: {e}")
            return False

    @property
    def stats_mod(self) -> dict | bool:
        """
        The data from the `stats_mod` endpoint.

        Returns:
            dict |: The data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache)
            return self._stats_mod_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `stats_mod` data: {e}")
            return False
    
    @property
    def local_console_mode(self) -> str | bool:
        """
        The `mode` data from the `local_console` endpoint.

        Returns:
            str | bool: The `mode` data from the `local_console` endpoint, False otherwise
        """
        try:
            log.debug(self._local_console_cache["mode"])
            return self._local_console_cache["mode"]
        except Exception as e:
            log.error(f"An error occurred fetching the `mode` data: {e}")
            return False
    
    @property
    def local_console_tcp_port(self) -> str | bool:
        """
        The `tcp_port` data from the `local_console` endpoint.

        Returns:
            str | bool: The `tcp_port` data from the `local_console` endpoint, False otherwise
        """
        try:
            log.debug(self._local_console_cache["tcp_port"])
            return self._local_console_cache["tcp_port"]
        except Exception as e:
            log.error(f"An error occurred fetching the `tcp_port` data: {e}")
            return False
    
    @property
    def local_p2p_connections(self) -> int | bool:
        """
        The `connections` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `connections` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            log.debug(self._local_p2p_cache["connections"])
            return self._local_p2p_cache["connections"]
        except Exception as e:
            log.error(f"An error occurred fetching the `connections` data: {e}")
            return False
    
    @property
    def local_p2p_incoming_connections(self) -> int | bool:
        """
        The `incoming_connections` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `incoming_connections` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            log.debug(self._local_p2p_cache["incoming_connections"])
            return self._local_p2p_cache["incoming_connections"]
        except Exception as e:
            log.error(f"An error occurred fetching the `incoming_connections` data: {e}")
            return False
    
    @property
    def local_p2p_peer_list_size(self) -> int | bool:
        """
        The `peer_list_size` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `peer_list_size` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            log.debug(self._local_p2p_cache["peer_list_size"])
            return self._local_p2p_cache["peer_list_size"]
        except Exception as e:
            log.error(f"An error occurred fetching the `peer_list_size` data: {e}")
            return False
    
    @property
    def local_p2p_peers(self) -> list | bool:
        """
        The `peers` data from the `local_p2p` endpoint.

        Returns:
            list | bool: The `peers` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            log.debug(self._local_p2p_cache["peers"])
            return self._local_p2p_cache["peers"]
        except Exception as e:
            log.error(f"An error occurred fetching the `peers` data: {e}")
            return False
    
    @property
    def local_p2p_uptime(self) -> int | bool:
        """
        The `uptime` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `uptime` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            log.debug(self._local_p2p_cache["uptime"])
            return self._local_p2p_cache["uptime"]
        except Exception as e:
            log.error(f"An error occurred fetching the `uptime` data: {e}")
            return False
    
    @property
    def local_stratum_hashrate_15m(self) -> int | bool:
        """
        The `hashrate_15m` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `hashrate_15m` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["hashrate_15m"])
            return self._local_stratum_cache["hashrate_15m"]
        except Exception as e:
            log.error(f"An error occurred fetching the `hashrate_15m` data: {e}")
            return False
    
    @property
    def local_stratum_hashrate_1h(self) -> int | bool:
        """
        The `hashrate_1h` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `hashrate_1h` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["hashrate_1h"])
            return self._local_stratum_cache["hashrate_1h"]
        except Exception as e:
            log.error(f"An error occurred fetching the `hashrate_1h` data: {e}")
            return False
    
    @property
    def local_stratum_hashrate_24h(self) -> int | bool:
        """
        The `hashrate_24h` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `hashrate_24h` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["hashrate_24h"])
            return self._local_stratum_cache["hashrate_24h"]
        except Exception as e:
            log.error(f"An error occurred fetching the `hashrate_24h` data: {e}")
            return False
    
    @property
    def local_stratum_total_hashes(self) -> int | bool:
        """
        The `total_hashes` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `total_hashes` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["total_hashes"])
            return self._local_stratum_cache["total_hashes"]
        except Exception as e:
            log.error(f"An error occurred fetching the `total_hashes` data: {e}")
            return False
    
    @property
    def local_stratum_shares_found(self) -> int | bool:
        """
        The `shares_found` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `shares_found` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["shares_found"])
            return self._local_stratum_cache["shares_found"]
        except Exception as e:
            log.error(f"An error occurred fetching the `shares_found` data: {e}")
            return False
    
    @property
    def local_stratum_shares_failed(self) -> int | bool:
        """
        The `shares_failed` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `shares_failed` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["shares_failed"])
            return self._local_stratum_cache["shares_failed"]
        except Exception as e:
            log.error(f"An error occurred fetching the `shares_failed` data: {e}")
            return False
    
    @property
    def local_stratum_average_effort(self) -> int | bool:
        """
        The `average_effort` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `average_effort` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["average_effort"])
            return self._local_stratum_cache["average_effort"]
        except Exception as e:
            log.error(f"An error occurred fetching the `average_effort` data: {e}")
            return False
    
    @property
    def local_stratum_current_effort(self) -> int | bool:
        """
        The `current_effort` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `current_effort` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["current_effort"])
            return self._local_stratum_cache["current_effort"]
        except Exception as e:
            log.error(f"An error occurred fetching the `current_effort` data: {e}")
            return False
    
    @property
    def local_stratum_connections(self) -> int | bool:
        """
        The `connections` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `connections` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["connections"])
            return self._local_stratum_cache["connections"]
        except Exception as e:
            log.error(f"An error occurred fetching the `connections` data: {e}")
            return False
    
    @property
    def local_stratum_incoming_connections(self) -> int | bool:
        """
        The `incoming_connections` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `incoming_connections` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["incoming_connections"])
            return self._local_stratum_cache["incoming_connections"]
        except Exception as e:
            log.error(f"An error occurred fetching the `incoming_connections` data: {e}")
            return False
    
    @property
    def local_stratum_block_reward_share_percent(self) -> int | bool:
        """
        The `block_reward_share_percent` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `block_reward_share_percent` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._local_stratum_cache["block_reward_share_percent"])
            return self._local_stratum_cache["block_reward_share_percent"]
        except Exception as e:
            log.error(f"An error occurred fetching the `block_reward_share_percent` data: {e}")
            return False
    
    @property
    def local_stratum_workers_full(self) -> list | bool:
        """
        The full version of the `workers` data from the `local_stratum` endpoint.

        Returns:
            list | bool: The `workers_full` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._workers_full_cache)
            return self._workers_full_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `workers_full` data: {e}")
            return False

    @property
    def local_stratum_workers(self) -> list | bool:
        """
        The minimal version of the `workers` data from the `local_stratum` endpoint.

        Returns:
            list | bool: The `workers` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            log.debug(self._workers_cache)
            return self._workers_cache
        except Exception as e:
            log.error(f"An error occurred fetching the `workers` data: {e}")
            return False
    
    @property
    def network_stats_difficulty(self) -> int | bool:
        """
        The `difficulty` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `difficulty` data from the `network_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._network_stats_cache["difficulty"])
            return self._network_stats_cache["difficulty"]
        except Exception as e:
            log.error(f"An error occurred fetching the `difficulty` data: {e}")
            return False
    
    @property
    def network_stats_hash(self) -> str | bool:
        """
        The `hash` data from the `network_stats` endpoint.

        Returns:
            str | bool: The `hash` data from the `network_stats` endpoint, False otherwise
        """

        try:
            log.debug(self._network_stats_cache["hash"])
            return self._network_stats_cache["hash"]
        except Exception as e:
            log.error(f"An error occurred fetching the `hash` data: {e}")
            return False
    
    @property
    def network_stats_height(self) -> int | bool:
        """
        The `height` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `height` data from the `network_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._network_stats_cache["height"])
            return self._network_stats_cache["height"]
        except Exception as e:
            log.error(f"An error occurred fetching the `height` data: {e}")
            return False
    
    @property
    def network_stats_reward(self) -> int | bool:
        """
        The `reward` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `reward` data from the `network_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._network_stats_cache["reward"])
            return self._network_stats_cache["reward"]
        except Exception as e:
            log.error(f"An error occurred fetching the `reward` data: {e}")
            return False
    
    @property
    def network_stats_timestamp(self) -> int | bool:
        """
        The `timestamp` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `timestamp` data from the `network_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._network_stats_cache["timestamp"])
            return self._network_stats_cache["timestamp"]
        except Exception as e:
            log.error(f"An error occurred fetching the `timestamp` data: {e}")
            return False
    
    @property
    def pool_blocks_heights(self) -> list | bool:
        """
        The `height` data from the `pool_blocks` endpoint.

        Returns:
            list | bool: The `height` data from the `pool_blocks` endpoint, False otherwise
        """
        try:
            heights = []
            for i in self._pool_blocks_cache:
                heights.append(self._pool_blocks_cache[i]["height"])
            log.debug(heights)
            return heights
        except Exception as e:
            log.error(f"An error occurred fetching the `heights` data: {e}")
            return False
    
    @property
    def pool_blocks_hashes(self) -> list | bool:
        """
        The `hash` data from the `pool_blocks` endpoint.

        Returns:
            list | bool: The `hash` data from the `pool_blocks` endpoint, False otherwise
        """
        try:
            hashes = []
            for i in self._pool_blocks_cache:
                hashes.append(self._pool_blocks_cache[i]["hash"])
            log.debug(hashes)
            return hashes
        except Exception as e:
            log.error(f"An error occurred fetching the `hashes` data: {e}")
            return False
    
    @property
    def pool_blocks_difficulties(self) -> list | bool:
        """
        The `difficulty` data from the `pool_blocks` endpoint.

        Returns:
            list | bool: The `difficulty` data from the `pool_blocks` endpoint, False otherwise
        """
        try:
            difficulties = []
            for i in self._pool_blocks_cache:
                difficulties.append(self._pool_blocks_cache[i]["difficulty"])
            log.debug(difficulties)
            return difficulties
        except Exception as e:
            log.error(f"An error occurred fetching the `difficulties` data: {e}")
            return False
    
    @property
    def pool_blocks_total_hashes(self) -> list | bool:
        """
        The `total_hashes` data from the `pool_blocks` endpoint.

        Returns:
            list | bool: The `total_hashes` data from the `pool_blocks` endpoint, False otherwise
        """
        try:
            total_hashes = []
            for i in self._pool_blocks_cache:
                total_hashes.append(self._pool_blocks_cache[i]["totalHashes"])
            log.debug(total_hashes)
            return total_hashes
        except Exception as e:
            log.error(f"An error occurred fetching the `total_hashes` data: {e}")
            return False
    
    @property
    def pool_blocks_timestamps(self) -> list | bool:
        """
        The `timestamp` data from the `pool_blocks` endpoint.

        Returns:
            list | bool: The `timestamp` data from the `pool_blocks` endpoint, False otherwise
        """
        try:
            timestamps = []
            for i in self._pool_blocks_cache:
                timestamps.append(self._pool_blocks_cache[i]["ts"])
            log.debug(timestamps)
            return timestamps
        except Exception as e:
            log.error(f"An error occurred fetching the `timestamps` data: {e}")
            return False
    
    @property
    def pool_stats_payout_type(self) -> str | bool:
        """
        The `payout_type` data from the `pool_stats` endpoint.

        Returns:
            str | bool: The `payout_type` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_list"][0])
            return self._pool_stats_cache["pool_list"][0]
        except Exception as e:
            log.error(f"An error occurred fetching the `payout_type` data: {e}")
            return False
    
    @property
    def pool_stats_hash_rate(self) -> int | bool:
        """
        The `hashrate` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `hashrate` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["hashRate"])
            return self._pool_stats_cache["pool_statistics"]["hashRate"]
        except Exception as e:
            log.error(f"An error occurred fetching the `hash_rate` data: {e}")
            return False
    
    @property
    def pool_stats_miners(self) -> int | bool:
        """
        The `miners` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `miners` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["miners"])
            return self._pool_stats_cache["pool_statistics"]["miners"]
        except Exception as e:
            log.error(f"An error occurred fetching the `miners` data: {e}")
            return False
    
    @property
    def pool_stats_total_hashes(self) -> int | bool:
        """
        The `total_hashes` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `total_hashes` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["totalHashes"])
            return self._pool_stats_cache["pool_statistics"]["totalHashes"]
        except Exception as e:
            log.error(f"An error occurred fetching the `total_hashes` data: {e}")
            return False
    
    @property
    def pool_stats_last_block_found_time(self) -> int | bool:
        """
        The `last_block_found_time` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `last_block_found_time` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["lastBlockFoundTime"])
            return self._pool_stats_cache["pool_statistics"]["lastBlockFoundTime"]
        except Exception as e:
            log.error(f"An error occurred fetching the `last_block_found_time` data: {e}")
            return False
    
    @property
    def pool_stats_last_block_found(self) -> int | bool:
        """
        The `last_block_found` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `last_block_found` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["lastBlockFound"])
            return self._pool_stats_cache["pool_statistics"]["lastBlockFound"]
        except Exception as e:
            log.error(f"An error occurred fetching the `last_block_found` data: {e}")
            return False
    
    @property
    def pool_stats_total_blocks_found(self) -> int | bool:
        """
        The `total_blocks_found` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `total_blocks_found` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["totalBlocksFound"])
            return self._pool_stats_cache["pool_statistics"]["totalBlocksFound"]
        except Exception as e:
            log.error(f"An error occurred fetching the `total_blocks_found` data: {e}")
            return False
    
    @property
    def pool_stats_pplns_weight(self) -> int | bool:
        """
        The `pplns_weight` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `pplns_weight` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["pplnsWeight"])
            return self._pool_stats_cache["pool_statistics"]["pplnsWeight"]
        except Exception as e:
            log.error(f"An error occurred fetching the `pplns_weight` data: {e}")
            return False
    
    @property
    def pool_stats_pplns_window_size(self) -> int | bool:
        """
        The `pplns_window_size` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `pplns_window_size` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["pplnsWindowSize"])
            return self._pool_stats_cache["pool_statistics"]["pplnsWindowSize"]
        except Exception as e:
            log.error(f"An error occurred fetching the `pplns_window_size` data: {e}")
            return False
    
    @property
    def pool_stats_sidechain_difficulty(self) -> int | bool:
        """
        The `sidechain_difficulty` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `sidechain_difficulty` data from the `pool_stats` endpoint, False otherwise
        """
        
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["sidechainDifficulty"])
            return self._pool_stats_cache["pool_statistics"]["sidechainDifficulty"]
        except Exception as e:
            log.error(f"An error occurred fetching the `sidechain_difficulty` data: {e}")
            return False
    
    @property
    def pool_stats_sidechain_height(self) -> int | bool:
        """
        The `sidechain_height` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `sidechain_height` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            log.debug(self._pool_stats_cache["pool_statistics"]["sidechainHeight"])
            return self._pool_stats_cache["pool_statistics"]["sidechainHeight"]
        except Exception as e:
            log.error(f"An error occurred fetching the `sidechain_height` data: {e}")
            return False
    
    @property
    def stats_mod_config(self) -> dict | bool:
        """
        The `config` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `config` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"])
            return self._stats_mod_cache["config"]
        except Exception as e:
            log.error(f"An error occurred fetching the `config` data: {e}")
            return False
    
    @property
    def stats_mod_ports(self) -> int | bool:
        """
        The `ports` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `ports` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            ports = []
            for i in self._stats_mod_cache["config"]["ports"]:
                ports.append(i["port"])
            log.debug(ports)
            return ports
        except Exception as e:
            log.error(f"An error occurred fetching the `ports` data: {e}")
            return False
    
    @property
    def stats_mod_tls(self) -> bool:
        """
        The `tls` data from the `stats_mod` endpoint.

        Returns:
            bool: The `tls` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            tls = []
            for i in self._stats_mod_cache["config"]["tls"]:
                tls.append(i["port"])
            log.debug(tls)
            return tls
        except Exception as e:
            log.error(f"An error occurred fetching the `tls` data: {e}")
            return False
    
    @property
    def stats_mod_fee(self) -> int | bool:
        """
        The `fee` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `fee` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["fee"])
            return self._stats_mod_cache["config"]["fee"]
        except Exception as e:
            log.error(f"An error occurred fetching the `fee` data: {e}")
            return False
    
    @property
    def stats_mod_min_payment_threshold(self) -> int | bool:
        """
        The `min_payment_threshold` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `min_payment_threshold` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["minPaymentThreshold"])
            return self._stats_mod_cache["config"]["minPaymentThreshold"]
        except Exception as e:
            log.error(f"An error occurred fetching the `min_payment_threshold` data: {e}")
            return False
    
    @property
    def stats_mod_network_height(self) -> int | bool:
        """
        The `network_height` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `network_height` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["network"]["height"])
            return self._stats_mod_cache["config"]["network"]["height"]
        except Exception as e:
            log.error(f"An error occurred fetching the `network_height` data: {e}")
            return False
    
    @property
    def stats_mod_last_block_found(self) -> str | bool:
        """
        The `last_block_found` data from the `stats_mod` endpoint.

        Returns:
            str | bool: The `last_block_found` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["pool"]["stats"]["lastBlockFound"])
            return self._stats_mod_cache["config"]["pool"]["stats"]["lastBlockFound"]
        except Exception as e:
            log.error(f"An error occurred fetching the `last_block_found` data: {e}")
            return False
    
    @property
    def stats_mod_blocks(self) -> list | bool:
        """
        The `blocks` data from the `stats_mod` endpoint.

        Returns:
            list | bool: The `blocks` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["pool"]["stats"]["blocks"])
            return self._stats_mod_cache["config"]["pool"]["stats"]["blocks"]
        except Exception as e:
            log.error(f"An error occurred fetching the `blocks` data: {e}")
            return False
    
    @property
    def stats_mod_miners(self) -> int | bool:
        """
        The `miners` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `miners` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["pool"]["stats"]["miners"])
            return self._stats_mod_cache["config"]["pool"]["stats"]["miners"]
        except Exception as e:
            log.error(f"An error occurred fetching the `miners` data: {e}")
            return False
    
    @property
    def stats_mod_hashrate(self) -> int | bool:
        """
        The `hashrate` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `hashrate` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["pool"]["stats"]["hashrate"])
            return self._stats_mod_cache["config"]["pool"]["stats"]["hashrate"]
        except Exception as e:
            log.error(f"An error occurred fetching the `hashrate` data: {e}")
            return False
    
    @property
    def stats_mod_round_hashes(self) -> int | bool:
        """
        The `round_hashes` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `round_hashes` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            log.debug(self._stats_mod_cache["config"]["pool"]["stats"]["roundHashes"])
            return self._stats_mod_cache["config"]["pool"]["stats"]["roundHashes"]
        except Exception as e:
            log.error(f"An error occurred fetching the `round_hashes` data: {e}")
            return False

# Define the public interface of the module
__all__ = ["P2PoolAPI"]
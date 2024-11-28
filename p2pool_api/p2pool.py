"""
P2Pool API interaction library.

This module provides the `P2PoolAPI` class for interacting with various data sources in a P2Pool miner API.
"""

import json


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

    def __init__(self, api_path: str):
        """
        Initializes a P2PoolAPI instance.

        Args:
            api_path (str): The base path to the API data directory.
        """
        self._api_path = api_path
        self._local_console = {}
        self._local_p2p = {}
        self._local_stratum = {}
        self._workers_full = {}
        self._workers = {}
        self._network_stats = {}
        self._pool_blocks = {}
        self._pool_stats = {}
        self._stats_mod = {}
        self.get_all_data()

    def get_local_console(self) -> bool:
        """
        Loads data from the `local/console` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/local/console", "r") as reader:
                self._local_console = json.loads(reader.read())
            return True
        except Exception as e:
            print(f"An error occurred opening the `local_console` file: {e}")
            return False

    def get_local_p2p(self) -> bool:
        """
        Loads data from the `local/p2p` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/local/p2p", "r") as reader:
                self._local_p2p = json.loads(reader.read())
            return True
        except Exception as e:
            print(f"An error occurred opening the `local_p2p` file: {e}")
            return False

    def get_local_stratum(self) -> bool:
        """
        Loads data from the `local/stratum` API endpoint and processes worker data.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/local/stratum", "r") as reader:
                self._local_stratum = json.loads(reader.read())
            self._workers_full = self._local_stratum["workers"]
            self._workers = []
            for w in self._workers_full:
                w_list = w.split(",")
                self._workers.append(w_list)
            self._workers = sorted(self._workers, key=lambda x: int(x[3]), reverse=True)
            return True
        except Exception as e:
            print(f"An error occurred opening the `local_stratum` file: {e}")
            return False

    def get_network_stats(self) -> bool:
        """
        Loads data from the `network/stats` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/network/stats", "r") as reader:
                self._network_stats = json.loads(reader.read())
            return True
        except Exception as e:
            print(f"An error occurred opening the `network_stats` file: {e}")
            return False

    def get_pool_blocks(self) -> bool:
        """
        Loads data from the `pool/blocks` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/pool/blocks", "r") as reader:
                self._pool_blocks = json.loads(reader.read())
            return True
        except Exception as e:
            print(f"An error occurred opening the `pool_blocks` file: {e}")
            return False

    def get_pool_stats(self) -> bool:
        """
        Loads data from the `pool/stats` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/pool/stats", "r") as reader:
                self._pool_stats = json.loads(reader.read())
            return True
        except Exception as e:
            print(f"An error occurred opening the `pool_stats` file: {e}")
            return False

    def get_stats_mod(self) -> bool:
        """
        Loads data from the `stats_mod` API endpoint.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            with open(f"{self._api_path}/stats_mod", "r") as reader:
                self._stats_mod = json.loads(reader.read())
            return True
        except Exception as e:
            print(f"An error occurred opening the `stats_mod` file: {e}")
            return False

    def get_all_data(self) -> bool:
        """
        Fetches and processes data from all API endpoints.

        Returns:
            bool: True if all data sources were successfully fetched, False otherwise.
        """
        try:
            self.get_local_console()
            self.get_local_p2p()
            self.get_local_stratum()
            self.get_network_stats()
            self.get_pool_blocks()
            self.get_pool_stats()
            self.get_stats_mod()
            return True
        except Exception as e:
            print(f"An error occurred fetching the latest data: {e}")
            return False

    @property
    def local_console(self) -> dict | bool:
        """
        The data from the `local/console` endpoint.

        Returns:
            dict |: The data from the `local/console` endpoint, False otherwise
        """
        return self._local_console

    @property
    def local_p2p(self) -> dict | bool:
        """
        The data from the `local/p2p` endpoint.

        Returns:
            dict |: The data from the `local/p2p` endpoint, False otherwise
        """
        return self._local_p2p

    @property
    def local_stratum(self) -> dict | bool:
        """
        The data from the `local/stratum` endpoint.

        Returns:
            dict |: The data from the `local/stratum` endpoint, False otherwise
        """
        return self._local_stratum

    @property
    def network_stats(self) -> dict | bool:
        """
        The data from the `network/stats` endpoint.

        Returns:
            dict |: The data from the `network/stats` endpoint, False otherwise
        """
        return self._network_stats

    @property
    def pool_blocks(self) -> dict | bool:
        """
        The data from the `pool/blocks` endpoint.

        Returns:
            dict |: The data from the `pool/blocks` endpoint, False otherwise
        """
        return self._pool_blocks

    @property
    def pool_stats(self) -> dict | bool:
        """
        The data from the `pool/stats` endpoint.

        Returns:
            dict |: The data from the `pool/stats` endpoint, False otherwise
        """
        return self._pool_stats

    @property
    def stats_mod(self) -> dict | bool:
        """
        The data from the `stats_mod` endpoint.

        Returns:
            dict |: The data from the `stats_mod` endpoint, False otherwise
        """
        return self._stats_mod
    
    @property
    def local_console_mode(self) -> str | bool:
        """
        The `mode` data from the `local_console` endpoint.

        Returns:
            str | bool: The `mode` data from the `local_console` endpoint, False otherwise
        """
        try:
            return self._local_console["mode"]
        except Exception as e:
            print(f"An error occurred fetching the `mode` data: {e}")
            return False
    
    @property
    def local_console_tcp_port(self) -> str | bool:
        """
        The `tcp_port` data from the `local_console` endpoint.

        Returns:
            str | bool: The `tcp_port` data from the `local_console` endpoint, False otherwise
        """
        try:
            return self._local_console["tcp_port"]
        except Exception as e:
            print(f"An error occurred fetching the `tcp_port` data: {e}")
            return False
    
    @property
    def local_p2p_connections(self) -> int | bool:
        """
        The `connections` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `connections` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            return self._local_p2p["connections"]
        except Exception as e:
            print(f"An error occurred fetching the `connections` data: {e}")
            return False
    
    @property
    def local_p2p_incoming_connections(self) -> int | bool:
        """
        The `incoming_connections` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `incoming_connections` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            return self._local_p2p["incoming_connections"]
        except Exception as e:
            print(f"An error occurred fetching the `incoming_connections` data: {e}")
            return False
    
    @property
    def local_p2p_peer_list_size(self) -> int | bool:
        """
        The `peer_list_size` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `peer_list_size` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            return self._local_p2p["peer_list_size"]
        except Exception as e:
            print(f"An error occurred fetching the `peer_list_size` data: {e}")
            return False
    
    @property
    def local_p2p_peers(self) -> list | bool:
        """
        The `peers` data from the `local_p2p` endpoint.

        Returns:
            list | bool: The `peers` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            return self._local_p2p["peers"]
        except Exception as e:
            print(f"An error occurred fetching the `peers` data: {e}")
            return False
    
    @property
    def local_p2p_uptime(self) -> int | bool:
        """
        The `uptime` data from the `local_p2p` endpoint.

        Returns:
            int | bool: The `uptime` data from the `local_p2p` endpoint, False otherwise
        """
        try:
            return self._local_p2p["uptime"]
        except Exception as e:
            print(f"An error occurred fetching the `uptime` data: {e}")
            return False
    
    @property
    def local_stratum_hashrate_15m(self) -> int | bool:
        """
        The `hashrate_15m` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `hashrate_15m` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["hashrate_15m"]
        except Exception as e:
            print(f"An error occurred fetching the `hashrate_15m` data: {e}")
            return False
    
    @property
    def local_stratum_hashrate_1h(self) -> int | bool:
        """
        The `hashrate_1h` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `hashrate_1h` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["hashrate_1h"]
        except Exception as e:
            print(f"An error occurred fetching the `hashrate_1h` data: {e}")
            return False
    
    @property
    def local_stratum_hashrate_24h(self) -> int | bool:
        """
        The `hashrate_24h` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `hashrate_24h` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["hashrate_24h"]
        except Exception as e:
            print(f"An error occurred fetching the `hashrate_24h` data: {e}")
            return False
    
    @property
    def local_stratum_total_hashes(self) -> int | bool:
        """
        The `total_hashes` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `total_hashes` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["total_hashes"]
        except Exception as e:
            print(f"An error occurred fetching the `total_hashes` data: {e}")
            return False
    
    @property
    def local_stratum_shares_found(self) -> int | bool:
        """
        The `shares_found` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `shares_found` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["shares_found"]
        except Exception as e:
            print(f"An error occurred fetching the `shares_found` data: {e}")
            return False
    
    @property
    def local_stratum_shares_failed(self) -> int | bool:
        """
        The `shares_failed` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `shares_failed` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["shares_failed"]
        except Exception as e:
            print(f"An error occurred fetching the `shares_failed` data: {e}")
            return False
    
    @property
    def local_stratum_average_effort(self) -> int | bool:
        """
        The `average_effort` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `average_effort` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["average_effort"]
        except Exception as e:
            print(f"An error occurred fetching the `average_effort` data: {e}")
            return False
    
    @property
    def local_stratum_current_effort(self) -> int | bool:
        """
        The `current_effort` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `current_effort` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["current_effort"]
        except Exception as e:
            print(f"An error occurred fetching the `current_effort` data: {e}")
            return False
    
    @property
    def local_stratum_connections(self) -> int | bool:
        """
        The `connections` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `connections` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["connections"]
        except Exception as e:
            print(f"An error occurred fetching the `connections` data: {e}")
            return False
    
    @property
    def local_stratum_incoming_connections(self) -> int | bool:
        """
        The `incoming_connections` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `incoming_connections` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["incoming_connections"]
        except Exception as e:
            print(f"An error occurred fetching the `incoming_connections` data: {e}")
            return False
    
    @property
    def local_stratum_block_reward_share_percent(self) -> int | bool:
        """
        The `block_reward_share_percent` data from the `local_stratum` endpoint.

        Returns:
            int | bool: The `block_reward_share_percent` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            return self._local_stratum["block_reward_share_percent"]
        except Exception as e:
            print(f"An error occurred fetching the `block_reward_share_percent` data: {e}")
            return False
    
    @property
    def local_stratum_workers(self, default: bool = True) -> list | bool:
        """
        The `workers` data from the `local_stratum` endpoint.

        Returns:
            list | bool: The `workers` data from the `local_stratum` endpoint, False otherwise
        """
        try:
            if default == False:
                return self._workers_full
            return self._workers
        except Exception as e:
            if default != "default":
                print(f"An error occurred fetching the `workers_full` data: {e}")
            else:
                print(f"An error occurred fetching the `workers` data: {e}")
            return False
    
    @property
    def network_stats_difficulty(self) -> int | bool:
        """
        The `difficulty` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `difficulty` data from the `network_stats` endpoint, False otherwise
        """
        try:
            return self._network_stats["difficulty"]
        except Exception as e:
            print(f"An error occurred fetching the `difficulty` data: {e}")
            return False
    
    @property
    def network_stats_hash(self) -> str | bool:
        """
        The `hash` data from the `network_stats` endpoint.

        Returns:
            str | bool: The `hash` data from the `network_stats` endpoint, False otherwise
        """

        try:
            return self._network_stats["hash"]
        except Exception as e:
            print(f"An error occurred fetching the `hash` data: {e}")
            return False
    
    @property
    def network_stats_height(self) -> int | bool:
        """
        The `height` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `height` data from the `network_stats` endpoint, False otherwise
        """
        try:
            return self._network_stats["height"]
        except Exception as e:
            print(f"An error occurred fetching the `height` data: {e}")
            return False
    
    @property
    def network_stats_reward(self) -> int | bool:
        """
        The `reward` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `reward` data from the `network_stats` endpoint, False otherwise
        """
        try:
            return self._network_stats["reward"]
        except Exception as e:
            print(f"An error occurred fetching the `reward` data: {e}")
            return False
    
    @property
    def network_stats_timestamp(self) -> int | bool:
        """
        The `timestamp` data from the `network_stats` endpoint.

        Returns:
            int | bool: The `timestamp` data from the `network_stats` endpoint, False otherwise
        """
        try:
            return self._network_stats["timestamp"]
        except Exception as e:
            print(f"An error occurred fetching the `timestamp` data: {e}")
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
            for i in self._pool_blocks:
                heights.append(self._pool_blocks[i]["height"])
            return heights
        except Exception as e:
            print(f"An error occurred fetching the `heights` data: {e}")
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
            for i in self._pool_blocks:
                hashes.append(self._pool_blocks[i]["hash"])
            return hashes
        except Exception as e:
            print(f"An error occurred fetching the `hashes` data: {e}")
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
            for i in self._pool_blocks:
                difficulties.append(self._pool_blocks[i]["difficulty"])
            return difficulties
        except Exception as e:
            print(f"An error occurred fetching the `difficulties` data: {e}")
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
            for i in self._pool_blocks:
                total_hashes.append(self._pool_blocks[i]["totalHashes"])
            return total_hashes
        except Exception as e:
            print(f"An error occurred fetching the `total_hashes` data: {e}")
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
            for i in self._pool_blocks:
                timestamps.append(self._pool_blocks[i]["ts"])
            return timestamps
        except Exception as e:
            print(f"An error occurred fetching the `timestamps` data: {e}")
            return False
    
    @property
    def pool_stats_payout_type(self) -> str | bool:
        """
        The `payout_type` data from the `pool_stats` endpoint.

        Returns:
            str | bool: The `payout_type` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_list"][0]
        except Exception as e:
            print(f"An error occurred fetching the `payout_type` data: {e}")
            return False
    
    @property
    def pool_stats_hash_rate(self) -> int | bool:
        """
        The `hashrate` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `hashrate` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["hashRate"]
        except Exception as e:
            print(f"An error occurred fetching the `hash_rate` data: {e}")
            return False
    
    @property
    def pool_stats_miners(self) -> int | bool:
        """
        The `miners` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `miners` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["miners"]
        except Exception as e:
            print(f"An error occurred fetching the `miners` data: {e}")
            return False
    
    @property
    def pool_stats_total_hashes(self) -> int | bool:
        """
        The `total_hashes` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `total_hashes` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["totalHashes"]
        except Exception as e:
            print(f"An error occurred fetching the `total_hashes` data: {e}")
            return False
    
    @property
    def pool_stats_last_block_found_time(self) -> int | bool:
        """
        The `last_block_found_time` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `last_block_found_time` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["lastBlockFoundTime"]
        except Exception as e:
            print(f"An error occurred fetching the `last_block_found_time` data: {e}")
            return False
    
    @property
    def pool_stats_last_block_found(self) -> int | bool:
        """
        The `last_block_found` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `last_block_found` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["lastBlockFound"]
        except Exception as e:
            print(f"An error occurred fetching the `last_block_found` data: {e}")
            return False
    
    @property
    def pool_stats_total_blocks_found(self) -> int | bool:
        """
        The `total_blocks_found` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `total_blocks_found` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["totalBlocksFound"]
        except Exception as e:
            print(f"An error occurred fetching the `total_blocks_found` data: {e}")
            return False
    
    @property
    def pool_stats_pplns_weight(self) -> int | bool:
        """
        The `pplns_weight` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `pplns_weight` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["pplnsWeight"]
        except Exception as e:
            print(f"An error occurred fetching the `pplns_weight` data: {e}")
            return False
    
    @property
    def pool_stats_pplns_window_size(self) -> int | bool:
        """
        The `pplns_window_size` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `pplns_window_size` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["pplnsWindowSize"]
        except Exception as e:
            print(f"An error occurred fetching the `pplns_window_size` data: {e}")
            return False
    
    @property
    def pool_stats_sidechain_difficulty(self) -> int | bool:
        """
        The `sidechain_difficulty` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `sidechain_difficulty` data from the `pool_stats` endpoint, False otherwise
        """
        
        try:
            return self._pool_stats["pool_statistics"]["sidechainDifficulty"]
        except Exception as e:
            print(f"An error occurred fetching the `sidechain_difficulty` data: {e}")
            return False
    
    @property
    def pool_stats_sidechain_height(self) -> int | bool:
        """
        The `sidechain_height` data from the `pool_stats` endpoint.

        Returns:
            int | bool: The `sidechain_height` data from the `pool_stats` endpoint, False otherwise
        """
        try:
            return self._pool_stats["pool_statistics"]["sidechainHeight"]
        except Exception as e:
            print(f"An error occurred fetching the `sidechain_height` data: {e}")
            return False
    
    @property
    def stats_mod_config(self) -> dict | bool:
        """
        The `config` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `config` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]
        except Exception as e:
            print(f"An error occurred fetching the `config` data: {e}")
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
            for i in self._stats_mod["config"]["ports"]:
                ports.append(i["port"])
            return ports
        except Exception as e:
            print(f"An error occurred fetching the `ports` data: {e}")
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
            for i in self._stats_mod["config"]["tls"]:
                tls.append(i["port"])
            return tls
        except Exception as e:
            print(f"An error occurred fetching the `tls` data: {e}")
            return False
    
    @property
    def stats_mod_fee(self) -> int | bool:
        """
        The `fee` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `fee` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["fee"]
        except Exception as e:
            print(f"An error occurred fetching the `fee` data: {e}")
            return False
    
    @property
    def stats_mod_min_payment_threshold(self) -> int | bool:
        """
        The `min_payment_threshold` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `min_payment_threshold` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["minPaymentThreshold"]
        except Exception as e:
            print(f"An error occurred fetching the `min_payment_threshold` data: {e}")
            return False
    
    @property
    def stats_mod_network_height(self) -> int | bool:
        """
        The `network_height` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `network_height` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["network"]["height"]
        except Exception as e:
            print(f"An error occurred fetching the `network_height` data: {e}")
            return False
    
    @property
    def stats_mod_last_block_found(self) -> str | bool:
        """
        The `last_block_found` data from the `stats_mod` endpoint.

        Returns:
            str | bool: The `last_block_found` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["pool"]["stats"]["lastBlockFound"]
        except Exception as e:
            print(f"An error occurred fetching the `last_block_found` data: {e}")
            return False
    
    @property
    def stats_mod_blocks(self) -> list | bool:
        """
        The `blocks` data from the `stats_mod` endpoint.

        Returns:
            list | bool: The `blocks` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["pool"]["stats"]["blocks"]
        except Exception as e:
            print(f"An error occurred fetching the `blocks` data: {e}")
            return False
    
    @property
    def stats_mod_miners(self) -> int | bool:
        """
        The `miners` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `miners` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["pool"]["stats"]["miners"]
        except Exception as e:
            print(f"An error occurred fetching the `miners` data: {e}")
            return False
    
    @property
    def stats_mod_hashrate(self) -> int | bool:
        """
        The `hashrate` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `hashrate` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["pool"]["stats"]["hashrate"]
        except Exception as e:
            print(f"An error occurred fetching the `hashrate` data: {e}")
            return False
    
    @property
    def stats_mod_round_hashes(self) -> int | bool:
        """
        The `round_hashes` data from the `stats_mod` endpoint.

        Returns:
            int | bool: The `round_hashes` data from the `stats_mod` endpoint, False otherwise
        """
        try:
            return self._stats_mod["config"]["pool"]["stats"]["roundHashes"]
        except Exception as e:
            print(f"An error occurred fetching the `round_hashes` data: {e}")
            return False
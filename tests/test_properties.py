import unittest, json
from unittest.mock import patch
from p2pool.api import P2PoolAPI
from pathlib import Path

class TestP2PoolAPIProperties(unittest.TestCase):

    @patch('p2pool.api.P2PoolAPI.update_all_endpoints', return_value=True)
    def setUp(self, mock_update_all_endpoints):
        self.local_path = Path("api/").resolve()
        self.api = P2PoolAPI(self.local_path)
        with open("api/local/console", "rb") as f:
            self.local_console = json.loads(f.read())
        with open("api/local/p2p", "rb") as f:
            self.local_p2p = json.loads(f.read())
        with open("api/local/stratum", "rb") as f:
            self.local_stratum = json.loads(f.read())
        with open("api/network/stats", "rb") as f:
            self.network_stats = json.loads(f.read())
        with open("api/pool/blocks", "rb") as f:
            self.pool_blocks = json.loads(f.read())
        with open("api/pool/stats", "rb") as f:
            self.pool_stats = json.loads(f.read())
        with open("api/stats_mod", "rb") as f:
            self.stats_mod = json.loads(f.read())
        self.api._local_console_cache = self.local_console
        self.api._local_p2p_cache = self.local_p2p
        self.api._local_stratum_cache = self.local_stratum
        self.api._network_stats_cache = self.network_stats
        self.api._pool_blocks_cache = self.pool_blocks
        self.api._pool_stats_cache = self.pool_stats
        self.api._stats_mod_cache = self.stats_mod
        self.local_console_table_name = "console"
        self.local_p2p_table_name = "p2p"
        self.local_stratum_table_name = "stratum"
        self.network_stats_table_name = "network_stats"
        self.pool_blocks_table_name = "pool_blocks"
        self.pool_stats_table_name = "pool_stats"
        self.stats_mod_table_name = "stats_mod"

    # Test all available property getters
    def test_local_console(self):
        self.assertEqual(self.api.local_console, self.local_console)

    def test_local_p2p(self):
        self.assertEqual(self.api.local_p2p, self.local_p2p)

    def test_local_stratum(self):
        self.assertEqual(self.api.local_stratum, self.local_stratum)
 
    def test_network_stats(self):
        self.assertEqual(self.api.network_stats, self.network_stats)

    def test_pool_blocks(self):
        self.assertEqual(self.api.pool_blocks, self.pool_blocks)

    def test_pool_stats(self):
        self.assertEqual(self.api.pool_stats, self.pool_stats)

    def test_stats_mod(self):
        self.assertEqual(self.api.stats_mod, self.stats_mod)
    
    def test_local_console_mode(self):
        self.assertEqual(self.api.local_console_mode, self.local_console["mode"])
    
    def test_local_console_tcp_port(self):
        self.assertEqual(self.api.local_console_tcp_port, self.local_console["tcp_port"])
    
    def test_local_p2p_connections(self):
        self.assertEqual(self.api.local_p2p_connections, self.local_p2p["connections"])
    
    def test_local_p2p_incoming_connections(self):
        self.assertEqual(self.api.local_p2p_incoming_connections, self.local_p2p["incoming_connections"])

    def test_local_p2p_peer_list_size(self):
        self.assertEqual(self.api.local_p2p_peer_list_size, self.local_p2p["peer_list_size"])

    def test_local_p2p_peers(self):
        self.assertEqual(self.api.local_p2p_peers, self.local_p2p["peers"])

    def test_local_p2p_uptime(self):
        self.assertEqual(self.api.local_p2p_uptime, self.local_p2p["uptime"])

    def test_local_stratum_hashrate_15m(self):
        self.assertEqual(self.api.local_stratum_hashrate_15m, self.local_stratum["hashrate_15m"])

    def test_local_stratum_hashrate_1h(self):
        self.assertEqual(self.api.local_stratum_hashrate_1h, self.local_stratum["hashrate_1h"])
    
    def test_local_stratum_hashrate_24h(self):
        self.assertEqual(self.api.local_stratum_hashrate_24h, self.local_stratum["hashrate_24h"])
    
    def test_local_stratum_total_hashes(self):
        self.assertEqual(self.api.local_stratum_total_hashes, self.local_stratum["total_hashes"])
    
    def test_local_stratum_shares_found(self):
        self.assertEqual(self.api.local_stratum_shares_found, self.local_stratum["shares_found"])
    
    def test_local_stratum_shares_failed(self):
        self.assertEqual(self.api.local_stratum_shares_failed, self.local_stratum["shares_failed"])
    
    def test_local_stratum_average_effort(self):
        self.assertEqual(self.api.local_stratum_average_effort, self.local_stratum["average_effort"])
    
    def test_local_stratum_current_effort(self):
        self.assertEqual(self.api.local_stratum_current_effort, self.local_stratum["current_effort"])
    
    def test_local_stratum_connections(self):
        self.assertEqual(self.api.local_stratum_connections, self.local_stratum["connections"])
    
    def test_local_stratum_incoming_connections(self):
        self.assertEqual(self.api.local_stratum_incoming_connections, self.local_stratum["incoming_connections"])

    def test_local_stratum_block_reward_share_percent(self):
        self.assertEqual(self.api.local_stratum_block_reward_share_percent, self.local_stratum["block_reward_share_percent"])
    
    def test_local_stratum_workers_full(self):
        self.assertEqual(self.api.local_stratum_workers_full, self.local_stratum["workers"])
    
    def test_local_stratum_workers_short(self):
        workers = self.local_stratum["workers"]
        expected_result = [w.split(",") for w in workers]
        expected_result = sorted(expected_result, key=lambda x: int(x[3]), reverse=True)
        self.assertEqual(self.api.local_stratum_workers_short, expected_result)
    
    def test_network_stats_difficulty(self):
        self.assertEqual(self.api.network_stats_difficulty, self.network_stats["difficulty"])
    
    def test_network_stats_hash(self):
        self.assertEqual(self.api.network_stats_hash, self.network_stats["hash"])
    
    def test_network_stats_height(self):
        self.assertEqual(self.api.network_stats_height, self.network_stats["height"])
    
    def test_network_stats_reward(self):
        self.assertEqual(self.api.network_stats_reward, self.network_stats["reward"])
    
    def test_network_stats_timestamp(self):
        self.assertEqual(self.api.network_stats_timestamp, self.network_stats["timestamp"])
    
    def test_pool_blocks_heights(self):
        self.assertEqual(self.api.pool_blocks_heights, [3342543,3342019,3341883])
    
    def test_pool_blocks_hashes(self):
        self.assertEqual(self.api.pool_blocks_hashes, ["a69b17b703b3987e758daf1740e620b56f52c8832ccc5f5ae6487b7f6e89f133","2d0ee9e27f7ae5a69f519d37242c260abe86cc264d9e110797d34ef2e4e1f42f","4a01b3d1e6f1975062cdf791fe248a6fc574706638f4bb59678589f5df29518f"])
    
    def test_pool_blocks_difficulty(self):
        self.assertEqual(self.api.pool_blocks_difficulties, [479248644548,471876229336,461749623245])

    def test_pool_blocks_total_hashes(self):
        self.assertEqual(self.api.pool_blocks_total_hashes, [1223001183570723,1221984298441455,1221701792894747])
    
    def test_pool_blocks_timestamps(self):
        self.assertEqual(self.api.pool_blocks_timestamps, [1738945363,1738886710,1738869067])
    
    def test_pool_stats_pool_list(self):
        self.assertEqual(self.api.pool_stats_pool_list, self.pool_stats["pool_list"])

    def test_pool_stats_payout_type(self):
        self.assertEqual(self.api.pool_stats_payout_type, self.pool_stats["pool_list"][0])

    def test_pool_stats_pool_statistics(self):
        self.assertEqual(self.api.pool_stats_pool_statistics, self.pool_stats["pool_statistics"])

    def test_pool_stats_hashrate(self):
        self.assertEqual(self.api.pool_stats_hashrate, self.pool_stats["pool_statistics"]["hashRate"])

    def test_pool_stats_miners(self):
        self.assertEqual(self.api.pool_stats_miners, self.pool_stats["pool_statistics"]["miners"])

    def test_pool_stats_total_hashes(self):
        self.assertEqual(self.api.pool_stats_total_hashes, self.pool_stats["pool_statistics"]["totalHashes"])

    def test_pool_stats_last_block_found_time(self):
        self.assertEqual(self.api.pool_stats_last_block_found_time, self.pool_stats["pool_statistics"]["lastBlockFoundTime"])

    def test_pool_stats_last_block_found(self):
        self.assertEqual(self.api.pool_stats_last_block_found, self.pool_stats["pool_statistics"]["lastBlockFound"])

    def test_pool_stats_total_blocks_found(self):
        self.assertEqual(self.api.pool_stats_total_blocks_found, self.pool_stats["pool_statistics"]["totalBlocksFound"])

    def test_pool_stats_pplns_weight(self):
        self.assertEqual(self.api.pool_stats_pplns_weight, self.pool_stats["pool_statistics"]["pplnsWeight"])

    def test_pool_stats_pplns_window_size(self):
        self.assertEqual(self.api.pool_stats_pplns_window_size, self.pool_stats["pool_statistics"]["pplnsWindowSize"])

    def test_pool_stats_sidechain_difficulty(self):
        self.assertEqual(self.api.pool_stats_sidechain_difficulty, self.pool_stats["pool_statistics"]["sidechainDifficulty"])

    def test_pool_stats_sidechain_height(self):
        self.assertEqual(self.api.pool_stats_sidechain_height, self.pool_stats["pool_statistics"]["sidechainHeight"])

    def test_stats_mod_config(self):
        self.assertEqual(self.api.stats_mod_config, self.stats_mod["config"])

    def test_stats_mod_ports(self):
        self.assertEqual(self.api.stats_mod_ports, self.stats_mod["config"]["ports"])

    def test_stats_mod_port_values(self):
        self.assertEqual(self.api.stats_mod_port_values, [3333])

    def test_stats_mod_tls(self):
        self.assertEqual(self.api.stats_mod_tls, [False])

    def test_stats_mod_fee(self):
        self.assertEqual(self.api.stats_mod_fee, self.stats_mod["config"]["fee"])

    def test_stats_mod_min_payment_threshold(self):
        self.assertEqual(self.api.stats_mod_min_payment_threshold, self.stats_mod["config"]["minPaymentThreshold"])

    def test_stats_mod_network(self):
        self.assertEqual(self.api.stats_mod_network, self.stats_mod["network"])

    def test_stats_mod_network_height(self):
        self.assertEqual(self.api.stats_mod_network_height, self.stats_mod["network"]["height"])

    def test_stats_mod_pool(self):
        self.assertEqual(self.api.stats_mod_pool, self.stats_mod["pool"])

    def test_stats_mod_pool_stats(self):
        self.assertEqual(self.api.stats_mod_pool_stats, self.stats_mod["pool"]["stats"])

    def test_stats_mod_last_block_found(self):
        self.assertEqual(self.api.stats_mod_last_block_found, self.stats_mod["pool"]["stats"]["lastBlockFound"])

    def test_stats_mod_blocks(self):
        self.assertEqual(self.api.stats_mod_blocks, self.stats_mod["pool"]["blocks"])

    def test_stats_mod_miners(self):
        self.assertEqual(self.api.stats_mod_miners, self.stats_mod["pool"]["miners"])

    def test_stats_mod_hashrate(self):
        self.assertEqual(self.api.stats_mod_hashrate, self.stats_mod["pool"]["hashrate"])

    def test_stats_mod_round_hashes(self):
        self.assertEqual(self.api.stats_mod_round_hashes, self.stats_mod["pool"]["roundHashes"])

if __name__ == '__main__':
    unittest.main()

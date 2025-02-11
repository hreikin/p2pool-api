import unittest
from unittest.mock import patch, MagicMock
from p2pool.api import P2PoolAPI
from pathlib import Path
from unittest.mock import call

# TODO: Needs fixing to not show the 404 error.

class TestP2PoolAPI(unittest.TestCase):

    @patch('p2pool.api.P2PoolAPI.update_all_endpoints', return_value=True)
    def setUp(self, mock_update_all_endpoints):
        self.local_path = Path("api/").resolve()
        self.remote_path = "http://example.com/api"
        self.local_api = P2PoolAPI(self.local_path)
        self.remote_api = P2PoolAPI(self.remote_path, True)

    @patch('p2pool.db.P2PoolDatabase._init_db')
    def test_init_local(self, mock_init_db):
        api = P2PoolAPI(self.local_path)
        self.assertEqual(api._api_path, self.local_path)
        self.assertFalse(api._is_remote)
        self.assertEqual(api._db_url, "sqlite:///p2pool.db")
        mock_init_db.assert_called_once_with("sqlite:///p2pool.db")
    
    @patch('p2pool.db.P2PoolDatabase._init_db')
    @patch('requests.get')
    def test_init_remote(self, mock_get, mock_init_db):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}  # Ensure this is a serializable dictionary
        mock_get.return_value = mock_response

        api = P2PoolAPI(self.remote_path, True)
        self.assertEqual(api._api_path, self.remote_path)
        self.assertTrue(api._is_remote)
        self.assertEqual(api._db_url, "sqlite:///p2pool.db")
        mock_init_db.assert_called_once_with("sqlite:///p2pool.db")

        expected_calls = [
            call(f"{self.remote_path}/local/console"),
            call(f"{self.remote_path}/local/p2p"),
            call(f"{self.remote_path}/local/stratum"),
            call(f"{self.remote_path}/network/stats"),
            call(f"{self.remote_path}/pool/blocks"),
            call(f"{self.remote_path}/pool/stats"),
            call(f"{self.remote_path}/stats_mod"),
        ]
        mock_get.assert_has_calls(expected_calls, any_order=True)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"key": "value"}')
    def test_fetch_data_local(self, mock_open):
        data = self.local_api._fetch_data("endpoint")
        self.assertEqual(data, {"key": "value"})
        mock_open.assert_called_once_with(f"{self.local_path}/endpoint", "r")

    @patch('requests.get')
    def test_fetch_data_remote(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response
        data = self.remote_api._fetch_data("endpoint")
        self.assertEqual(data, {"key": "value"})
        mock_get.assert_called_once_with(f"{self.remote_path}/endpoint")

    @patch('p2pool.db.P2PoolDatabase._insert_data_into_db')
    @patch('p2pool.api.P2PoolAPI._fetch_data')
    def test_get_endpoint_local(self, mock_fetch_data, mock_insert_data):
        mock_fetch_data.return_value = {"key": "value"}
        result = self.local_api._get_endpoint("local/console")
        self.assertTrue(result)
        self.assertEqual(self.local_api._local_console_cache, {"key": "value"})
        mock_insert_data.assert_called_once_with({"key": "value"}, "local/console", "sqlite:///p2pool.db")
    
    @patch('p2pool.db.P2PoolDatabase._insert_data_into_db')
    @patch('p2pool.api.P2PoolAPI._fetch_data')
    def test_get_endpoint_remote(self, mock_fetch_data, mock_insert_data):
        mock_fetch_data.return_value = {"key": "value"}
        result = self.remote_api._get_endpoint("local/console")
        self.assertTrue(result)
        self.assertEqual(self.remote_api._local_console_cache, {"key": "value"})
        mock_insert_data.assert_called_once_with({"key": "value"}, "local/console", "sqlite:///p2pool.db")

    @patch('p2pool.api.P2PoolAPI.update_local_console')
    @patch('p2pool.api.P2PoolAPI.update_local_p2p')
    @patch('p2pool.api.P2PoolAPI.update_local_stratum')
    @patch('p2pool.api.P2PoolAPI.update_network_stats')
    @patch('p2pool.api.P2PoolAPI.update_pool_blocks')
    @patch('p2pool.api.P2PoolAPI.update_pool_stats')
    @patch('p2pool.api.P2PoolAPI.update_stats_mod')
    def test_update_all_endpoints_local(self, mock_update_stats_mod, mock_update_pool_stats, mock_update_pool_blocks, mock_update_network_stats, mock_update_local_stratum, mock_update_local_p2p, mock_update_local_console):
        mock_update_local_console.return_value = True
        mock_update_local_p2p.return_value = True
        mock_update_local_stratum.return_value = True
        mock_update_network_stats.return_value = True
        mock_update_pool_blocks.return_value = True
        mock_update_pool_stats.return_value = True
        mock_update_stats_mod.return_value = True
        result = self.local_api.update_all_endpoints()
        self.assertTrue(result)
        mock_update_local_console.assert_called_once()
        mock_update_local_p2p.assert_called_once()
        mock_update_local_stratum.assert_called_once()
        mock_update_network_stats.assert_called_once()
        mock_update_pool_blocks.assert_called_once()
        mock_update_pool_stats.assert_called_once()
        mock_update_stats_mod.assert_called_once()

    @patch('p2pool.api.P2PoolAPI.update_local_console')
    @patch('p2pool.api.P2PoolAPI.update_local_p2p')
    @patch('p2pool.api.P2PoolAPI.update_local_stratum')
    @patch('p2pool.api.P2PoolAPI.update_network_stats')
    @patch('p2pool.api.P2PoolAPI.update_pool_blocks')
    @patch('p2pool.api.P2PoolAPI.update_pool_stats')
    @patch('p2pool.api.P2PoolAPI.update_stats_mod')
    def test_update_all_endpoints_remote(self, mock_update_stats_mod, mock_update_pool_stats, mock_update_pool_blocks, mock_update_network_stats, mock_update_local_stratum, mock_update_local_p2p, mock_update_local_console):
        mock_update_local_console.return_value = True
        mock_update_local_p2p.return_value = True
        mock_update_local_stratum.return_value = True
        mock_update_network_stats.return_value = True
        mock_update_pool_blocks.return_value = True
        mock_update_pool_stats.return_value = True
        mock_update_stats_mod.return_value = True
        result = self.remote_api.update_all_endpoints()
        self.assertTrue(result)
        mock_update_local_console.assert_called_once()
        mock_update_local_p2p.assert_called_once()
        mock_update_local_stratum.assert_called_once()
        mock_update_network_stats.assert_called_once()
        mock_update_pool_blocks.assert_called_once()
        mock_update_pool_stats.assert_called_once()
        mock_update_stats_mod.assert_called_once()

    @patch('p2pool.db.P2PoolDatabase.retrieve_data_from_db')
    def test_get_from_db_local(self, mock_retrieve_data):
        mock_retrieve_data.return_value = [{"key": "value"}]
        result = self.local_api.get_from_db("table_name", "selection")
        self.assertEqual(result, [{"key": "value"}])
        mock_retrieve_data.assert_called_once_with("sqlite:///p2pool.db", "table_name", "selection")

    @patch('p2pool.db.P2PoolDatabase.retrieve_data_from_db')
    def test_get_from_db_remote(self, mock_retrieve_data):
        mock_retrieve_data.return_value = [{"key": "value"}]
        result = self.remote_api.get_from_db("table_name", "selection")
        self.assertEqual(result, [{"key": "value"}])
        mock_retrieve_data.assert_called_once_with("sqlite:///p2pool.db", "table_name", "selection")

if __name__ == '__main__':
    unittest.main()

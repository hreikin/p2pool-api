import unittest
from unittest.mock import patch, MagicMock
from p2pool.db import P2PoolDatabase
from sqlalchemy.orm import Session

class TestP2PoolDatabase(unittest.TestCase):

    @patch('p2pool.db.create_engine')
    @patch('p2pool.models.Base.metadata.create_all')
    def test_init_db(self, mock_create_all, mock_create_engine):
        db_url = "sqlite:///test.db"
        engine = MagicMock()
        mock_create_engine.return_value = engine
        result = P2PoolDatabase._init_db(db_url)
        self.assertEqual(result, engine)
        mock_create_engine.assert_called_once_with(db_url)
        mock_create_all.assert_called_once_with(engine)

    @patch('p2pool.db.P2PoolDatabase._get_db_session')
    def test_insert_data_into_db(self, mock_get_db_session):
        session = MagicMock()
        mock_get_db_session.return_value = session
        json_data = {"mode": "test", "tcp_port": 1234}
        P2PoolDatabase._insert_data_into_db(json_data, "local/console", "sqlite:///test.db")
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.close.assert_called_once()

    @patch('p2pool.db.P2PoolDatabase._get_db_session')
    def test_retrieve_data_from_db(self, mock_get_db_session):
        mock_session = MagicMock(spec=Session)
        mock_get_db_session.return_value = mock_session
        mock_query = mock_session.query.return_value
        mock_query.order_by.return_value.limit.return_value.all.return_value = [MagicMock(_asdict=lambda: {"key": "value"})]
        data = P2PoolDatabase.retrieve_data_from_db("sqlite:///test.db", "console")
        self.assertEqual(data, [{"key": "value"}])

if __name__ == '__main__':
    unittest.main()

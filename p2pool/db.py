from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from p2pool.exceptions import P2PoolDatabaseError
from p2pool.models import Base, Console, P2P, Stratum, NetworkStats, PoolBlocks, PoolStats, StatsMod
from p2pool.helpers import _local_console_endpoint, _local_p2p_endpoint, _local_stratum_endpoint, _network_stats_endpoint, _pool_blocks_endpoint, _pool_stats_endpoint, _stats_mod_endpoint
from datetime import datetime
import traceback, logging

log = logging.getLogger("p2pool.db")

class P2PoolDatabase:
    """
    P2Pool Database class.

    This class provides methods to interact with the P2Pool database.    
    """
    _engines = {}
    _table_model_map = {
        "console": Console,
        "p2p": P2P,
        "stratum": Stratum,
        "network_stats": NetworkStats,
        "pool_blocks": PoolBlocks,
        "pool_stats": PoolStats,
        "stats_mod": StatsMod
    }

    @classmethod
    def _init_db(cls, db_url):
        """
        Initializes the database engine, if it already exists, it returns the existing engine.

        Args:
            db_url (str): Database URL for creating the engine.

        Returns:
            Engine: SQLAlchemy engine instance.

        Raises:
            P2PoolDatabaseError: If an error occurs while initializing the database.
        """
        try:
            if db_url not in cls._engines:
                engine = create_engine(db_url)
                Base.metadata.create_all(engine)
                cls._engines[db_url] = engine
            return cls._engines[db_url]
        except Exception as e:
            raise P2PoolDatabaseError(e, traceback.format_exc(), f"An error occurred initializing the database:") from e
    
    @classmethod
    def _get_db_session(cls, db_url):
        """
        Returns a new session for the specified database URL.

        Args:
            db_url (str): Database URL for creating the session.

        Returns:
            Session: SQLAlchemy session instance.

        Raises:
            P2PoolDatabaseError: If the database engine does not exist.
        """
        try:
            engine = cls._engines[db_url]
            Session = sessionmaker(bind=engine)
            return Session()
        except KeyError as e:
            raise P2PoolDatabaseError(e, traceback.format_exc(), f"Database engine for '{db_url}' does not exist. Please initialize the database first.") from e
    
    @classmethod
    def _insert_data_into_db(cls, json_data, endpoint, db_url):
        """
        Inserts JSON data into the specified database table.

        Args:
            json_data (dict | list): JSON data to insert.
            endpoint (str): Endpoint from which the data is retrieved.
            db_url (str): Database URL for creating the engine.

        Raises:
            P2PoolDatabaseError: If an error occurs while inserting data into the database.
        """
        try:
            session = cls._get_db_session(db_url)
            cur_time = datetime.now()
            if endpoint == _local_console_endpoint:
                cls._insert_local_console_data(session, json_data, cur_time)
            elif endpoint == _local_p2p_endpoint:
                cls._insert_local_p2p_data(session, json_data, cur_time)
            elif endpoint == _local_stratum_endpoint:
                cls._insert_local_stratum_data(session, json_data, cur_time)
            elif endpoint == _network_stats_endpoint:
                cls._insert_network_stats_data(session, json_data, cur_time)
            elif endpoint == _pool_blocks_endpoint:
                cls._insert_pool_blocks_data(session, json_data, cur_time)
            elif endpoint == _pool_stats_endpoint:
                cls._insert_pool_stats_data(session, json_data, cur_time)
            elif endpoint == _stats_mod_endpoint:
                cls._insert_stats_mod_data(session, json_data, cur_time)
            session.commit()
        except Exception as e:
            session.rollback()
            raise P2PoolDatabaseError(e, traceback.format_exc(), f"An error occurred inserting data to the database:") from e
        finally:
            session.close()
    
    @classmethod
    def _insert_local_console_data(cls, session, json_data, cur_time):
        """
        Inserts local console endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a Console object which is then added to the database session.

        Args:
            session (Session): The database session to add the local console data to.
            json_data (dict): The JSON data containing the local console information.
            cur_time (datetime): The current timestamp.
        """
        local_console = Console(
            time = cur_time,
            full_json = json_data,
            mode = json_data.get("mode"),
            tcp_port = json_data.get("tcp_port")
        )
        session.add(local_console)
    
    @classmethod
    def _insert_local_p2p_data(cls, session, json_data, cur_time):
        """
        Inserts local p2p endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a P2P object which is then added to the database session.

        Args:
            session (Session): The database session to add the local p2p data to.
            json_data (dict): The JSON data containing the local p2p information.
            cur_time (datetime): The current timestamp.
        """
        local_p2p = P2P(
            time = cur_time,
            full_json = json_data,
            connections = json_data.get("connections"),
            incoming_connections = json_data.get("incoming_connections"),
            peer_list_size = json_data.get("peer_list_size"),
            peers = json_data.get("peers"),
            uptime = json_data.get("uptime")
        )
        session.add(local_p2p)
    
    @classmethod
    def _insert_local_stratum_data(cls, session, json_data, cur_time):
        """
        Inserts local stratum endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a Stratum object which is then added to the database session.

        Args:
            session (Session): The database session to add the local stratum data to.
            json_data (dict): The JSON data containing the local stratum information.
            cur_time (datetime): The current timestamp.
        """
        local_stratum = Stratum(
            time = cur_time,
            full_json = json_data,
            hashrate_15m = json_data.get("hashrate_15m"),
            hashrate_1h = json_data.get("hashrate_1h"),
            hashrate_24h = json_data.get("hashrate_24h"),
            total_hashes = json_data.get("total_hashes"),
            shares_found = json_data.get("shares_found"),
            shares_failed = json_data.get("shares_failed"),
            average_effort = json_data.get("average_effort"),
            current_effort = json_data.get("current_effort"),
            connections = json_data.get("connections"),
            incoming_connections = json_data.get("incoming_connections"),
            block_reward_share_percent = json_data.get("block_reward_share_percent"),
            workers = json_data.get("workers")
        )
        session.add(local_stratum)
    
    @classmethod
    def _insert_network_stats_data(cls, session, json_data, cur_time):
        """
        Inserts network stats endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a NetworkStats object which is then added to the database session.

        Args:
            session (Session): The database session to add the network stats data to.
            json_data (dict): The JSON data containing the network stats information.
            cur_time (datetime): The current timestamp.
        """
        network_stats = NetworkStats(
            time = cur_time,
            full_json = json_data,
            difficulty = json_data.get("difficulty"),
            hash_value = json_data.get("hash"),
            height = json_data.get("height"),
            reward = json_data.get("reward"),
            timestamp = json_data.get("timestamp")
        )
        session.add(network_stats)
    
    @classmethod
    def _insert_pool_blocks_data(cls, session, json_data, cur_time):
        """
        Inserts pool blocks endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a PoolBlocks object which is then added to the database session.

        Args:
            session (Session): The database session to add the pool blocks data to.
            json_data (dict): The JSON data containing the pool blocks information.
            cur_time (datetime): The current timestamp.
        """
        pool_blocks = PoolBlocks(
            time = cur_time,
            full_json = json_data,
        )
        session.add(pool_blocks)
    
    @classmethod
    def _insert_pool_stats_data(cls, session, json_data, cur_time):
        """
        Inserts pool stats endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a PoolStats object which is then added to the database session.

        Args:
            session (Session): The database session to add the pool stats data to.
            json_data (dict): The JSON data containing the pool stats information.
            cur_time (datetime): The current timestamp.
        """
        pool_stats = PoolStats(
            time = cur_time,
            full_json = json_data,
            pool_list = json_data.get("pool_list"),
            pool_statistics = json_data.get("pool_statistics"),
            hashrate = json_data["pool_statistics"].get("hashRate") if json_data.get("pool_statistics") else None,
            miners = json_data["pool_statistics"].get("miners") if json_data.get("pool_statistics") else None,
            total_hashes = json_data["pool_statistics"].get("totalHashes") if json_data.get("pool_statistics") else None,
            last_block_found_time = json_data["pool_statistics"].get("lastBlockFoundTime") if json_data.get("pool_statistics") else None,
            last_block_found = json_data["pool_statistics"].get("lastBlockFound") if json_data.get("pool_statistics") else None,
            total_blocks_found = json_data["pool_statistics"].get("totalBlocksFound") if json_data.get("pool_statistics") else None,
            pplns_weight = json_data["pool_statistics"].get("pplnsWeight") if json_data.get("pool_statistics") else None,
            pplns_window_size = json_data["pool_statistics"].get("pplnsWindowSize") if json_data.get("pool_statistics") else None,
            sidechain_difficulty = json_data["pool_statistics"].get("sidechainDifficulty") if json_data.get("pool_statistics") else None,
            sidechain_height = json_data["pool_statistics"].get("sidechainHeight") if json_data.get("pool_statistics") else None
        )
        session.add(pool_stats)
    
    @classmethod
    def _insert_stats_mod_data(cls, session, json_data, cur_time):
        """
        Inserts stats mod endpoints data into the database.

        This method extracts various pieces of information from the provided JSON data
        and creates a StatsMod object which is then added to the database session.

        Args:
            session (Session): The database session to add the stats mod data to.
            json_data (dict): The JSON data containing the stats mod information.
            cur_time (datetime): The current timestamp.
        """
        stats_mod = StatsMod(
            time = cur_time,
            full_json = json_data,
            config = json_data.get("config"),
            ports = json_data["config"].get("ports") if json_data.get("config") else None,
            fee = json_data["config"].get("fee") if json_data.get("config") else None,
            min_payment_threshold = json_data["config"].get("minPaymentThreshold") if json_data.get("config") else None,
            network = json_data.get("network"),
            height = json_data["network"].get("height") if json_data.get("network") else None,
            pool = json_data.get("pool"),
            stats = json_data["pool"].get("stats") if json_data.get("pool") else None,
            last_block_found = json_data["pool"]["stats"].get("lastBlockFound") if json_data.get("pool") and json_data["pool"].get("stats") else None,
            blocks = json_data["pool"].get("blocks") if json_data.get("pool") else None,
            miners = json_data["pool"].get("miners") if json_data.get("pool") else None,
            hashrate = json_data["pool"].get("hashrate") if json_data.get("pool") else None,
            round_hashes = json_data["pool"].get("roundHashes") if json_data.get("pool") else None
        )
        session.add(stats_mod)
    
    @classmethod
    def retrieve_data_from_db(cls, db_url, table_name, selection = "*", start_time = None, end_time = None, limit = 1):
        """
        Retrieves data from the specified database table within the given timeframe.

        Args:
            db_url (str): Database URL for creating the engine.
            table_name (str): Name of the table to retrieve data from.
            selection (str, optional): Column(s) to select from the table. Defaults to "*".
            start_time (datetime, optional): Start time for the data retrieval. Defaults to None.
            end_time (datetime, optional): End time for the data retrieval. Defaults to None.
            limit (int, optional): Limit the number of rows retrieved. Defaults to 1.

        Returns:
            list: List of dictionaries containing the retrieved data or "N/A" if no data is found.

        Raises:
            P2PoolDatabaseError: If an error occurs while retrieving data from the database.
        """
        data = "N/A"
        try:
            session = cls._get_db_session(db_url)

            model_class = cls._table_model_map.get(table_name)
            if not model_class:
                raise ValueError(f"Table '{table_name}' does not have a corresponding ORM model class.")

            # Build the query
            query = session.query(model_class)

            # Apply selection
            if selection != "*":
                if isinstance(selection, list):
                    query = query.with_entities(*[getattr(model_class, col) for col in selection])
                else:
                    query = query.with_entities(getattr(model_class, selection))

            # Apply time filters
            if start_time:
                query = query.filter(model_class.timestamp >= start_time)
            if end_time:
                query = query.filter(model_class.timestamp <= end_time)

            # Apply limit
            query = query.order_by(model_class.timestamp.desc()).limit(limit)

            # Execute the query and fetch results
            results = query.all()
            if results:
                data = [result._asdict() for result in results]
            else:
                data = "N/A"
        except Exception as e:
            raise P2PoolDatabaseError(e, traceback.format_exc(), f"An error occurred retrieving data from the database:") from e
        finally:
            session.close()
        return data

# Define the public interface of the module
__all__ = ["P2PoolDatabase"]
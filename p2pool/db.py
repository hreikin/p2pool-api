from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from p2pool.exceptions import P2PoolDatabaseError
from p2pool.models import Base, Console, P2P, Stratum, NetworkStats, PoolBlocks, PoolStats, StatsMod
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
"""
P2Pool Models module.

This module provides SQLAlchemy ORM models for various P2Pool API endpoints.
It includes:

- Console: ORM model for the local console endpoint.
- P2P: ORM model for the local P2P endpoint.
- Stratum: ORM model for the local stratum endpoint.
- NetworkStats: ORM model for the network stats endpoint.
- PoolBlocks: ORM model for the pool blocks endpoint.
- PoolStats: ORM model for the pool stats endpoint.
- StatsMod: ORM model for the stats mod endpoint.
"""

from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Console(Base):
    """
    ORM model for the local console endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
        mode (str): Mode of the console.
        tcp_port (int): TCP port of the console.
    """
    __tablename__ = 'console'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    mode = Column(String)
    tcp_port = Column(Integer)

class P2P(Base):
    """
    ORM model for the local P2P endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
        connections (int): Number of connections.
        incoming_connections (int): Number of incoming connections.
        peer_list_size (int): Size of the peer list.
        peers (dict): List of peers.
        uptime (int): Uptime of the P2P connection.
    """
    __tablename__ = 'p2p'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    connections = Column(Integer)
    incoming_connections = Column(Integer)
    peer_list_size = Column(Integer)
    peers = Column(JSON)
    uptime = Column(Integer)

class Stratum(Base):
    """
    ORM model for the local stratum endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
        hashrate_15m (int): Hashrate for the last 15 minutes.
        hashrate_1h (int): Hashrate for the last hour.
        hashrate_24h (int): Hashrate for the last 24 hours.
        total_hashes (int): Total number of hashes.
        shares_found (int): Number of shares found.
        shares_failed (int): Number of shares failed.
        average_effort (float): Average effort.
        current_effort (float): Current effort.
        connections (int): Number of connections.
        incoming_connections (int): Number of incoming connections.
        block_reward_share_percent (float): Block reward share percentage.
        workers (dict): List of workers.
    """
    __tablename__ = 'stratum'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    hashrate_15m = Column(Integer)
    hashrate_1h = Column(Integer)
    hashrate_24h = Column(Integer)
    total_hashes = Column(Integer)
    shares_found = Column(Integer)
    shares_failed = Column(Integer)
    average_effort = Column(Float)
    current_effort = Column(Float)
    connections = Column(Integer)
    incoming_connections = Column(Integer)
    block_reward_share_percent = Column(Float)
    workers = Column(JSON)

class NetworkStats(Base):
    """
    ORM model for the network stats endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
        difficulty (int): Network difficulty.
        hash_value (str): Network hash value.
        height (int): Network height.
        reward (int): Network reward.
        timestamp (int): Network timestamp.
    """
    __tablename__ = 'network_stats'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    difficulty = Column(Integer)
    hash_value = Column(String)
    height = Column(Integer)
    reward = Column(Integer)
    timestamp = Column(Integer)

class PoolBlocks(Base):
    """
    ORM model for the pool blocks endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
    """
    __tablename__ = 'pool_blocks'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)

class PoolStats(Base):
    """
    ORM model for the pool stats endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
        pool_list (dict): List of pools.
        pool_statistics (dict): Pool statistics.
        hashrate (int): Pool hashrate.
        miners (int): Number of miners.
        total_hashes (int): Total number of hashes.
        last_block_found_time (int): Time of the last block found.
        last_block_found (int): Last block found.
        total_blocks_found (int): Total number of blocks found.
        pplns_weight (int): PPLNS weight.
        pplns_window_size (int): PPLNS window size.
        sidechain_difficulty (int): Sidechain difficulty.
        sidechain_height (int): Sidechain height.
    """
    __tablename__ = 'pool_stats'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    pool_list = Column(JSON)
    pool_statistics = Column(JSON)
    hashrate = Column(Integer)
    miners = Column(Integer)
    total_hashes = Column(Integer)
    last_block_found_time = Column(Integer)
    last_block_found = Column(Integer)
    total_blocks_found = Column(Integer)
    pplns_weight = Column(Integer)
    pplns_window_size = Column(Integer)
    sidechain_difficulty = Column(Integer)
    sidechain_height = Column(Integer)

class StatsMod(Base):
    """
    ORM model for the stats mod endpoint.

    Attributes:
        uid (int): Primary key.
        time (datetime): Timestamp of the record.
        full_json (dict): Full JSON data.
        config (dict): Configuration data.
        ports (dict): Ports data.
        fee (int): Fee.
        min_payment_threshold (int): Minimum payment threshold.
        network (dict): Network data.
        height (int): Network height.
        pool (dict): Pool data.
        stats (dict): Stats data.
        last_block_found (str): Last block found.
        blocks (dict): Blocks data.
        miners (int): Number of miners.
        hashrate (int): Hashrate.
        round_hashes (int): Round hashes.
    """
    __tablename__ = 'stats_mod'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    config = Column(JSON)
    ports = Column(JSON)
    fee = Column(Integer)
    min_payment_threshold = Column(Integer)
    network = Column(JSON)
    height = Column(Integer)
    pool = Column(JSON)
    stats = Column(JSON)
    last_block_found = Column(String)
    blocks = Column(JSON)
    miners = Column(Integer)
    hashrate = Column(Integer)
    round_hashes = Column(Integer)

# Define the public interface of the module
__all__ = ["Console", "P2P", "Stratum", "NetworkStats", "PoolBlocks", "PoolStats", "StatsMod"]
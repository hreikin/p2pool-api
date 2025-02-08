from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Console(Base):
    __tablename__ = 'console'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)
    mode = Column(String)
    tcp_port = Column(Integer)

class P2P(Base):
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
    __tablename__ = 'pool_blocks'
    uid = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now)
    full_json = Column(JSON)

class PoolStats(Base):
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
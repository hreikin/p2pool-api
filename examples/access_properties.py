from env import log, api_path
from p2pool import P2PoolAPI

log.info(f"Initializing P2PoolAPI with path: {api_path}")
x = P2PoolAPI(api_path)
log.info("P2PoolAPI initialized.")
log.info("Full JSON response examples:")
log.info(f"`local/console` endpoint: {x.local_console}")
log.info(f"`local/p2p` endpoint: {x.local_p2p}")
log.info(f"`local/stratum` endpoint: {x.local_stratum}")
log.info("Individual data examples:")
log.info(f"`uptime` from `local/p2p` endpoint: {x.local_p2p_uptime}")
log.info(f"`heights` from `pool/blocks` endpoint: {x.pool_blocks_heights}")
log.info(f"`ports` from `stats/mod` endpoint: {x.stats_mod_ports}")
from env import log, api_path
from p2pool import P2PoolAPI

log.info(f"Initializing P2PoolAPI with path: {api_path}")
x = P2PoolAPI(api_path)
log.info("P2PoolAPI initialized.")
log.info("Updating all individual endpoints.")
x.update_local_console()
x.update_local_p2p()
x.update_local_stratum()
x.update_network_stats()
x.update_pool_blocks()
x.update_pool_stats()
x.update_stats_mod()
log.info("All individual endpoints updated.")
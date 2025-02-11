from env import log, api_path
from p2pool import P2PoolAPI

log.info(f"Initializing P2PoolAPI with path: {api_path}")
x = P2PoolAPI(api_path)
log.info("P2PoolAPI initialized.")
log.info("Updating all endpoints.")
x.update_all_endpoints()
log.info("All endpoints updated.")
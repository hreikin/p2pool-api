from env import log
from p2pool import P2PoolAPI

api_path = "api/"               # Can also be a URL: api_path = "http://example.com/api/"
log.info(f"Initializing P2PoolAPI with path: {api_path}")
x = P2PoolAPI(api_path)         # If using a URL: x = P2PoolAPI(api_path, is_remote=True)
log.info("P2PoolAPI initialized.")
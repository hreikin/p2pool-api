import logging
from p2pool import P2PoolAPI

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,  # Set the log level for the entire application, change to DEBUG to print all responses.
    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s',  # Consistent format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
log = logging.getLogger("MyLOG")

api_path = "api/"               # Can also be a URL: api_path = "http://example.com/api/"
x = P2PoolAPI(api_path)         # If using a URL: x = P2PoolAPI(api_path, is_remote=True)

x.update_stats_mod()            # Update individual `stats_mod` endpoint
x.update_all_endpoints()        # Update all endpoints at once
log.info(x.local_stratum)       # Log entire response
log.info(x.local_p2p_uptime)    # Log property representing individual data from the API
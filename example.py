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

api_path = "api/"
x = P2PoolAPI(api_path)

x.get_stats_mod()                                               # Update individual `stats_mod` endpoint
x.get_all_data()                                                # Update all endpoints at once
log.info(x._local_stratum)                                      # Log entire response
log.info(x.local_p2p_uptime)                                    # Log property representing individual data from the API
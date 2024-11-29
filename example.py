import p2pool_api, logging

logging.basicConfig()
logging.getLogger("P2PoolAPI").setLevel(logging.INFO)           # Change to DEBUG to print out all responses when their methods are called
log = logging.getLogger("MyLOG")

api_path = "/path/to/p2pool/api"
x = p2pool_api.P2PoolAPI(api_path)

log.info(x._local_stratum)                                      # Log entire reponse
log.info(x.local_p2p_uptime)                                    # Log property representing individual data from the API
x.get_stats_mod()                                               # Update individual `stats_mod` endpoint
x.get_all_data()                                                # Update all endpoints at once
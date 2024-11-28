import p2pool_api

api = "/path/to/p2pool/api"

x = p2pool_api.P2PoolAPI(api)

print(x._local_stratum)         # Print entire reponse
print(x.local_p2p_uptime)       # Print property representing individual data from the API
x.get_stats_mod()               # Update individual `stats_mod` endpoint
x.get_all_data()                # Update all endpoints at once
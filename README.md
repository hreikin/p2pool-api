# P2Pool API

This module provides the `P2PoolAPI` object to allow interacting with the P2Pool API.

## Usage

API data is updated on initialization and can be updated individually or altogether using the relevant methods. Data is also available as properties to allow accessing the cached endpoint data all at once or as individual items.

```python
import p2pool_api

api = "/path/to/p2pool/api"

x = p2pool_api.P2PoolAPI(api)

print(x._local_stratum)         # Print entire reponse
print(x.local_p2p_uptime)       # Print property representing individual data from the API
x.get_stats_mod()               # Update individual endpoints
x.get_all_data()                # Update all endpoints at once
```
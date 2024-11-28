# P2Pool API

This module provides the `P2PoolAPI` object to allow interacting with the P2Pool API.

## Installation

The module can be installed from PyPi or Github with pip:

```
pip install p2pool-api
# or to install from the Github repository
pip install p2pool-api@git+https://github.com/hreikin/p2pool-api.git@main
```

## Usage

API data is updated on initialization and can be updated individually or altogether using the relevant methods. Data is also available as properties to allow accessing the cached endpoint data all at once or as individual items.

```python
import p2pool_api

api = "/path/to/p2pool/api"

x = p2pool_api.P2PoolAPI(api)

print(x._local_stratum)         # Print entire reponse
print(x.local_p2p_uptime)       # Print property representing individual data from the API
x.get_stats_mod()               # Update individual `stats_mod` endpoint
x.get_all_data()                # Update all endpoints at once
```
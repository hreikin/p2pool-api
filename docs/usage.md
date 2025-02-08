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
```
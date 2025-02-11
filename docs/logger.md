# Logging

To enable logging within your project and get detailed information from the P2Pool-API library, you can configure the logging module in your Python script. Here is an example of how to set up logging:

```python
import logging

# Configure the logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level for the entire application, change to DEBUG to print all responses.
    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s',  # Consistent format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

log = logging.getLogger("MyLogger")

from p2pool import P2PoolAPI

api_path = "api/"               # Can also be a URL: api_path = "http://example.com/api/"
log.info(f"Initializing P2PoolAPI with path: {api_path}")
x = P2PoolAPI(api_path)         # If using a URL: x = P2PoolAPI(api_path, is_remote=True)
log.info("P2PoolAPI initialized.")
```

This configuration will output detailed debug information to the console, including timestamps, logger names, log levels, and log messages.


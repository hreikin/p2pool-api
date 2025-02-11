import logging
# Configure the root logger
logging.basicConfig(
    level=logging.INFO,  # Set the log level for the entire application, change to DEBUG to print all responses.
    format='[%(asctime)s - %(name)s] - %(levelname)s - %(message)s',  # Consistent format
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
log = logging.getLogger("ExampleLog")
api_path = "../api/"               # Can also be a URL: api_path = "http://example.com/api/"

log.info("####################################################################################################################################")
log.info("## Please ensure you have a running P2Pool instance to connect to and have updated the connection details within the env.py file. ##")
log.info("####################################################################################################################################")
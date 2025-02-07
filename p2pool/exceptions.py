"""
P2Pool Exceptions module.

This module provides custom exception classes for handling specific P2Pool API errors.
It includes:

- P2PoolAPIError: General error with the P2Pool API.
- P2PoolConnectionError: Connection error with the P2Pool API.
- P2PoolDatabaseError: Database error with the P2Pool API.
"""
class P2PoolAPIError(Exception):
    """
    Exception raised when a general error occurs with the P2Pool API.

    Attributes:
        error (str): Specific error message.
        traceback (str): Traceback of the error.
        message (str): Error message explaining the API issue.
    """
    def __init__(self, error = None, traceback = None, message = "An error occurred with the P2Pool API:"):
        """
        Initialize the API error.

        Args:
            error (str, optional): Specific error message. Defaults to None.
            traceback (str, optional): Traceback of the error. Defaults to None.
            message (str): Error message explaining the API issue. Defaults to a generic API error message.
        """
        error_message = f" {error}" if error else ""
        traceback_message = f"\n{traceback}" if traceback else ""
        self.message = message + error_message + traceback_message
        super().__init__(self.message)

class P2PoolConnectionError(P2PoolAPIError):
    """
    Exception raised when a connection error occurs with the P2Pool API.
    """
    def __init__(self, error = None, traceback = None, message = "Failed to connect to the P2Pool API. Please check the IP, port, and network connection."):
        super().__init__(error, traceback, message)

class P2PoolDatabaseError(P2PoolAPIError):
    """
    Exception raised when a database error occurs with the P2Pool API.
    """
    def __init__(self, error = None, traceback = None, message = "An error occurred with the P2Pool database. Please check the database configuration."):
        super().__init__(error, traceback, message)

# Define the public interface of the module
__all__ = ["P2PoolAPIError", "P2PoolConnectionError", "P2PoolDatabaseError"]
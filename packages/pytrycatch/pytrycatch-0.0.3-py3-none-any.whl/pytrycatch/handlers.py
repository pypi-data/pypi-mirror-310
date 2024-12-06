import logging
from functools import wraps

# Configure default logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("pytrycatch")

def handle_errors(log=True, default_return=None, exception_types=(Exception,), log_level=logging.ERROR, custom_handler=None):
    """
    A decorator to handle exceptions in a function.
    
    Args:
        log (bool): Whether to log the exception.
        default_return (any): The value to return if an exception occurs.
        exception_types (tuple): Specific exception types to catch.
        log_level (int): The logging level to use (default: logging.ERROR).
        custom_handler (function): A custom handler function to call when an exception occurs.
    
    Returns:
        Decorated function with error handling.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                # Call the custom handler if provided
                if custom_handler:
                    custom_handler(func, e)
                
                # Log the error message without traceback
                if log:
                    logger.log(log_level, f"Exception in {func.__name__}: {str(e)}")
                
                return default_return
        return wrapper
    return decorator

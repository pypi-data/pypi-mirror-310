import logging
from functools import wraps

# Configure default logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("pytrycatch")

def handle_errors(log=True, default_return=None, exception_types=(Exception,)):
    """
    A decorator to handle exceptions in a function.
    
    Args:
        log (bool): Whether to log the exception.
        default_return (any): The value to return if an exception occurs.
        exception_types (tuple): Specific exception types to catch.
    
    Returns:
        Decorated function with error handling.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                if log:
                    logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
                return default_return
        return wrapper
    return decorator

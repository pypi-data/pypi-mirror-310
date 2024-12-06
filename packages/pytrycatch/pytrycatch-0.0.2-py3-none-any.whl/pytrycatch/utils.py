def safe_execute(func, *args, default_return=None, log=False, **kwargs):
    """
    Execute a function safely without raising exceptions.
    
    Args:
        func (callable): The function to execute.
        default_return (any): The value to return if an exception occurs.
        log (bool): Whether to log the exception.
        
    Returns:
        Result of the function or default_return.
    """
    from .handlers import logger
    
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log:
            logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
        return default_return

import logging
import traceback
logger = logging.getLogger()
def try_decorator(original_function):
    def wrapper_function(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
        except Exception:
            logger.error(traceback.print_exc())
            pass
    return wrapper_function
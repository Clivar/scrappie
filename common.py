import time
from functools import wraps
import logging
logger = logging.getLogger(__name__)

def retry(tries=3, delay=1, backoff=2):
    """Retry calling the decorated function using an exponential backoff."""

    def deco_retry(func):

        @wraps(func)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay  # mutable versions of tries and delay
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warn(f"{str(e)}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            raise ValueError("Failed after several retry attempts")

        return f_retry

    return deco_retry
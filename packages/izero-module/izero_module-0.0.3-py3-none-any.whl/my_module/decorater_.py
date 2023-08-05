import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def log_arguments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logging.info(f"args: {args}\tkwargs: {kwargs}\treturn: {res}")
        return res

    return wrapper

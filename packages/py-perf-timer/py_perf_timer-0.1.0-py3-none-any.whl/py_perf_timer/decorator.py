

import functools
from .measurer import Measurer


def measure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with Measurer(func.__name__):
            return func(*args, **kwargs)
    return wrapper
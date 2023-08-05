#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import logging
from multiprocessing import current_process
import multiprocessing_logging
from functools import wraps

__version__ = "0.1.0"

logger = logging.getLogger()

# Create a decorator for functions that are called via multiprocessing pools
# This decorator adds process name to log messages
# Create a decorator for functions that are called via multiprocessing pools
def logs_mp_process_names(fn):
    class MultiProcessLogFilter(logging.Filter):
        def filter(self, record):
            try:
                process_name = current_process().name
            except BaseException:
                process_name = __name__
            record.msg = f"{process_name} :: {record.msg}"
            return True

    multiprocessing_logging.install_mp_handler()
    f = MultiProcessLogFilter()

    # Wraps is needed here so apply / apply_async know the function name
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger.removeFilter(f)
        logger.addFilter(f)
        return fn(*args, **kwargs)

    return wrapper

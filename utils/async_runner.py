"""
Module to run YouTube subtitle processing asynchronously with timeout.
"""

import threading
import time
from typing import Callable

def run_with_timeout(func: Callable, args=(), kwargs=None, timeout: int = 30):
    """
    Run a function in a separate thread with a timeout.

    Args:
        func: function to run
        args: positional arguments for func
        kwargs: keyword arguments for func
        timeout: seconds before forcefully stopping

    Returns:
        result: function return value, or None if timeout
        status: 'success', 'timeout', or 'error'
    """
    if kwargs is None:
        kwargs = {}

    result_container = {'result': None, 'status': 'success'}

    def target():
        try:
            result_container['result'] = func(*args, **kwargs)
        except Exception as e:
            result_container['result'] = e
            result_container['status'] = 'error'

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # Thread still running → timeout
        result_container['status'] = 'timeout'
        return None, 'timeout'

    return result_container['result'], result_container['status']

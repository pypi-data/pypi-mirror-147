"""
A Python library to quickly time functions.
"""
import time

def time_function(func):
    """
    Run a certain function and return the time it took to run (in milliseconds).
    """
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    return end - start

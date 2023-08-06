import os

from quicktimekeeper.__main__ import time_function

def test_timing():
    """
    Test the time_function function.
    """
    def test_func():
        """
        A function to test.
        """
        pass
    assert time_function(test_func) > 0
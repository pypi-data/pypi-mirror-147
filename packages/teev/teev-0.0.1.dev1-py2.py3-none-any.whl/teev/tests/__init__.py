import time
import unittest
from threading import Thread
from multiprocessing import Process

from teev import Teev


def thread_decorator(func):
    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def process_decorator(func):
    def wrapper(*args, **kwargs):
        process = Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process

    return wrapper


def time_func(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"\n{func.__name__}: {end - start:.3}s")
        return result

    return wrapper


class TestTeev(unittest.TestCase):
    @time_func
    def test_buffer_one(self):

        self.assertEqual(True, True)

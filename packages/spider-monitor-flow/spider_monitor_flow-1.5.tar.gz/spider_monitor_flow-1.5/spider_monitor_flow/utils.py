from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import pytz


def get_cur_date():
    return datetime.datetime.now(pytz.timezone('PRC')).strftime("%Y-%m-%d")


pool = ThreadPoolExecutor()

def get_cur_timestamp():
    return int(time.time())


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner

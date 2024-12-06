import concurrent.futures
import logging
from threading import Thread
from typing import Union, List

import gevent.monkey


def is_gevent_patched():
    if gevent.monkey.is_module_patched('socket') and gevent.monkey.is_module_patched('threading'):
        return True

    return False


def concurrent_execute(fn, data: Union[List[dict], List[str], List[tuple], List[list]], work_num=4):
    def process_item(item):
        if isinstance(item, dict):
            return fn(**item)
        elif isinstance(item, tuple):
            return fn(*item)
        elif isinstance(item, list):
            return fn(*item)
        elif isinstance(item, str):
            return fn(item)
        else:
            raise ValueError(f"Unsupported data type: {type(item)}")

    if is_gevent_patched():
        # 主要在api状态下使用
        logging.debug(f"gevent concurrent_execute, fn:{fn.__name__} data: {repr(data)}")
        jobs = [gevent.spawn(process_item, x) for x in data]
        gevent.joinall(jobs)
        results = [job.value for job in jobs]
    else:
        logging.debug(f"thread concurrent_execute,work_num:{work_num} fn:{fn.__name__} data: {repr(data)}")
        with concurrent.futures.ThreadPoolExecutor(work_num) as executor:
            results = list(executor.map(process_item, data))
    return results


def run_in_thread(fn):
    '''
    @run_in_thread
    def test(abc):
        return abc

    test(123)
    '''

    def wrapper(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t

    return wrapper

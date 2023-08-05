# -*- coding: utf-8 -*-
"""
    :author: Dabai
    :url: samuelbaizg.github.io
    :copyright: © 2018 Dabai <zhgbai@163.com>
    :license: MIT, see LICENSE for more details.
"""
import contextlib
import itertools
import logging
import sys
import threading
import typing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from queue import Queue, Empty


class RWLock(object):
    """
    Classic implementation of reader-writer lock with preference to writers.

    Readers can access a resource simultaneously.
    Writers get an exclusive access.

    API is self-descriptive:
        reader_enters()
        reader_leaves()
        writer_enters()
        writer_leaves()
    """

    def __init__(self):
        self.mutex = threading.RLock()
        self.can_read = threading.Semaphore(0)
        self.can_write = threading.Semaphore(0)
        self.active_readers = 0
        self.active_writers = 0
        self.waiting_readers = 0
        self.waiting_writers = 0

    def reader_enters(self):
        with self.mutex:
            if self.active_writers == 0 and self.waiting_writers == 0:
                self.active_readers += 1
                self.can_read.release()
            else:
                self.waiting_readers += 1
        self.can_read.acquire()

    def reader_leaves(self):
        with self.mutex:
            self.active_readers -= 1
            if self.active_readers == 0 and self.waiting_writers != 0:
                self.active_writers += 1
                self.waiting_writers -= 1
                self.can_write.release()

    @contextlib.contextmanager
    def reader(self):
        self.reader_enters()
        try:
            yield
        finally:
            self.reader_leaves()

    def writer_enters(self):
        with self.mutex:
            if self.active_writers == 0 and self.waiting_writers == 0 and self.active_readers == 0:
                self.active_writers += 1
                self.can_write.release()
            else:
                self.waiting_writers += 1
        self.can_write.acquire()

    def writer_leaves(self):
        with self.mutex:
            self.active_writers -= 1
            if self.waiting_writers != 0:
                self.active_writers += 1
                self.waiting_writers -= 1
                self.can_write.release()
            elif self.waiting_readers != 0:
                t = self.waiting_readers
                self.waiting_readers = 0
                self.active_readers += t
                while t > 0:
                    self.can_read.release()
                    t -= 1

    @contextlib.contextmanager
    def writer(self):
        self.writer_enters()
        try:
            yield
        finally:
            self.writer_leaves()


def create_rlock(process=False):
    """Creates a reentrant lock object."""
    if process:
        from multiprocessing import RLock as rlockp
        return rlockp()
    else:
        from threading import RLock as rlockt
        return rlockt()


def create_lock(process=False):
    """Creates a reentrant lock object."""
    if process:
        from multiprocessing import Lock as lockp
        return lockp()
    else:
        from threading import Lock as lockt
        return lockt()


class WaitCall(object):
    """
        Run functions in thread or process in blocking mode.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, max_workers, process=False):
        if process:
            self._pool = ProcessPoolExecutor(max_workers)
        else:
            self._pool = ThreadPoolExecutor(max_workers)
        self._process = process
        self._max_workers = max_workers
        self._functions = {}

    def submit(self, fn_id, timeout, fn, *args, **kwargs):
        """
        Submits function for execution.
        :param st fn_id: the identification of fn.
        :param int timeout: the number of seconds to wait the fn execution. return None if timeout.
                            if None, then there is no limit on the wait time.
        :param function fn: function to execute
        :param tuple args: parameters of fn
        :param dict kwargs: parameters of fn
        :return void
        """
        if (len(self._functions)) == self._max_workers:
            raise RuntimeError("this call has exceeds the max workers functions , new function can't be added.")
        if fn_id in self._functions:
            raise ValueError("the function %s has been added." % fn_id)
        self._functions[fn_id] = (fn, timeout, args, kwargs)

    def run(self, timeout=None):
        """
        run the multiple functions in thread pool or process pool.
        :param int timeout: The maximum number of seconds to wait. If None, then there
                            is no limit on the wait time.
        :return tuple(data dict, error dict): error error dict is None if no error is raised.
                     the key of data dict is func_id. the key of error dict is func_id.
                     the value of error dict is sys.exc_info tuple (exc_type, exc_value, exc_traceback).
        """

        def wrap_func(fn1, args1, kwargs1):
            try:
                return None, fn1(*args1, **kwargs1)
            except BaseException as e1:
                return e1, sys.exc_info()

        try:
            if len(self._functions) == 1:
                key, (fn, timeout, args, kwargs) = self._functions.popitem()
                try:
                    data = fn(*args, **kwargs)
                    return {key: data}, None
                except Exception as e:
                    self.logger.exception("failed to execute function <%s> due to %s." % (key, str(e)))
                    return None, {key: sys.exc_info()}
            else:
                tasks = []
                for id1, func in self._functions.items():
                    fn, to, args, kwargs = func
                    f = self._pool.submit(wrap_func, fn, args, kwargs)
                    f.timeout = to
                    f.fn_id = id1
                    tasks.append(f)
                datas = {}
                errors = {}
                for future in as_completed(tasks, timeout=timeout):
                    try:
                        future.exception(future.timeout)
                        data = future.result()
                        if data[0] is None:
                            datas[future.fn_id] = data[1]
                        else:
                            errors[future.fn_id] = data[1]
                    except Exception as e:
                        self.logger.exception("failed to execute function <%s> due to %s." % (future.fn_id, str(e)))
                        errors[future.fn_id] = sys.exc_info()
                return datas, None if len(errors) == 0 else errors
        finally:
            self._pool = None


class NoWaitCall(object):
    """
        Run functions in thread or process in no-wait mode.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, max_workers, process=False):
        if process:
            self._pool = ProcessPoolExecutor(max_workers)
        else:
            self._pool = ThreadPoolExecutor(max_workers)
        self._process = process
        self._max_workers = max_workers
        self._lock = create_rlock(self._process)

    def shutdown(self, wait=True):
        """
        Shuts down this executor.
        :param bool wait: ``True`` to wait until all submitted functions
            have been executed
        """
        self._pool.shutdown(wait)

    def submit(self, fn, success_cb, fail_cb, *args, **kwargs):
        """
        Submits function for execution.
        :param function fn: function to execute
        :param function success_cb: function to call while success
        :param function fail_cb: function to call while fail
        :raises MaxInstancesReachedError: if the maximum number of
            allowed instances for this job has been reached
        """

        def callback(f):
            exc, tb = f.exception_info() if hasattr(f, 'exception_info') else (
                f.exception(), getattr(f.exception(), '__traceback__', None))
            exc_info = exc.__class__, exc, tb
            if exc:
                self.logger.exception("failed to execute function due to %s." % str(exc))
                if fail_cb is not None:
                    fail_cb(exc_info)
            else:
                if success_cb is not None:
                    success_cb(f.result())

        with self._lock:
            func = self._pool.submit(fn, *args, **kwargs)
            func.add_done_callback(callback)


@contextlib.contextmanager
def contextmanager_dummy():
    """A context manager that does nothing special."""
    yield


class QueueCall(object):
    """
        Run functions in thread or process in queue mode.
        This class is generally used to speed restapi call via accumulating multiple requests to run in batch.
    """

    logger = logging.getLogger(__name__)

    class Future(threading.Event):
        def __init__(self):
            self._result = None

        def set_result(self, obj):
            self._result = obj

        def get_result(self, timeout=None):
            if self.wait(timeout):
                return self._result
            else:
                raise TimeoutError

    def __init__(self, queue: Queue, max_size: int, fn, process=False):
        """
        Usage:
            firstly, define a global queue "q", a function xxx(list_arg) and a global QueueCall,
            for example: qc = QueueCall(q, xxx, 5)
            secondly, call qc.run to run in a method,
            for example: qc.run([3,4])
        @param Queue queue:
        @param function fn: the function to be run when queue size exceeds max_size. only one List arguments is accepted.
        @param int max_size: the max length of accumulated argument of fn.
        """
        self._queue = queue
        self._fn = fn
        self._max_size = max_size
        if process:
            self._pool = ProcessPoolExecutor(1)
        else:
            self._pool = ThreadPoolExecutor(1)
        self._pool.submit(self._run)

    def run(self, arg: typing.List, timeout=None):
        future = QueueCall.Future()
        self._queue.put((arg, future))
        return future.get_result(timeout=timeout)

    def _run(self):
        args = list()
        futures = list()
        future_range = list()
        while True:
            arg_length = 0
            while len(args) < self._max_size:
                try:
                    if len(args) == 0:
                        arg, future = self._queue.get(block=True)
                    else:
                        arg, future = self._queue.get(block=False)

                    if arg_length == 0 or arg_length + len(arg) < self._max_size:
                        arg_length += len(arg)
                    else:
                        break
                    args.append(arg)
                    futures.append(future)
                    future_range.append((arg_length - len(arg), arg_length))
                except Empty as e:
                    self.logger.info('queue is empty.')
                    break
            if len(arg) > 0:
                results = self._fn(itertools.chain(arg))
                for future, (result_start, result_end) in zip(futures, future_range):
                    future.set_result(results[result_start, result_end])
                args.clear()
                futures.clear()
                future_range.clear()


from __future__ import absolute_import # so we can import standard 'threading'

from .exceptions import print_exception
from threading import Thread, Lock
from Queue import Queue, Empty
import itertools, multiprocessing

# https://gist.github.com/tliron/81dd915166b0bfc64be08b4f8e22c835
class FixedThreadPoolExecutor(object):
    """
    Executes tasks in a fixed thread pool.
    
    Makes sure to gather all returned results and thrown exceptions in one place, in order of task
    submission.
    
    Example::
    
        def sum(arg1, arg2):
            return arg1 + arg2
            
        executor = FixedThreadPoolExecutor(10)
        try:
            for value in range(100):
                executor.submit(sum, value, value)
            executor.drain()
        except:
            executor.close()
        executor.raise_first()
        print executor.returns
    
    You can also use it with the Python "with" keyword, in which case you don't need to call "close"
    explicitly::
    
        with FixedThreadPoolExecutor(10) as executor:
            for value in range(100):
                executor.submit(sum, value, value)
            executor.drain()
            executor.raise_first()
            print executor.returns
    """

    _CYANIDE = object() # Special task marker used to kill worker threads.

    def __init__(self, size=multiprocessing.cpu_count() * 2 + 1, timeout=None, print_exceptions=False):
        """
        :param size: Number of threads in the pool (fixed).
        :param timeout: Timeout in seconds for all blocking operations. (Defaults to none, meaning no timeout) 
        :param print_exceptions: Set to true in order to print exceptions from tasks. (Defaults to false)
        """
        self.size = size
        self.timeout = timeout
        self.print_exceptions = print_exceptions

        self._tasks = Queue()
        self._returns = {}
        self._exceptions = {}
        self._id_creator = itertools.count()
        self._lock = Lock() # for console output

        self._workers = []
        for index in range(size):
            worker = Thread(
                name='%s%d' % (self.__class__.__name__, index),
                target=self._thread_worker)
            worker.daemon = True
            worker.start()
            self._workers.append(worker)

    def submit(self, fn, *args, **kwargs):
        """
        Submit a task for execution.
        
        The task will be called ASAP on the next available worker thread in the pool.
        """
        self._tasks.put((self._id_creator.next(), fn, args, kwargs), timeout=self.timeout)

    def close(self):
        """
        Blocks until all current tasks finish execution and all worker threads are dead.
        
        You cannot submit tasks anymore after calling this.
        
        This is called automatically upon exit if you are using the "with" keyword.
        """
        self.drain()
        while self.is_alive:
            self._tasks.put(self._CYANIDE, timeout=self.timeout)
        self._workers = None

    def drain(self):
        """
        Blocks until all current tasks finish execution, but leaves the worker threads alive.
        """
        self._tasks.join() # oddly, the API does not support a timeout parameter

    @property
    def is_alive(self):
        """
        True if any of the worker threads are alive.
        """
        for worker in self._workers:
            if worker.is_alive():
                return True
        return False
    
    @property
    def returns(self):
        """
        The returned values from all tasks, in order of submission.
        """
        return [self._returns[k] for k in sorted(self._returns)]

    @property
    def exceptions(self):
        """
        The raised exceptions from all tasks, in order of submission.
        """
        return [self._exceptions[k] for k in sorted(self._exceptions)]

    def raise_first(self):
        """
        If exceptions were thrown by any task, then the first one will be raised.
        
        This is rather arbitrary: proper handling would involve iterating all the
        exceptions. However, if you want to use the "raise" mechanism, you are
        limited to raising only one of them.
        """
        exceptions = self.exceptions
        if exceptions:
            raise exceptions[0]

    def _thread_worker(self):
        while True:
            if not self._execute_next_task():
                break

    def _execute_next_task(self):
        try:
            task = self._tasks.get(timeout=self.timeout)
        except Empty:
            return True
        if task == self._CYANIDE:
            # Time to die :(
            return False
        self._execute_task(*task)
        return True

    def _execute_task(self, id, fn, args, kwargs):
        try:
            r = fn(*args, **kwargs)
            self._returns[id] = r
        except Exception as e:
            self._exceptions[id] = e
            if self.print_exceptions:
                with self._lock:
                    print_exception(e)
        self._tasks.task_done()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        return False


class LockedList(list):
    """
    A list that supports the "with" keyword with a built-in lock.
    
    Though Python lists are thread-safe in that they will not raise exceptions
    during concurrent access, they do not guarantee atomicity. This class will
    let you gain atomicity when needed.
    """

    def __init__(self, *args, **kwargs):
        super(LockedList, self).__init__(*args, **kwargs)
        self.lock = Lock()

    def __enter__(self):
        return self.lock.__enter__()

    def __exit__(self, type, value, traceback):
        return self.lock.__exit__(type, value, traceback)

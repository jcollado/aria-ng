
from threading import Thread, Lock
from collections import OrderedDict
from clint.textui import puts, colored, indent
import sys, linecache

class OpenClose(object):
    """
    Wraps an object that has open() and close() methods to support the "with" keyword.
    """
    
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __enter__(self):
        if hasattr(self.wrapped, 'open'):
            self.wrapped.open()
        return self.wrapped

    def __exit__(self, type, value, traceback):
        if hasattr(self.wrapped, 'close'):
            self.wrapped.close()
        return False

class MultithreadedExecutor(object):
    """
    Executes functions on their own threads.
    
    Makes sure to gather all thrown exceptions in one place.
    """

    # TODO: this is a trivial multithreaded solution, but it would be good enough
    # for many simple use cases. It's not a good solution if you need the threads
    # submitting new threads to the executor, or re-submitting existing threads.
    # Of course, it can be improved by using a Queue with a thread pool.
    
    def __init__(self):
        self.lock = Lock()
        self.threads = []
        self.exceptions = []
        self.print_exceptions = False
    
    def submit(self, fn, args):
        def wrapper(executor, fn, args):
            try:
                fn(*args)
            except Exception as e:
                with executor.lock:
                    executor.exceptions.append(e)
                    if self.print_exceptions:
                        print_exception(e)
        
        thread = Thread(target=wrapper, args=(self, fn, args))
        self.threads.append(thread)
        thread.start()
        return thread

    def join_all(self):
        for thread in self.threads:
            thread.join()
        if self.exceptions:
            raise self.exceptions[0]

class LockedList(list):
    """
    A list that supports the "with" keyword with a built-in lock.
    
    Though Python lists are thread-safe in that they will not raise exceptions
    during concurrent access, they do not guarantee atomicity. This class will
    let you gain atomicity when needed.
    """
    def __init__(self):
        super(LockedList, self).__init__()
        self.lock = Lock()
    
    def __enter__(self):
        return self.lock.__enter__()
        
    def __exit__(self, type, value, traceback):
        return self.lock.__exit__(type, value, traceback)

class ReadOnlyList(list):
    """
    A read-only list.
    
    After initialization it will raise TypeError exceptions if modification
    is attempted.
    """
    def __init__(self, *args, **kwargs):
        self.locked = False
        super(ReadOnlyList, self).__init__(*args, **kwargs)
        self.locked = True

    def __setitem__(self, key, value):
        if self.locked:
            raise TypeError('read-only list')
        return super(ReadOnlyList, self).__setitem__(key, value)

    def __delitem__(self, key):
        if self.locked:
            raise TypeError('read-only list')
        return super(ReadOnlyList, self).__delitem__(key)

class ReadOnlyDict(OrderedDict):
    """
    A read-only ordered dict.
    
    After initialization it will raise TypeError exceptions if modification
    is attempted.
    """
    def __init__(self, *args, **kwargs):
        self.locked = False
        super(ReadOnlyDict, self).__init__(*args, **kwargs)
        self.locked = True

    def __setitem__(self, key, value):
        if self.locked:
            raise TypeError('read-only dict')
        return super(ReadOnlyDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        if self.locked:
            raise TypeError('read-only dict')
        return super(ReadOnlyDict, self).__delitem__(key)

class StrictList(list):
    """
    A list that raises TypeError exceptions when objects of the wrong type are inserted.
    """
    def __init__(self, value_class, items=None, wrapper_fn=None, unwrapper_fn=None):
        super(StrictList, self).__init__()
        self.value_class = value_class
        self.wrapper_fn = wrapper_fn
        self.unwrapper_fn = unwrapper_fn
        if items:
            for item in items:
                self.append(item)

    def __getitem__(self, key):
        value = super(StrictList, self).__getitem__(key)
        if self.unwrapper_fn:
            value = self.unwrapper_fn(value)
        return value
        
    def __setitem__(self, key, value):
        if not isinstance(value, self.value_class):
            raise TypeError('value must be a %s.%s' % (self.value_class.__module__, self.value_class.__name__))
        if self.wrapper_fn:
            value = self.wrapper_fn(value)
        return super(StrictList, self).__setitem__(key, value)

class StrictDict(OrderedDict):
    """
    An ordered dict that raises TypeError exceptions when keys or values of the wrong type are used.
    """
    def __init__(self, key_class, value_class, items=None, wrapper_fn=None, unwrapper_fn=None):
        super(StrictDict, self).__init__()
        self.key_class = key_class
        self.value_class = value_class
        self.wrapper_fn = wrapper_fn
        self.unwrapper_fn = unwrapper_fn
        if items:
            for k, v in items:
                self[k] = v
    
    def __getitem__(self, key):
        if not isinstance(key, self.key_class):
            raise TypeError('key must be a %s.%s' % (self.key_class.__module__, self.key_class.__name__))
        value = super(StrictDict, self).__getitem__(key)
        if self.unwrapper_fn:
            value = self.unwrapper_fn(value)
        return value
        
    def __setitem__(self, key, value):
        if not isinstance(key, self.key_class):
            raise TypeError('key must be a %s.%s' % (self.key_class.__module__, self.key_class.__name__))
        if not isinstance(value, self.value_class):
            raise TypeError('value must be a %s.%s' % (self.value_class.__module__, self.value_class.__name__))
        if self.wrapper_fn:
            value = self.wrapper_fn(value)
        return super(StrictDict, self).__setitem__(key, value)
        
def classname(o):
    """
    The full class name of an object.
    """
    return '%s.%s' % (o.__class__.__module__, o.__class__.__name__)

def merge(a, b, path=None, strict=True):
    """
    Deep merge dicts.
    """
    #TODO: a.add_yaml_merge(b), see https://bitbucket.org/ruamel/yaml/src/86622a1408e0f171a12e140d53c4ffac4b6caaa3/comments.py?fileviewer=file-view-default
    
    if path is None:
        path = []
    for key, value_b in b.iteritems():
        if key in a:
            value_a = a[key]
            if isinstance(value_a, dict) and isinstance(value_b, dict):
                merge(value_a, value_b, path + [str(key)], strict)
            elif strict and (value_a != value_b):
                raise ValueError('dict merge conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = value_b
    return a

def import_class(name, paths=[]):
    """
    Imports a class based on its full name, optionally searching for it in the paths.
    """
    if name is None:
        return None
    
    def do_import(name):
        if name and ('.' in name):
            module_name, class_name = name.rsplit('.', 1)
            return getattr(__import__(module_name, fromlist=[class_name], level=0), class_name)
        else:
            raise ImportError('class not found: %s' % name)
    
    try:
        return do_import(name)
    except:
        for p in paths:
            try:
                return do_import('%s.%s' % (p, name))
            except Exception as e:
                raise ImportError('cannot import class %s, because %s' % (name, e))

    raise ImportError('class not found: %s' % name)

def import_modules(name):
    """
    Imports a module and all its sub-modules, recursively. Relies on modules defining a 'MODULES' attribute
    listing their sub-module names.
    """
    module = __import__(name, fromlist=['MODULES'], level=0)
    if hasattr(module, 'MODULES'):
        for m in module.MODULES:
            import_modules('%s.%s' % (name, m))

def print_exception(e, full=True, cause=False, tb=None):
    """
    Prints the exception with nice colors and such.
    """
    def format(e):
        return '%s%s: %s' % (colored.red('Caused by ') if cause else '', colored.red(e.__class__.__name__, bold=True), colored.red(str(e)))
        
    puts(format(e))
    if full:
        if cause:
            if tb:
                print_traceback(tb)
        else:
            print_traceback()
    if hasattr(e, 'cause') and e.cause:
        tb = e.cause_tb if hasattr(e, 'cause_tb') else None
        print_exception(e.cause, full=full, cause=True, tb=tb)

def print_traceback(tb=None):
    """
    Prints the traceback with nice colors and such.
    """
    if tb is None:
        _, _, tb = sys.exc_info()
    while tb is not None:
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        with indent(2):
            puts('File "%s", line %s, in %s' % (colored.blue(filename), colored.cyan(lineno), colored.cyan(name)))
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            if line:
                with indent(2):
                    puts(colored.black(line.strip()))
        tb = tb.tb_next

def make_agnostic(value):
    if isinstance(value, dict):
        value = dict(value) # makes sure we convert ordereddict to dict
    if isinstance(value, dict):
        for k, v in value.iteritems():
            value[k] = make_agnostic(v)
    if isinstance(value, list):
        for i in range(len(value)):
            value[i] = make_agnostic(value[i])
    return value

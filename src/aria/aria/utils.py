
from clint.textui import puts, colored, indent
from threading import Lock
import sys, traceback, linecache

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

class LockedList(list):
    """
    A list that supports the "with" keyword with a built-in lock.
    """
    def __init__(self):
        super(LockedList, self).__init__()
        self.lock = Lock()
    
    def __enter__(self):
        return self.lock.__enter__()
        
    def __exit__(self, type, value, traceback):
        return self.lock.__exit__(type, value, traceback)
        
def classname(o):
    """
    The full class name of an object.
    """
    return o.__module__ + '.' + o.__class__.__name__

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


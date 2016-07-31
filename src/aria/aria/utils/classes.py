
from functools32 import lru_cache

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
        
def classname(o):
    """
    The full class name of an object.
    """
    
    return '%s.%s' % (o.__class__.__module__, o.__class__.__name__)

cachedmethod = lru_cache()

class HasCachedMethods(object):
    @property
    def _method_cache_info(self):
        """
        The cache infos of all cached methods.
        
        :rtype: dict of str, CacheInfo
        """
        
        r = {}
        for k in self.__class__.__dict__:
            p = getattr(self, k)
            if hasattr(p, 'cache_info'):
                r[k] = p.cache_info()
        return r

    def _reset_method_cache(self):
        """
        Resets the caches of all cached methods.
        """
        
        for k in self.__class__.__dict__:
            p = getattr(self, k)
            if hasattr(p, 'cache_clear'):
                p.cache_clear()

#
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from functools import partial
from threading import Lock
from collections import OrderedDict

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

    def __exit__(self, the_type, value, traceback):
        if hasattr(self.wrapped, 'close'):
            self.wrapped.close()
        return False
        
def classname(o):
    """
    The full class name of an object.
    """
    
    return '%s.%s' % (o.__class__.__module__, o.__class__.__name__)

#cachedmethod = lambda x: x

class cachedmethod(object):
    """
    Decorator for caching method return values.
    
    Supports :code:`cache_info` to be compatible with Python 3's :code:`functools.lru_cache`. The statistics are
    combined for all instances of the class.
    
    Won't use the cache if not called when bound to an object, allowing you to override the cache.
    
    Adapted from `this solution <http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/>`__.
    """
    
    def __init__(self, func):
        self.func = func
        self.hits = 0
        self.misses = 0
        self.lock = Lock()

    def cache_info(self):
        with self.lock:
            return (self.hits, self.misses, None, self.misses)
    
    def reset_cache_info(self):
        with self.lock:
            self.hits = 0
            self.misses = 0

    def __get__(self, obj, objtype=None):
        if obj is None:
            # Don't use cache if not bound to an object
            return self.func
        return partial(self, obj)
    
    def __call__(self, *args, **kw):
        instance = args[0]
        
        try:
            cache = instance._method_cache
        except AttributeError:
            cache = {}
            instance._method_cache = cache
            
        key = (self.func, args[1:], frozenset(kw.items()))
        
        try:
            r = cache[key]
            with self.lock:
                self.hits += 1
        except KeyError:
            r = cache[key] = self.func(*args, **kw)
            with self.lock:
                self.misses += 1
                
        return r

class HasCachedMethods(object):
    """
    Provides convenience methods for working with :class:`cachedmethod`.
    """
    
    @property
    def _method_cache_info(self):
        """
        The cache infos of all cached methods.
        
        :rtype: dict of str, 4-tuple
        """
        
        r = OrderedDict()
        for k, p in self.__class__.__dict__.iteritems():
            if isinstance(p, property):
                # The property getter might be cached
                p = p.fget
            if hasattr(p, 'cache_info'):
                r[k] = p.cache_info()
        return r

    def _reset_method_cache(self):
        """
        Resets the caches of all cached methods.
        """
        
        if hasattr(self, '_method_cache'):
            delattr(self, '_method_cache')
        
        for p in self.__class__.__dict__.itervalues():
            if isinstance(p, property):
                # The property getter might be cached
                p = p.fget
            if hasattr(p, 'reset_cache_info'):
                p.reset_cache_info()


from __future__ import absolute_import # so we can import standard 'collections'

from collections import OrderedDict
from copy import deepcopy

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

EMPTY_READ_ONLY_LIST = ReadOnlyList()

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

EMPTY_READ_ONLY_DICT = ReadOnlyDict()

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

    def append(self, value):
        if not isinstance(value, self.value_class):
            raise TypeError('value must be a %s.%s' % (self.value_class.__module__, self.value_class.__name__))
        if self.wrapper_fn:
            value = self.wrapper_fn(value)
        return super(StrictList, self).append(value)

class StrictDict(OrderedDict):
    """
    An ordered dict that raises TypeError exceptions when keys or values of the wrong type are used.
    """
    
    def __init__(self, key_class, value_class=None, items=None, wrapper_fn=None, unwrapper_fn=None):
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
        if self.value_class is not None:
            if not isinstance(value, self.value_class):
                raise TypeError('value must be a %s.%s' % (self.value_class.__module__, self.value_class.__name__))
        if self.wrapper_fn:
            value = self.wrapper_fn(value)
        return super(StrictDict, self).__setitem__(key, value)

def merge(a, b, path=[], strict=False):
    """
    Merges dicts, recursively.
    """
    
    # TODO: a.add_yaml_merge(b), see https://bitbucket.org/ruamel/yaml/src/86622a1408e0f171a12e140d53c4ffac4b6caaa3/comments.py?fileviewer=file-view-default
    
    for key, value_b in b.iteritems():
        if key in a:
            value_a = a[key]
            if isinstance(value_a, dict) and isinstance(value_b, dict):
                merge(value_a, value_b, path + [str(key)], strict)
            elif value_a != value_b:
                if strict:
                    raise ValueError('dict merge conflict at %s' % '.'.join(path + [str(key)]))
                else:
                    a[key] = value_b
        else:
            a[key] = value_b
    return a

def deepclone(value):
    """
    Copies dicts and lists, recursively.
    
    If the value uses dict or list subclasses, they are used for the clone.
    
    Makes sure to copy over "\_locator" for all elements.
    """
    
    if isinstance(value, dict):
        r = []
        for k, v in value.iteritems():
            r.append((k, deepclone(v)))
        r = value.__class__(r)
    elif isinstance(value, list):
        r = []
        for v in value:
            r.append(deepclone(v))
        r = value.__class__(r)
    else:
        r = deepcopy(value)
    
    locator = getattr(value, '_locator', None)
    if locator is not None:
        try:
            setattr(r, '_locator', locator)
        except AttributeError:
            pass
        
    return r

def make_agnostic(value):
    """
    Converts subclasses of dict and list to standard dicts and lists, recursively.
    """
    
    if isinstance(value, dict) and (type(value) != dict):
        value = dict(value)
    elif isinstance(value, list) and (type(value) != list):
        value = list(value)
        
    if isinstance(value, dict):
        for k, v in value.iteritems():
            value[k] = make_agnostic(v)
    elif isinstance(value, list):
        for i in range(len(value)):
            value[i] = make_agnostic(value[i])
            
    return value

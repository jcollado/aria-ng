
def get_raw(raw, name, default=None):
    return raw.get(name, default)

def get_primitive(raw, name, default=None):
    return raw.get(name, default)

def get_primitive_list(raw, name, default=None):
    return raw.get(name) or default

def get_object(raw, name, cls, default=None):
    raw = raw.get(name)
    return cls(raw) if raw else default

def get_object_list(raw, name, cls, default=None):
    raws = raw.get(name)
    return [cls(raw) for raw in raws] if raws else default

def get_object_dict(raw, name, cls, default=None):
    raws = raw.get(name)
    return {k: cls(raw) for k, raw in raws.iteritems()} if raws else default

def has_properties(cls):
    """
    Class decorator.
    """
    
    # Make sure we have PROPERTIES
    if not hasattr(cls, 'PROPERTIES'):
        cls.PROPERTIES = {}
    
    # Inherit PROPERTIES from base classes 
    for base in cls.__bases__:
        if hasattr(base, 'PROPERTIES'):
            cls.PROPERTIES.update(base.PROPERTIES)
    
    for name, p in cls.__dict__.iteritems():
        if isinstance(p, Property):
            # Accumulate
            cls.PROPERTIES[name] = p
            
            # Convert to Python property
            if p.type == 'raw':
                def closure(name, p):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_raw(this.raw, name, default=p.default)
                    return the_property
                setattr(cls, name, closure(name, p))
                
            elif p.type == 'primitive':
                def closure(name, p):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_primitive(this.raw, name, default=p.default)
                    return the_property
                setattr(cls, name, closure(name, p))
                
            elif p.type == 'primitive_list':
                def closure(name, p):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_primitive_list(this.raw, name, default=p.default)
                    return the_property
                setattr(cls, name, closure(name, p))
                
            elif p.type == 'object':
                def closure(name, p):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_object(this.raw, name, p.cls, default=p.default)
                    return the_property
                setattr(cls, name, closure(name, p))
                
            elif p.type == 'object_list':
                def closure(name, p):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_object_list(this.raw, name, p.cls, default=p.default)
                    return the_property
                setattr(cls, name, closure(name, p))
                
            elif p.type == 'object_dict':
                def closure(name, p):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_object_dict(this.raw, name, p.cls, default=p.default)
                    return the_property
                setattr(cls, name, closure(name, p))
                
            else:
                raise AttributeError('Unsupported Property type: %s' % p.type)
                
    return cls

def property_raw(f):
    return Property('raw')

def property_primitive(f):
    return Property('primitive')

def property_primitive_default(default):
    def decorator(f):
        return Property('primitive', default=default)
    return decorator

def property_primitive_list(f):
    return Property('primitive_list')

def property_object(cls):
    def decorator(f):
        return Property('object', cls=cls)
    return decorator

def property_object_list(cls):
    def decorator(f):
        return Property('object_list', cls=cls)
    return decorator

def property_object_dict(cls):
    def decorator(f):
        return Property('object_dict', cls=cls)
    return decorator

def required(f):
    if isinstance(f, Property):
        f.required = True
        return f
    else:
        raise AttributeError('@required must be used with a Property')

class HasRaw(object):
    def __init__(self, raw={}):
        self.raw = raw

class Property(object):
    def __init__(self, type, default=None, cls=None, required=False):
        self.type = type
        self.default = default
        self.cls = cls
        self.required = required

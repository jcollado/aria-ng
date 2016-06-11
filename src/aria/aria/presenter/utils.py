
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

def has_fields(cls):
    """
    Class decorator for presentations.
    """
    
    # Make sure we have PROPERTIES
    if not hasattr(cls, 'PROPERTIES'):
        cls.PROPERTIES = {}
    
    # Inherit PROPERTIES from base classes 
    for base in cls.__bases__:
        if hasattr(base, 'PROPERTIES'):
            cls.PROPERTIES.update(base.PROPERTIES)
    
    for name, field in cls.__dict__.iteritems():
        if isinstance(field, Field):
            # Accumulate
            cls.PROPERTIES[name] = field
            
            # Convert to Python property
            if field.type == 'raw':
                def closure(name, field):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_raw(this.raw, name, default=field.default)
                    return the_property
                setattr(cls, name, closure(name, field))
                
            elif field.type == 'primitive':
                def closure(name, field):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_primitive(this.raw, name, default=field.default)
                    return the_property
                setattr(cls, name, closure(name, field))
                
            elif field.type == 'primitive_list':
                def closure(name, field):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_primitive_list(this.raw, name, default=field.default)
                    return the_property
                setattr(cls, name, closure(name, field))
                
            elif field.type == 'object':
                def closure(name, field):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_object(this.raw, name, field.cls, default=field.default)
                    return the_property
                setattr(cls, name, closure(name, field))
                
            elif field.type == 'object_list':
                def closure(name, field):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_object_list(this.raw, name, field.cls, default=field.default)
                    return the_property
                setattr(cls, name, closure(name, field))
                
            elif field.type == 'object_dict':
                def closure(name, field):
                    @property
                    def the_property(*args):
                        this = args[0] # First argument is 'self'
                        return get_object_dict(this.raw, name, field.cls, default=field.default)
                    return the_property
                setattr(cls, name, closure(name, field))
                
            else:
                raise AttributeError('Unsupported Field type: %s' % field.type)
                
    return cls

def raw_field(f):
    return Field('raw')

def primitive_field(f):
    return Field('primitive')

def primitive_field_with_default(default):
    def decorator(f):
        return Field('primitive', default=default)
    return decorator

def primitive_list_field(f):
    return Field('primitive_list')

def object_field(cls):
    def decorator(f):
        return Field('object', cls=cls)
    return decorator

def object_list_field(cls):
    def decorator(f):
        return Field('object_list', cls=cls)
    return decorator

def object_dict_field(cls):
    def decorator(f):
        return Field('object_dict', cls=cls)
    return decorator

def required_field(f):
    if isinstance(f, Field):
        f.required = True
        return f
    else:
        raise AttributeError('@required_field must be used with a Field')

class Presentation(object):
    def __init__(self, raw={}):
        self.raw = raw
        
    def validate(self):
        # TODO
        pass

class Field(object):
    def __init__(self, type, default=None, cls=None, required=False):
        self.type = type
        self.default = default
        self.cls = cls
        self.required = required

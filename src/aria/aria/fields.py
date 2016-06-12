
from issue import Issue
from exceptions import InvalidValueError
from functools import wraps
from types import MethodType
from collections import OrderedDict

def get_location(raw, name):
    if hasattr(raw, '_map'):
        map = raw._map
        map = map.children.get(name, map)
        return str(map)
    return '<unknown>'

class Field(object):
    def __init__(self, fn, type, cls=None, name=None, default=None, required=False):
        self.fn = fn
        self.type = type
        self.cls = cls
        self.name = name
        self.default = default
        self.required = required
    
    def get(self, raw):
        return self._get(raw)
    
    def _get(self, raw):
        if not isinstance(raw, dict):
            # Only dicts are supported
            return None
        
        value = raw.get(self.name, self.default)

        if value is None:
            if self.required:
                raise InvalidValueError('Required field must have a value: %s, at %s' % (self.name, get_location(raw, self.name)))
            else:
                return None

        if self.type == 'primitive':
            if self.cls and not isinstance(value, self.cls):
                try:
                    return self.cls(value)
                except ValueError:
                    raise InvalidValueError('Field must be coercible to %s: %s=%s' % (self.cls.__name__, self.name, repr(value)))
            return value

        elif self.type == 'primitive_list':
            if not isinstance(value, list):
                raise InvalidValueError('Field must be a list: %s=%s' % (self.name, repr(value)))
            if self.cls:
                for i in range(len(value)):
                    if not InvalidValueError(value[i], self.cls):
                        try:
                            value[i] = self.cls(value[i])
                        except ValueError:
                            raise InvalidValueError('Field must be coercible to a list of %s: %s[%d]=%s' % (self.cls.__name__, self.name, i, repr(value[i])))
            return value

        elif self.type == 'object':
            return self.cls(value)

        elif self.type == 'object_list':
            if not isinstance(value, list):
                raise InvalidValueError('Field must be a list: %s=%s' % (self.name, repr(value)))
            return [self.cls(v) for v in value]

        elif self.type == 'object_dict':
            if not isinstance(value, dict):
                raise InvalidValueError('Field must be a dict: %s=%s' % (self.name, repr(value)))
            return OrderedDict([(k, self.cls(v)) for k, v in value.iteritems()])
            
        else:
            raise AttributeError('Unsupported field type: %s' % self.type)

    def set(self, raw, value):
        old = raw.get(self.name)
        raw[self.name] = value
        try:
            # Validates our value
            self.get(raw)
        except Exception as e:
            raw[self.name] = old
            raise e
        return old

    def validate(self, presentation, issues):
        self._validate(presentation, issues)
    
    def _validate(self, presentation, issues):
        value = None
        
        try:
            value = getattr(presentation, self.name)
        except InvalidValueError as e:
            issues.append(Issue(str(e), exception=e))
            
        if isinstance(value, list):
            for v in value:
                if hasattr(v, 'validate'):
                    v.validate(issues)
        elif isinstance(value, dict):
            for v in value.itervalues():
                if hasattr(v, 'validate'):
                    v.validate(issues)
        elif hasattr(value, 'validate'):
            value.validate(issues)

def has_fields(cls):
    """
    Class decorator for field support.
    
    1. Adds a `FIELDS` class property that is a dict of all the fields.
       Will inherit and merge `FIELDS` properties from base classes if
       they have them.
    
    2. Generates automatic `@property` implementations for the fields
       with the help of a set of special function decorators.
    """
    
    # Make sure we have FIELDS
    if not hasattr(cls, 'FIELDS'):
        cls.FIELDS = {}
    
    # Inherit FIELDS from base classes 
    for base in cls.__bases__:
        if hasattr(base, 'FIELDS'):
            cls.FIELDS.update(base.FIELDS)
    
    for name, field in cls.__dict__.iteritems():
        if isinstance(field, Field):
            # Accumulate
            cls.FIELDS[name] = field
            
            field.name = name
            
            # Convert to Python property
            def closure(field):
                # By convention, we will have the getter wrap the original function.
                # (It is, for example, where the Python help() function will look for
                # docstrings.)

                @wraps(field.fn)
                def getter(self):
                    return field.get(self.raw)
                    
                def setter(self, value):
                    field.set(self.raw, value)

                return property(fget=getter, fset=setter)

            setattr(cls, name, closure(field))
                
    return cls

def primitive_field(f):
    """
    Function decorator for primitive fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    return Field(f, 'primitive')

def primitive_list_field(f):
    """
    Function decorator for list of primitive fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    return Field(f, 'primitive_list')

def object_field(cls):
    """
    Function decorator for object fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(f):
        return Field(f, 'object', cls)
    return decorator

def object_list_field(cls):
    """
    Function decorator for list of object fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(f):
        return Field(f, 'object_list', cls)
    return decorator

def object_dict_field(cls):
    """
    Function decorator for dict of object fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(f):
        return Field(f, 'object_dict', cls)
    return decorator

def field_type(type):
    """
    Function decorator for setting the type of a field.
    
    The function must already be decorated with :func:`primitive\_field` or :func:`primitive\_list\_field`.
    """
    def decorator(f):
        if isinstance(f, Field):
            f.cls = type
            return f
        else:
            raise AttributeError('@field_type must be used with a Field')
    return decorator

def field_getter(getter_fn):
    """
    Function decorator for overriding the getter function of a field.
    
    The signature of the getter function must be: f(field, raw).
    
    The function must already be decorated with a field decorator.
    """
    def decorator(f):
        if isinstance(f, Field):
            f.get = MethodType(getter_fn, f, Field)
            return f
        else:
            raise AttributeError('@field_validator must be used with a Field')
    return decorator

def field_validator(validator_fn):
    """
    Function decorator for overriding the validator function of a field.
    
    The signature of the validator function must be: f(field, presentation, issues).
    
    The function must already be decorated with a field decorator.
    """
    def decorator(f):
        if isinstance(f, Field):
            f.validate = MethodType(validator_fn, f, Field)
            return f
        else:
            raise AttributeError('@field_validator must be used with a Field')
    return decorator

def field_default(default):
    """
    Function decorator for setting the default value of a field.
    
    The function must already be decorated with a field decorator.
    """
    def decorator(f):
        if isinstance(f, Field):
            f.default = default
            return f
        else:
            raise AttributeError('@field_default must be used with a Field')
    return decorator

def required_field(f):
    """
    Function decorator for setting the field as required.
    
    The function must already be decorated with a field decorator.
    """
    if isinstance(f, Field):
        f.required = True
        return f
    else:
        raise AttributeError('@required_field must be used with a Field')


from .exceptions import InvalidValueError
from functools import wraps
from types import MethodType
from collections import OrderedDict

class Prop(object):
    def __init__(self, fn=None, cls=None, status='supported', name=None, default=None, required=False):
        self.fn = fn
        self.cls = cls
        self.name = name
        self.default = default
        self.required = False
    
    def validate(self, value):
        if value is None:
            if self.required:
                raise InvalidValueError('required property must have a value: %s' % self.name)
            else:
                return None

        if self.cls and not isinstance(value, self.cls):
            try:
                return self.cls(value)
            except ValueError:
                raise InvalidValueError('property must be coercible to %s: %s=%s' % (self.cls.__name__, self.name, repr(value)))

        return value

def has_validated_properties_iter_validated_property_names(self):
    for name in self.__class__.PROPERTIES:
        yield name

def has_validated_properties_iter_validated_properties(self):
    for name in self.__class__.PROPERTIES:
        yield name, self.__dict__[name]

def has_validated_properties(cls):
    """
    Class decorator for validated property support.
    
    1. Adds a `PROPERTIES` class property that is a dict of all the fields.
       Will inherit and merge `PROPERTIES` properties from base classes if
       they have them.
    
    2. Generates automatic `@property` implementations for the fields
       with the help of a set of special function decorators.

    The class will also gain two utility methods,
    `iter_validated_property_names` and `iter_validated_properties`.
    """

    # Make sure we have PROPERTIES
    if not hasattr(cls, 'PROPERTIES'):
        cls.PROPERTIES = OrderedDict()
    
    # Inherit PROPERTIES from base classes 
    for base in cls.__bases__:
        if hasattr(base, 'PROPERTIES'):
            cls.PROPERTIES.update(base.PROPERTIES)
    
    for name, prop in cls.__dict__.iteritems():
        if isinstance(prop, Prop):
            # Accumulate
            cls.PROPERTIES[name] = prop
            
            prop.name = name

            # Convert to Python property
            def closure(prop):
                # By convention, we will have the getter wrap the original function.
                # (It is, for example, where the Python help() function will look for
                # docstrings.)

                @wraps(prop.fn)
                def getter(self):
                    value = getattr(self, '_' + prop.name)
                    if value is None:
                        value = prop.default
                        setattr(self, '_' + prop.name, value)
                    return prop.validate(value)
                    
                def setter(self, value):
                    value = prop.validate(value)
                    setattr(self, '_' + prop.name, value)
                    
                return property(fget=getter, fset=setter)
                
            setattr(cls, name, closure(prop))

    # Bind methods
    setattr(cls, 'iter_validated_property_names', MethodType(has_validated_properties_iter_validated_property_names, None, cls))
    setattr(cls, 'iter_validated_properties', MethodType(has_validated_properties_iter_validated_properties, None, cls))
                
    return cls

def validated_property(f):
    """
    Function decorator for primitive fields.
    
    The function must be a method in a class decorated with :func:`has\_validated\_properties`.
    """
    return Prop(fn=f)

def property_type(cls):
    """
    Function decorator for setting the type of a property.
    
    The function must already be decorated with :func:`validated\_property`.
    """
    def decorator(f):
        if isinstance(f, Prop):
            f.cls = cls
            return f
        else:
            raise AttributeError('@property_type must be used with a validated propery')
    return decorator

def property_default(default):
    """
    Function decorator for setting the default value of a property.
    
    The function must already be decorated with :func:`validated\_property`.
    """
    def decorator(f):
        if isinstance(f, Prop):
            f.default = default
            return f
        else:
            raise AttributeError('@property_default must be used with a validated propery')
    return decorator

def property_status(status):
    """
    Function decorator for setting the default value of a property.
    
    The function must already be decorated with  func:`validated\_property`.
    """
    def decorator(f):
        if isinstance(f, Prop):
            f.status = status
            return f
        else:
            raise AttributeError('@property_status must be used with a validated propery')
    return decorator

def required_property(f):
    """
    Function decorator for setting the property as required.
    
    The function must already be decorated with a :func:`validated\_property`.
    """
    if isinstance(f, Prop):
        f.required = True
        return f
    else:
        raise AttributeError('@required_property must be used with a validated propery')


from ..issue import Issue
from ..exceptions import InvalidValueError
from ..utils import ReadOnlyList, ReadOnlyDict
from functools import wraps
from types import MethodType
from collections import OrderedDict

class Field(object):
    def __init__(self, type, fn, cls=None, default=None, allowed=None, required=False):
        self.container = None
        self.name = None
        self.type = type
        self.fn = fn
        self.cls = cls
        self.default = default
        self.allowed = allowed
        self.required = required
    
    def get(self, raw):
        return self._get(raw)
    
    def _get(self, raw):
        short_form = (self.container.SHORT_FORM_FIELD == self.name) if hasattr(self.container, 'SHORT_FORM_FIELD') else False

        if short_form:
            value = raw
        else:
            if isinstance(raw, dict):
                value = raw.get(self.name, self.default)
            else:
                value = None

        if value is None:
            if self.required:
                raise InvalidValueError('required %s must have a value' % self.fullname, map=self.get_map(raw))
            else:
                return None
        
        if self.allowed is not None:
            if value not in self.allowed:
                raise InvalidValueError('%s must be %s' % (self.fullname, ' or '.join([repr(v) for v in self.allowed])), map=self.get_map(raw))

        if self.type == 'primitive':
            if self.cls and not isinstance(value, self.cls):
                try:
                    return self.cls(value)
                except ValueError:
                    raise InvalidValueError('%s must be coercible to %s: %s' % (self.fullname, self.fullclass, repr(value)), map=self.get_map(raw))
            return value

        elif self.type == 'primitive_list':
            if not isinstance(value, list):
                location = self._get_location(raw)
                raise InvalidValueError('%s must be a list: %s' % (self.fullname, repr(value)), map=self.get_map(raw))
            if self.cls:
                for i in range(len(value)):
                    if not isinstance(value[i], self.cls):
                        try:
                            value[i] = self.cls(value[i])
                        except ValueError:
                            raise InvalidValueError('%s must be coercible to a list of %s: element %d is %s' % (self.fullname, self.fullclass, i, repr(value[i])), map=self.get_map(raw))
            return ReadOnlyList(value)

        elif self.type == 'object':
            try:
                return self.cls(raw=value)
            except TypeError as e:
                raise InvalidValueError('could not initialize %s to type %s: %s' % (self.fullname, self.fullclass), cause=e, map=self.get_map(raw))

        elif self.type == 'object_list':
            if not isinstance(value, list):
                raise InvalidValueError('%s must be a list: %s' % (self.fullname, repr(value)), map=self.get_map(raw))
            return ReadOnlyList([self.cls(raw=v) for v in value])

        elif self.type == 'object_dict':
            if not isinstance(value, dict):
                raise InvalidValueError('%s must be a dict: %s' % (self.fullname, repr(value)), map=self.get_map(raw))
            return ReadOnlyDict([(k, self.cls(name=k, raw=v)) for k, v in value.iteritems()])
            
        else:
            map = self.get_map(raw)
            location = (', at %s' % map) if map is not None else ''
            raise AttributeError('%s has unsupported type: %s%s' % (self.fullname, self.type, location))

    def set(self, raw, value):
        return self._set(raw, value)

    def _set(self, raw, value):
        old = raw.get(self.name)
        raw[self.name] = value
        try:
            # Validates our value
            self.get(raw)
        except Exception as e:
            raw[self.name] = old
            raise e
        return old

    def validate(self, presentation, consumption_context):
        self._validate(presentation, consumption_context)
    
    def _validate(self, presentation, consumption_context):
        value = None
        
        try:
            value = getattr(presentation, self.name)
        except Exception as e:
            if hasattr(e, 'issue') and isinstance(e.issue, Issue):
                consumption_context.validation.issues.append(e.issue)
            else:
                consumption_context.validation.issues.append(Issue(exception=e))
            
        if isinstance(value, list):
            for v in value:
                if hasattr(v, '_validate'):
                    v._validate(consumption_context)
        elif isinstance(value, dict):
            for v in value.itervalues():
                if hasattr(v, '_validate'):
                    v._validate(consumption_context)
        elif hasattr(value, '_validate'):
            value._validate(consumption_context)

    @property
    def fullname(self):
        return 'field "%s" in %s.%s' % (self.name, self.container.__module__, self.container.__name__)

    @property
    def fullclass(self):
        return '%s.%s' % (self.cls.__module__, self.cls.__name__)

    def get_map(self, raw):
        if hasattr(raw, '_map'):
            return raw._map.children.get(self.name) or raw._map
        return None
    
def has_fields_iter_field_names(self):
    for name in self.__class__.FIELDS:
        yield name

def has_fields_iter_fields(self):
    return self.FIELDS.iteritems()

def has_fields_len(self):
    return len(self.__class__.FIELDS)

def has_fields_getitem(self, key):
    if not isinstance(key, basestring):
        raise TypeError('key must be a string')
    if key not in self.__class__.FIELDS:
        raise KeyError('no \'%s\' property' % key)
    return getattr(self, key)

def has_fields_setitem(self, key, value):
    if not isinstance(key, basestring):
        raise TypeError('key must be a string')
    if key not in self.__class__.FIELDS:
        raise KeyError('no \'%s\' property' % key)
    return setattr(self, key, value)

def has_fields_delitem(self, key):
    if not isinstance(key, basestring):
        raise TypeError('key must be a string')
    if key not in self.__class__.FIELDS:
        raise KeyError('no \'%s\' property' % key)
    return setattr(self, key, None)

def has_fields_iter(self):
    return self.__class__.FIELDS.iterkeys()

def has_fields_contains(self, key):
    if not isinstance(key, basestring):
        raise TypeError('key must be a string')
    return key in self.__class__.FIELDS

def has_fields(cls):
    """
    Class decorator for validated field support.
    
    1. Adds a `FIELDS` class property that is a dict of all the fields.
       Will inherit and merge `FIELDS` properties from base classes if
       they have them.
    
    2. Generates automatic `@property` implementations for the fields
       with the help of a set of special function decorators.

    The class also works with the Python dict protocol, so that
    fields can be accessed via dict semantics. The functionality is
    identical to that of using attribute access.

    The class will also gain two utility methods, `_iter_field_names`
    and `_iter_fields`.
    """
    
    # Make sure we have FIELDS
    if 'FIELDS' not in cls.__dict__:
        setattr(cls, 'FIELDS', OrderedDict())
    
    # Inherit FIELDS from base classes 
    for base in cls.__bases__:
        if hasattr(base, 'FIELDS'):
            cls.FIELDS.update(base.FIELDS)
    
    for name, field in cls.__dict__.iteritems():
        if isinstance(field, Field):
            # Accumulate
            cls.FIELDS[name] = field
            
            field.name = name
            field.container = cls
            
            # Convert to Python property
            def closure(field):
                # By convention, we will have the getter wrap the original function.
                # (It is, for example, where the Python help() function will look for
                # docstrings.)

                @wraps(field.fn)
                def getter(self):
                    return field.get(self._raw)
                    
                def setter(self, value):
                    field.set(self._raw, value)

                return property(fget=getter, fset=setter)

            setattr(cls, name, closure(field))

    # Bind methods
    setattr(cls, '_iter_field_names', MethodType(has_fields_iter_field_names, None, cls))
    setattr(cls, '_iter_fields', MethodType(has_fields_iter_fields, None, cls))
    
    # Behave like a dict
    setattr(cls, '__len__', MethodType(has_fields_len, None, cls))
    setattr(cls, '__getitem__', MethodType(has_fields_getitem, None, cls))
    setattr(cls, '__setitem__', MethodType(has_fields_setitem, None, cls))
    setattr(cls, '__delitem__', MethodType(has_fields_delitem, None, cls))
    setattr(cls, '__iter__', MethodType(has_fields_iter, None, cls))
    setattr(cls, '__contains__', MethodType(has_fields_contains, None, cls))
    
    return cls

def short_form_field(name):
    """
    Class decorator for specifying the short form field.
    
    The class must be decorated with :func:`has\_fields`.
    """
    def decorator(cls):
        if hasattr(cls, name) and hasattr(cls, 'FIELDS') and (name in cls.FIELDS):
            setattr(cls, 'SHORT_FORM_FIELD', name)
            return cls
        else:
            raise AttributeError('@short_form_field must be used with a @property name')
    return decorator

def primitive_field(cls=None, default=None, allowed=None, required=False):
    """
    Function decorator for primitive fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(fn):
        return Field(type='primitive', fn=fn, cls=cls, default=default, allowed=allowed, required=required)
    return decorator

def primitive_list_field(cls=None, default=None, allowed=None, required=False):
    """
    Function decorator for list of primitive fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(fn):
        return Field(type='primitive_list', fn=fn, cls=cls, default=default, allowed=allowed, required=required)
    return decorator

def object_field(cls, default=None, allowed=None, required=False):
    """
    Function decorator for object fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(fn):
        return Field(type='object', fn=fn, cls=cls, default=default, allowed=allowed, required=required)
    return decorator

def object_list_field(cls, default=None, allowed=None, required=False):
    """
    Function decorator for list of object fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(fn):
        return Field(type='object_list', fn=fn, cls=cls, default=default, allowed=allowed, required=required)
    return decorator

def object_dict_field(cls, default=None, allowed=None, required=False):
    """
    Function decorator for dict of object fields.
    
    The function must be a method in a class decorated with :func:`has\_fields`.
    """
    def decorator(fn):
        return Field(type='object_dict', fn=fn, cls=cls, default=default, allowed=allowed, required=required)
    return decorator

def field_getter(getter_fn):
    """
    Function decorator for overriding the getter function of a field.
    
    The signature of the getter function must be: f(field, raw).
    The default getter can be accessed as field.\_get().
    
    The function must already be decorated with a field decorator.
    """
    def decorator(field):
        if isinstance(field, Field):
            field.get = MethodType(getter_fn, field, Field)
            return field
        else:
            raise AttributeError('@field_getter must be used with a Field')
    return decorator

def field_setter(setter_fn):
    """
    Function decorator for overriding the setter function of a field.
    
    The signature of the setter function must be: f(field, raw, value).
    The default setter can be accessed as field.\_set().
    
    The function must already be decorated with a field decorator.
    """
    def decorator(field):
        if isinstance(field, Field):
            field.set = MethodType(setter_fn, field, Field)
            return field
        else:
            raise AttributeError('@field_setter must be used with a Field')
    return decorator

def field_validator(validator_fn):
    """
    Function decorator for overriding the validator function of a field.
    
    The signature of the validator function must be: f(field, presentation, consumption_context).
    The default validator can be accessed as field.\_validate().
    
    The function must already be decorated with a field decorator.
    """
    def decorator(field):
        if isinstance(field, Field):
            field.validate = MethodType(validator_fn, field, Field)
            return field
        else:
            raise AttributeError('@field_validator must be used with a Field')
    return decorator

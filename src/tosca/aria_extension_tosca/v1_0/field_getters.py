
from aria import InvalidValueError

def data_type_class_getter(cls):
    """
    Wraps the field value in a specialized data type class.

    Can be used with the :func:`field_getter` decorator.
    """
    
    def getter(field, presentation):
        raw = field._get(presentation)
        if raw is not None:
            try:
                return cls(None, None, raw, None)
            except ValueError as e:
                raise InvalidValueError('%s is not a valid "%s.%s" in "%s": %s' % (field.fullname, cls.__module__, cls.__name__, presentation._name, repr(raw)), cause=e, locator=field.get_locator(raw))
    return getter


from .utils.data_types import coerce_data_type_value
from aria import Issue, InvalidValueError

def data_type_class_getter(cls):
    """
    Wraps the field value in a specialized data type class.
    """
    
    def getter(field, presentation):
        raw = field._get(presentation)
        if raw is not None:
            try:
                return cls(None, None, raw, None)
            except ValueError as e:
                raise InvalidValueError('%s is not a valid "%s.%s" in "%s": %s' % (field.fullname, cls.__module__, cls.__name__, presentation._name, repr(raw)), cause=e, locator=field.get_locator(raw))
    return getter

def data_type_getter(context, presentation, field_name, type_name):
    the_type = context.presentation.datatypes.get(type_name) if context.presentation.datatypes is not None else None
    if the_type is not None:
        value = getattr(presentation, field_name)
        if value is not None:
            return coerce_data_type_value(context, presentation, the_type, None, None, value, None)
    else:
        context.validation.report('field "%s" in "%s" refers to unknown data type "%s"' % (field_name, presentation._fullname, type_name), locator=presentation._locator, level=Issue.BETWEEN_TYPES)
    return None

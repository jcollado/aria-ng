
from ..functions import get_function
from aria import Issue
from aria.utils import import_fullname
from collections import OrderedDict

#
# DataType
#

def coerce_data_type_value(context, presentation, data_type, value, aspect):
    """
    Handles the :code:`_coerce_data()` hook for complex data types.
    
    We return the assigned property values while making
    sure they are defined in our type. The property definition's default value, if available, will
    be used if we did not assign it. We also make sure that required definitions indeed end up with
    a value.
    """
    
    definitions = data_type._get_properties(context)
    if isinstance(value, dict):
        r = OrderedDict()

        # Fill in our values, but make sure they are defined
        for name, v in value.iteritems():
            if name in definitions:
                definition = definitions[name]
                definition_type = definition._get_type(context)
                r[name] = coerce_value(context, presentation, definition_type, v)
            else:
                context.validation.report('assignment to undefined property "%s" in type "%s" in "%s"' % (name, data_type._fullname, presentation._fullname), locator=v._locator, level=Issue.BETWEEN_TYPES)

        # Fill in defaults from the definitions, and check if required definitions have not been assigned
        for name, definition in definitions.iteritems():
            if (r.get(name) is None) and hasattr(definition, 'default') and (definition.default is not None):
                definition_type = definition._get_type(context)
                r[name] = coerce_value(context, presentation, definition_type, definition.default)

            if getattr(definition, 'required', False) and (r.get(name) is None):
                context.validation.report('required property "%s" in type "%s" is not assigned a value in "%s"' % (name, data_type._fullname, presentation._fullname), locator=presentation._get_child_locator('definitions'), level=Issue.BETWEEN_TYPES)
        
        value = r
    else:
        context.validation.report('value of type "%s" is not a dict in "%s"' % (data_type._fullname, presentation._fullname), locator=value._locator, level=Issue.BETWEEN_TYPES)
        value = None
    
    return value

#
# PropertyDefinition
#

def get_data_type(context, presentation, field_name, allow_none=False):
    """
    Returns the type, whether it's a complex data type (a DataType instance) or a primitive (a Python primitive type class).
    
    If the type is not specified, defaults to :class:`str`.
    """
    
    the_type = getattr(presentation, field_name)
    
    if the_type is None:
        if allow_none:
            return None
        else:
            return str
    
    # Try complex data type
    complex = context.presentation.data_types.get(the_type) if context.presentation.data_types is not None else None
    if complex is not None:
        return complex 
    
    # Try primitive data type
    return get_primitive_data_type(the_type)

#
# Utils
#

PRIMITIVE_DATA_TYPES = {
    'string': str,
    'integer': int,
    'float': float,
    'boolean': bool}

def get_primitive_data_type(type_name):
    return PRIMITIVE_DATA_TYPES.get(type_name)

def get_data_type_name(the_type):
    """
    Returns the name of the type, whether it's a DataType, a primitive type, or another class.
    """
    
    if hasattr(the_type, '_name'):
        return the_type._name
    return '%s.%s' % (the_type.__module__, the_type.__name__) 

def coerce_value(context, presentation, the_type, value, aspect=None):
    """
    Returns the value after it's coerced to its type, reporting validation errors if it cannot be coerced.
    
    Supports both complex data types and primitives.
    
    Data types can use the :code:`coerce_value` extension to hook their own specialized function. If the extension
    is present, we will delegate to that hook.
    """

    is_function, fn = get_function(context, presentation, value)
    if is_function:
        return fn
    
    if the_type is None:
        return None

    # Delegate to 'coerce_value' extension
    if hasattr(the_type, '_get_extension'):
        coerce_value_fn_name = the_type._get_extension('coerce_value')
        if coerce_value_fn_name is not None:
            coerce_value_fn = import_fullname(coerce_value_fn_name)
            return coerce_value_fn(context, presentation, the_type, value, aspect)

    if hasattr(the_type, '_coerce_value'):
        # Delegate to _coerce_value (likely a DataType instance)
        return the_type._coerce_value(context, presentation, value, aspect)

    if the_type is not None:
        # Coerce to primitive type
        return coerce_to_primitive(context, presentation, the_type, value, aspect)
    
    return None

def coerce_to_primitive(context, presentation, primitive_type, value, aspect=None):
    """
    Returns the value after it's coerced to a primitive type, translating exceptions to validation errors if it cannot be coerced.
    """

    try:
        # Coerce
        value = primitive_type(value)
    except ValueError as e:
        report_issue_for_bad_format(context, presentation, primitive_type, value, aspect, e)
        value = None
    except TypeError as e:
        report_issue_for_bad_format(context, presentation, primitive_type, value, aspect, e)
        value = None
    
    return value

def report_issue_for_bad_format(context, presentation, the_type, value, aspect, e):
    aspect = None
    if aspect == 'default':
        aspect = '"default" value'
    elif aspect is not None:
        aspect = '"%s" constraint'  
    
    if aspect is not None:
        context.validation.report('%s for field "%s" is not a valid "%s": %s' % (aspect, presentation._name or presentation._container._name, get_data_type_name(the_type), repr(value)), locator=presentation._locator, level=Issue.BETWEEN_FIELDS, exception=e)
    else:
        context.validation.report('field "%s" is not a valid "%s": %s' % (presentation._name or presentation._container._name, get_data_type_name(the_type), repr(value)), locator=presentation._locator, level=Issue.BETWEEN_FIELDS, exception=e)

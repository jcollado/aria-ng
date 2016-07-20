
from aria import Issue, dsl_specification, import_fullname

PRIMITIVE_DATA_TYPES = {
    # YAML 1.2:
    'tag:yaml.org,2002:str': str,
    'tag:yaml.org,2002:integer': int,
    'tag:yaml.org,2002:float': float,
    'tag:yaml.org,2002:bool': bool,
    'tag:yaml.org,2002:null': None.__class__,
    # TODO timestamp

    # TOSCA aliases:
    'string': str,
    'integer': int,
    'float': float,
    'boolean': bool,
    'null': None.__class__
}

def get_data_type(context, presentation):
    the_type = presentation.type
    
    if the_type is None:
        # The default type is str
        return str
    
    # Try complex data type
    if the_type in context.presentation.data_types:
        return context.presentation.data_types[the_type]
    
    # Try primitive data type
    return PRIMITIVE_DATA_TYPES.get(the_type)

def validate_constraint(context, presentation):
    if len(presentation._raw) != 1:
        context.validation.report('constraint "%s" is not a dict with exactly one key %s' % (presentation._name, presentation._container._fullname), locator=presentation._locator, level=Issue.BETWEEN_FIELDS)
    
    # TODO values to match the type
    pass

def validate_entry_schema(context, presentation):
    the_type = presentation._container._get_type(context) if presentation._container is not None else None
    
    # Make sure the type supports entry_schema
    use_entry_schema = the_type._get_extension('use_entry_schema', False) if the_type is not None else False
    if not use_entry_schema:
        context.validation.report('data type "%s" does not support entry_schema for %s' % (the_type._name, presentation._container._fullname), locator=presentation._locator, level=Issue.BETWEEN_FIELDS)

@dsl_specification('3.2.1', 'tosca-simple-profile-1.0')
def coerce_value(context, presentation, the_type, entry_schema, constraints, value):
    """
    Many of the types we use in this profile are built-in types from the YAML 1.2 specification (i.e., those identified by the "tag:yaml.org,2002" version tag) [YAML-1.2].
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#_Toc373867862>`__
    """
        
    if the_type is None:
        return None

    if the_type == None.__class__:
        if value is not None:
            context.validation.report('field "%s" is of type "null" but has a non-null value: %s' % (presentation._name, repr(value)), locator=presentation._locator, level=Issue.BETWEEN_FIELDS)
            return None
    
    # Delegate to 'coerce_value' extension
    if hasattr(the_type, '_get_extension'):
        coerce_value_fn_name = the_type._get_extension('coerce_value')
        if coerce_value_fn_name is not None:
            coerce_value_fn = import_fullname(coerce_value_fn_name)
            return coerce_value_fn(context, presentation, the_type, entry_schema, constraints, value)
    
    if hasattr(the_type, '_coerce_value'):
        # Complex type
        value = the_type._coerce_value(constraints, value)
    else:
        # Primitive type
        try:
            value = the_type(value)
        except ValueError as e:
            report_issue_for_bad_format(context, presentation, the_type, value, e)
            value = None
    
    return value

def coerce_data_type_value(presentation, constraints, value):
    return value

def coerce_to_class(context, presentation, the_type, entry_schema, constraints, value):
    try:
        return the_type(entry_schema, constraints, value)
    except ValueError as e:
        report_issue_for_bad_format(context, presentation, the_type, value, e)
    return None

def report_issue_for_bad_format(context, presentation, the_type, value, e):
    context.validation.report('field "%s" is not a valid "%s.%s": %s' % (presentation._name, the_type.__module__, the_type.__name__, repr(value)), locator=presentation._locator, level=Issue.BETWEEN_FIELDS, exception=e)


from .data import PRIMITIVE_DATA_TYPES, get_data_type_name
from aria import Issue
from aria.presentation import report_issue_for_unknown_type, derived_from_validator

def node_type_or_template_validator(field, presentation, context):
    """
    Makes sure that the field refers to either a node template or a node type.
    
    Can be used with @field\_validator.
    """
    
    field._validate(presentation, context)
    
    value = getattr(presentation, field.name)
    if value is not None:
        node_templates = context.presentation.node_templates or {}
        node_types = context.presentation.node_types or {}
        if (value not in node_templates) and (value not in node_types):
            report_issue_for_unknown_type(context, presentation, 'node template or node type', field.name)

def relationship_type_or_template_validator(field, presentation, context):
    """
    Makes sure that the field refers to either a relationship template or a relationship type.
    
    Can be used with @field\_validator.
    """
    
    field._validate(presentation, context)
    
    value = getattr(presentation, field.name)
    if value is not None:
        relationship_templates = context.presentation.relationship_templates or {}
        relationship_types = context.presentation.relationship_types or {}
        if (value not in relationship_templates) and (value not in relationship_types):
            report_issue_for_unknown_type(context, presentation, 'relationship template or relationship type', field.name)

def list_node_type_or_group_type_validator(field, presentation, context):
    """
    Makes sure that the field's elements refer to either node types or a group types.

    Assumes that the field is a list.

    Can be used with @field\_validator.
    """
    
    field._validate(presentation, context)
    
    values = getattr(presentation, field.name)
    if values is not None:
        for value in values:
            node_types = context.presentation.node_types or {}
            group_types = context.presentation.group_types or {}
            if (value not in node_types) and (value not in group_types):
                report_issue_for_unknown_type(context, presentation, 'node type or group type', field.name)

def list_node_template_or_group_validator(field, presentation, context):
    """
    Makes sure that the field's elements refer to either node templates or groups.

    Assumes that the field is a list.

    Can be used with @field\_validator.
    """
    
    field._validate(presentation, context)
    
    values = getattr(presentation, field.name)
    if values is not None:
        for value in values:
            node_templates = context.presentation.node_templates or {}
            groups = context.presentation.groups or {}
            if (value not in node_templates) and (value not in groups):
                report_issue_for_unknown_type(context, presentation, 'node template or group', field.name)

def data_type_validator(type_name='data type'):
    """
    Makes sure that the field refers to a valid data type, whether primitive or complex. 
    
    Can be used with @field\_validator.
    
    Returns true if is a complex data type.
    """

    def validator(field, presentation, context):
        field._validate(presentation, context)
    
        value = getattr(presentation, field.name)
        if value is not None:
            # Can be a complex data type
            if value in context.presentation.data_types:
                return True
            # Can be a primitive data type
            if value not in PRIMITIVE_DATA_TYPES:
                report_issue_for_unknown_type(context, presentation, type_name, field.name)
    
        return False

    return validator

_data_type_derived_from_validator = derived_from_validator('data_types')

def data_type_derived_from_validator(field, presentation, context):
    """
    Makes sure that the field ("derived\_from" in DataType) refers to a valid parent type (primitive or complex).
    
    Can be used with @field\_validator.
    """
    
    if data_type_validator()(field, presentation, context):
        # Validate derivation only if a complex data type (primitive types have no derivation hierarchy)
        _data_type_derived_from_validator(field, presentation, context)

def entry_schema_validator(field, presentation, context):
    """
    According to whether the data type supports entry_schema (e.g., it is or inherits from list or map),
    make sure that we either have or don't have a valid data type value.
    
    Can be used with @field\_validator.
    """

    field._validate(presentation, context)

    def type_uses_entry_schema(the_type):
        use_entry_schema = the_type._get_extension('use_entry_schema', False) if hasattr(the_type, '_get_extension') else False
        if use_entry_schema:
            return True
        parent = the_type._get_parent(context) if hasattr(the_type, '_get_parent') else None
        if parent is None:
            return False
        return type_uses_entry_schema(parent)

    value = getattr(presentation, field.name)
    the_type = presentation._get_type(context)
    if the_type is None:
        return
    use_entry_schema = type_uses_entry_schema(the_type)
    
    if use_entry_schema:
        if value is None:
            context.validation.report('"entry_schema" does not have a value as required by data type "%s" for %s' % (get_data_type_name(the_type), presentation._container._fullname), locator=presentation._locator, level=Issue.BETWEEN_TYPES)
    else:
        if value is not None:
            context.validation.report('"entry_schema" has a value but it is not used by data type "%s" for %s' % (get_data_type_name(the_type), presentation._container._fullname), locator=presentation._locator, level=Issue.BETWEEN_TYPES)

def data_value_validator(field, presentation, context):
    """
    Makes sure that the field contains a valid value according to data type and constraints.
    
    Can be used with @field\_validator.
    """

    field._validate(presentation, context)

    # TODO

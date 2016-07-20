
from .data import PRIMITIVE_DATA_TYPES
from aria.presentation import report_issue_for_unknown_type, derived_from_validator

def data_type_validator(type_name='data type'):
    """
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

def data_value_validator(field, presentation, context):
    """
    Can be used with @field\_validator.
    """

    field._validate(presentation, context)

    # TODO

_data_type_derived_from_validator = derived_from_validator('data_types')

def data_type_derived_from_validator(field, presentation, context):
    """
    Can be used with @field\_validator.
    """
    
    if data_type_validator()(field, presentation, context):
        # Validate derivation only if a complex data type (primitive types have no derivation hierarchy)
        _data_type_derived_from_validator(field, presentation, context)

def node_type_or_template_validator(field, presentation, context):
    """
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

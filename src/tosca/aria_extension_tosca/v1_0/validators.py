
def node_type_or_template_validator(field, presentation, consumption_context):
    field._validate(presentation, consumption_context)
    
    value = getattr(presentation, field.name)
    if value is not None:
        if (value not in consumption_context.presentation.node_templates) and (value not in consumption_context.presentation.node_types):
            presentation._append_value_error_for_unknown_type(consumption_context, 'node template or node type', field.name)

def relationship_type_or_template_validator(field, presentation, consumption_context):
    field._validate(presentation, consumption_context)
    
    value = getattr(presentation, field.name)
    if value is not None:
        if (value not in consumption_context.presentation.relationship_templates) and (value not in consumption_context.presentation.relationship_types):
            presentation._append_value_error_for_unknown_type(consumption_context, 'relationship template or relationship type', field.name)

def list_node_type_or_group_type_validator(field, presentation, consumption_context):
    field._validate(presentation, consumption_context)
    
    values = getattr(presentation, field.name)
    if values is not None:
        for value in values:
            if (value not in consumption_context.presentation.node_types) and (value not in consumption_context.presentation.group_types):
                presentation._append_value_error_for_unknown_type(consumption_context, 'node type or group type', field.name)

def list_node_template_or_group_validator(field, presentation, consumption_context):
    field._validate(presentation, consumption_context)
    
    values = getattr(presentation, field.name)
    if values is not None:
        for value in values:
            if (value not in consumption_context.presentation.node_templates) and (value not in consumption_context.presentation.groups):
                presentation._append_value_error_for_unknown_type(consumption_context, 'node template or group', field.name)

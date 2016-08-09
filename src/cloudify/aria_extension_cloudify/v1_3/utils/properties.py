
from .data_types import coerce_value
from aria import Issue
from aria.utils import merge
from collections import OrderedDict

#
# NodeType, RelationshipType, PolicyType, DataType
#

def get_inherited_property_definitions(context, presentation, field_name, for_presentation=None): # works on properties, parameters, inputs, and attributes
    """
    Returns our property definitions added on top of those of our parent, if we have one (recursively).
    
    Allows overriding all aspects of parent properties except data type.  
    """
    
    # Get definitions from parent
    parent = presentation._get_parent(context)
    definitions = get_inherited_property_definitions(context, parent, field_name, for_presentation=presentation) if parent is not None else OrderedDict()
    
    # Add/merge our definitions
    our_definitions = getattr(presentation, field_name)
    if our_definitions is not None:
        our_definitions_clone = OrderedDict()
        for name, our_definition in our_definitions.iteritems():
            our_definitions_clone[name] = our_definition._clone(for_presentation)
        our_definitions = our_definitions_clone
        merge_property_definitions(context, presentation, definitions, our_definitions, field_name, for_presentation)
        
    return definitions

#
# NodeTemplate, RelationshipTemplate
#

def get_assigned_and_defined_property_values(context, presentation):
    """
    Returns the assigned property values while making sure they are defined in our type.
    
    The property definition's default value, if available, will be used if we did not assign it.
    
    Makes sure that required properties indeed end up with a value.
    """

    values = OrderedDict()
    
    the_type = presentation._get_type(context)
    assignments = presentation.properties
    definitions = the_type._get_properties(context) if the_type is not None else None

    # Fill in our assignments, but make sure they are defined
    if assignments is not None:
        for name, value in assignments.iteritems():
            if (definitions is not None) and (name in definitions):
                definition = definitions[name]
                if value.value is not None:
                    values[name] = coerce_property_value(context, value, definition, value.value)
            else:
                context.validation.report('assignment to undefined property "%s" in "%s"' % (name, presentation._fullname), locator=value._locator, level=Issue.BETWEEN_TYPES)
    
    # Fill in defaults from the definitions
    if definitions is not None:
        for name, definition in definitions.iteritems():
            if (values.get(name) is None) and hasattr(definition, 'default') and (definition.default is not None):
                values[name] = coerce_property_value(context, presentation, definition, definition.default) 

    validate_required_values(context, presentation, values, definitions)
    
    return values

#
# TopologyTemplate
#

def get_input_values(context, presentation):
    values = OrderedDict()
    
    inputs = presentation.inputs

    # Fill in defaults and values
    for name, definition in inputs.iteritems():
        if (values.get(name) is None):
            if hasattr(definition, 'default') and (definition.default is not None):
                values[name] = coerce_property_value(context, presentation, definition, definition.default)
    
    return values

#
# Utils
#

def validate_required_values(context, presentation, values, definitions):
    """
    Check if required properties have not been assigned.
    """
    
    if definitions is None:
        return
    for name, definition in definitions.iteritems():
        if getattr(definition, 'required', False) and ((values is None) or (values.get(name) is None)):
            context.validation.report('required property "%s" is not assigned a value in "%s"' % (name, presentation._fullname), locator=presentation._get_child_locator('properties'), level=Issue.BETWEEN_TYPES)

def merge_raw_property_definition(context, presentation, raw_property_definition, our_property_definition, field_name, property_name):
    # Check if we changed the type
    # TODO: allow a sub-type?
    type1 = raw_property_definition.get('type')
    type2 = our_property_definition.type
    if type1 != type2:
        context.validation.report('override changes type from "%s" to "%s" for property "%s" in "%s"' % (type1, type2, property_name, presentation._fullname), locator=presentation._get_grandchild_locator(field_name, property_name), level=Issue.BETWEEN_TYPES)

    merge(raw_property_definition, our_property_definition._raw)

def merge_property_definitions(context, presentation, property_definitions, our_property_definitions, field_name, for_presentation):
    if our_property_definitions is None:
        return
    for property_name, our_property_definition in our_property_definitions.iteritems():
        if property_name in property_definitions:
            property_definition = property_definitions[property_name]
            merge_raw_property_definition(context, presentation, property_definition._raw, our_property_definition, field_name, property_name)
        else:
            property_definitions[property_name] = our_property_definition._clone()

def coerce_property_value(context, presentation, definition, value): # works on properties, inputs, and parameters
    the_type = definition._get_type(context) if definition is not None else None
    return coerce_value(context, presentation, the_type, value)

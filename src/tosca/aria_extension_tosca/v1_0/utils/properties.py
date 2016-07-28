
from .data import coerce_value
from aria import Issue, merge, deepclone
from collections import OrderedDict

#
# ArtifactType, DataType, CapabilityType, RelationshipType, NodeType, GroupType, PolicyType, CapabilityDefinition
#

def get_inherited_property_definitions(context, presentation, field_name, for_presentation=None): # works on properties, parameters, inputs, and attributes
    """
    Returns our property definitions added on top of those of our parent, if we have one (recursively).
    
    Allows overriding all aspects of parent properties except data type.  
    """
    
    # Get definitions from parent
    parent = presentation._get_parent(context) if hasattr(presentation, '_get_parent') else None # if we inherit from a primitive, it does not have a parent
    definitions = get_inherited_property_definitions(context, parent, field_name, for_presentation=presentation) if parent is not None else OrderedDict()
    
    # Add/merge our definitions
    our_definitions = getattr(presentation, field_name, None) # if we inherit from a primitive, it does not have our field
    if our_definitions is not None:
        for name, our_definition in our_definitions.iteritems():
            if name in definitions:
                definition = definitions[name]
                
                # Check if we changed the type
                type1 = getattr(definition, 'type', None)
                type2 = getattr(our_definition, 'type', None)
                if type1 != type2:
                    context.validation.report('override changes type from "%s" to "%s" for property "%s" for "%s"' % (type1, type2, name, presentation._fullname), locator=presentation._get_grandchild_locator(field_name, name), level=Issue.BETWEEN_TYPES)
                
                merge(definition._raw, deepclone(our_definition._raw))
            else:
                if for_presentation is not None:
                    definitions[name] = our_definition._clone(for_presentation)
                else:
                    definitions[name] = our_definition
        
    return definitions

#
# NodeTemplate, RelationshipTemplate, GroupDefinition, PolicyDefinition
#

def get_assigned_and_defined_property_values(context, presentation, original_presentation=None):
    """
    Returns the assigned property values while making sure they are defined in our type.
    
    The property definition's default value, if available, will be used if we did not assign it.
    
    Makes sure that required properties indeed end up with a value.
    """

    values = OrderedDict()
    
    the_type = presentation._get_type(context)
    
    if isinstance(the_type, tuple):
        # In RequirementAssignmentRelationship
        the_type = the_type[0] # This could be a RelationshipTemplate
    
    assignments = presentation.properties
    definitions = the_type._get_properties(context) if the_type is not None else None

    # Fill in our assignments, but make sure they are defined
    if assignments is not None:
        for name, value in assignments.iteritems():
            if (definitions is not None) and (name in definitions):
                definition = definitions[name]
                if value.value is not None:
                    values[name] = coerce_property_value(context, value, definition)
            else:
                context.validation.report('assignment to undefined property "%s" for "%s"' % (name, presentation._fullname), locator=value._locator, level=Issue.BETWEEN_TYPES)
    
    # Fill in defaults from the definitions, and check if required properties have not been assigned
    if definitions is not None:
        for name, definition in definitions.iteritems():
            if (values.get(name) is None) and hasattr(definition, 'default') and (definition.default is not None):
                values[name] = coerce_default_property_value(context, presentation, definition) 

            if getattr(definition, 'required', False) and (values.get(name) is None):
                if original_presentation is None:
                    original_presentation = presentation 
                context.validation.report('required property "%s" is not assigned a value for "%s"' % (name, original_presentation._fullname), locator=original_presentation._get_child_locator('properties'), level=Issue.BETWEEN_TYPES)
    
    return values

#
# Utils
#

def coerce_property_value(context, value, definition): # works on both properties and inputs
    the_type = definition._get_type(context) if definition is not None else None
    entry_schema = definition.entry_schema if definition is not None else None
    constraints = definition._get_constraints(context) if definition is not None else None
    return coerce_value(context, value, the_type, entry_schema, constraints, value.value)

def coerce_default_property_value(context, presentation, definition): # works on both properties and inputs
    the_type = definition._get_type(context) if definition is not None else None
    entry_schema = definition.entry_schema if definition is not None else None
    constraints = definition._get_constraints(context) if definition is not None else None
    return coerce_value(context, presentation, the_type, entry_schema, constraints, definition.default)

def convert_property_definitions_to_values(definitions):
    values = OrderedDict()
    for name, definition in definitions.iteritems():
        default = definition.default
        if default is not None:
            values[name] = default
    return values

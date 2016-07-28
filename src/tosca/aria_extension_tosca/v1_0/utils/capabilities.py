
from .properties import convert_property_definitions_to_values
from aria import Issue, merge, deepclone
from collections import OrderedDict

#
# NodeType
#

def get_inherited_capability_definitions(context, presentation, for_presentation=None):
    """
    Returns our capability capability_definitions added on top of those of our parent, if we have one (recursively).
    
    Allows overriding all aspects of parent capability properties except data type.  
    """

    # Get capability_definitions from parent
    parent = presentation._get_parent(context)
    capability_definitions = get_inherited_capability_definitions(context, parent, for_presentation=presentation) if parent is not None else OrderedDict()
    
    # Add/merge our capability_definitions
    our_capability_definitions = presentation.capabilities
    if our_capability_definitions is not None:
        for name, our_capability_definition in our_capability_definitions.iteritems():
            if name in capability_definitions:
                capability_definition = capability_definitions[name]
                
                # Check if we changed the type
                #type1 = getattr(capability_definition, 'type', None)
                #type2 = getattr(our_capability_definition, 'type', None)
                #if type1 != type2:
                #    context.validation.report('override changes type from "%s" to "%s" for property "%s" for "%s"' % (type1, type2, name, presentation._fullname), locator=presentation._get_grandchild_locator(field_name, name), level=Issue.BETWEEN_TYPES)
                
                merge(capability_definition._raw, deepclone(our_capability_definition._raw))
            else:
                if for_presentation is not None:
                    capability_definitions[name] = our_capability_definition._clone(for_presentation)
                else:
                    capability_definitions[name] = our_capability_definition
        
    return capability_definitions

#
# NodeTemplate
#

def get_template_capabilities(context, presentation):
    """
    Returns the node type's capabilities with our assignments to properties and attributes merged in. 
    
    Capability properties' default values, if available, will be used if we did not assign them.
    
    Makes sure that required properties indeed end up with a value.
    """

    capability_assignments = OrderedDict()
    
    the_type = presentation._get_type(context) # NodeType
    capability_definitions = the_type._get_capabilities(context) if the_type is not None else None

    # Copy over capability definitions from the type (will initialize properties with default values)
    if capability_definitions is not None:
        for capability_name, capability in capability_definitions.iteritems():
            capability_assignments[capability_name] = convert_capability_from_definition_to_assignment(context, capability, presentation)

    # Fill in our capability assignments
    our_capability_assignments = presentation.capabilities
    if our_capability_assignments is not None:
        for capability_name, our_capability_assignment in our_capability_assignments.iteritems():
            if capability_name in capability_assignments:
                # TODO
                assign_raw_properties(context)
            else:
                context.validation.report('capability "%s" not declared in node type "%s" for "%s"' % (capability_name, presentation.type, presentation._fullname), locator=our_capability_assignment._locator, level=Issue.BETWEEN_TYPES)

    return capability_assignments

#
# Utils
#

def convert_capability_from_definition_to_assignment(context, presentation, container):
    from ..assignments import CapabilityAssignment
    
    raw = OrderedDict()
    
    properties = presentation._get_properties(context)
    if properties is not None:
        raw['properties'] = convert_property_definitions_to_values(properties)

    # TODO attributes

    return CapabilityAssignment(name=presentation._name, raw=raw, container=container)

def assign_raw_properties(context):
    pass

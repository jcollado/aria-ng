
from .properties import coerce_property_value, convert_property_definitions_to_values
from aria import Issue, merge
from collections import OrderedDict
from copy import deepcopy

#
# NodeType
#

def get_inherited_requirements(context, presentation):
    """
    Returns our requirement definitions added to those of our parent, if we have one (recursively).
    
    Requirements with the same name will not be accumulated.
    """
    
    def has_requirement(requirements, name):
        for n, _ in requirements:
            if n == name:
                return True
        return False
    
    parent = presentation._get_parent(context)
    requirements = get_inherited_requirements(context, parent) if parent is not None else []
    
    our_requirements = presentation.requirements
    if our_requirements is not None:
        for requirement_name, our_requirement in our_requirements:
            if not has_requirement(requirements, requirement_name):
                requirements.append((requirement_name, our_requirement))

    return requirements

def get_inherited_capabilities(context, presentation, for_presentation=None):
    """
    Returns our capability capabilities added on top of those of our parent, if we have one (recursively).
    
    Allows overriding all aspects of parent capability properties except data type.  
    """

    # Get capabilities from parent
    parent = presentation._get_parent(context)
    capabilities = get_inherited_capabilities(context, parent, for_presentation=presentation) if parent is not None else OrderedDict()
    
    # Add/merge our capabilities
    our_capabilities = presentation.capabilities
    if our_capabilities is not None:
        for name, our_capability in our_capabilities.iteritems():
            if name in capabilities:
                definition = capabilities[name]
                
                # Check if we changed the type
                #type1 = getattr(definition, 'type', None)
                #type2 = getattr(our_capability, 'type', None)
                #if type1 != type2:
                #    context.validation.report('override changes type from "%s" to "%s" for property "%s" for "%s"' % (type1, type2, name, presentation._fullname), locator=presentation._get_grandchild_locator(field_name, name), level=Issue.BETWEEN_TYPES)
                
                merge(definition._raw, deepcopy(our_capability._raw))
            else:
                if for_presentation is not None:
                    capabilities[name] = our_capability._clone(for_presentation)
                else:
                    capabilities[name] = our_capability
        
    return capabilities

#
# NodeTemplate
#

def get_template_requirements(context, presentation):
    """
    Returns our requirements added on top of those of the node type.
    
    If the requirement has a relationship, the relationship properties and interfaces are assigned.
    
    Returns the assigned property values while making sure they are defined in our type.
    
    The property definition's default value, if available, will be used if we did not assign it.
    
    Makes sure that required properties indeed end up with a value.
    """
    
    requirement_assignments = []

    the_type = presentation._get_type(context) # NodeType
    requirement_definitions = the_type._get_requirements(context) if the_type is not None else None

    # Copy over requirement definitions from the type (will initialize properties with default values)
    if requirement_definitions is not None:
        for requirement_name, requirement_definition in requirement_definitions:
            requirement_assignment = convert_requirement_from_definition_to_assignment(context, requirement_definition, presentation)
            requirement_assignments.append((requirement_name, requirement_assignment))

    # Add in our requirement assignments
    our_requirement_assignments = presentation.requirements
    if our_requirement_assignments is not None:
        for requirement_name, our_requirement_assignment in our_requirement_assignments:
            requirement_assignment = our_requirement_assignment._clone(presentation)
            requirement_assignments.append((requirement_name, requirement_assignment))

    return requirement_assignments

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

def convert_requirement_from_definition_to_assignment(context, presentation, container):
    from ..assignments import RequirementAssignment
    
    raw = OrderedDict()
    
    raw['capability'] = presentation.capability # capability type name
    
    node_type = presentation._get_node_type(context)
    if node_type is not None:
        raw['node'] = node_type._name
        
    relationship = presentation.relationship # RequirementDefinitionRelationship
    if relationship is not None:
        raw['relationship'] = OrderedDict()
        relationship_type = relationship._get_type(context)
        if relationship_type is not None:
            raw['relationship']['type'] = relationship_type._name
            
            # Properties and interfaces will be pulled from this type

    return RequirementAssignment(name=presentation._name, raw=raw, container=container)

def convert_capability_from_definition_to_assignment(context, presentation, container):
    from ..assignments import CapabilityAssignment
    
    raw = OrderedDict()
    
    properties = presentation._get_properties(context)
    if properties is not None:
        raw['properties'] = OrderedDict()
        convert_property_definitions_to_values(raw['properties'], properties)

    # TODO attributes

    return CapabilityAssignment(name=presentation._name, raw=raw, container=container)

def assign_raw_properties(context):

    pass

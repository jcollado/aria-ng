
from .properties import convert_property_definitions_to_values, get_assigned_and_defined_property_values
from .interfaces import convert_interface_definition_from_type_to_raw_template, get_template_interfaces
from aria.utils import merge, deepclone
from collections import OrderedDict

#
# NodeType
#

def get_inherited_requirement_definitions(context, presentation):
    """
    Returns our requirement definitions added on top of those of our parent, if we have one (recursively).
    
    Allows overriding requirement definitions if they have the same name.  
    """
    
    def get_requirement(requirement_definitions, name):
        for n, requirement in requirement_definitions:
            if n == name:
                return requirement
        return None
    
    parent = presentation._get_parent(context)
    requirement_definitions = get_inherited_requirement_definitions(context, parent) if parent is not None else []
    
    our_requirement_definitions = presentation.requirements
    if our_requirement_definitions is not None:
        for requirement_name, our_requirement_definition in our_requirement_definitions:
            # Remove existing requirement definitions of this name if they exist
            for n, r in requirement_definitions:
                if n == requirement_name:
                    requirement_definitions.remove((n, r))

            requirement_definitions.append((requirement_name, our_requirement_definition))

    return requirement_definitions

#
# NodeTemplate
#

def get_template_requirements(context, presentation):
    """
    Returns our requirements added on top of those of the node type.
    
    If the requirement has a relationship, the relationship properties and interfaces are assigned.
    
    Returns the assigned property, interface input, and interface operation input values while making
    sure they are defined in our type. Default values, if available, will be used if we did not assign
    them. Also makes sure that required properties and inputs indeed end up with a value.
    """
    
    def get_requirement(requirements, name):
        for n, requirement in requirements:
            if n == name:
                return requirement
        return None

    requirement_assignments = []

    the_type = presentation._get_type(context) # NodeType
    requirement_definitions = the_type._get_requirements(context) if the_type is not None else None

    # Copy over requirement definitions from the type (will initialize properties with default values)
    if requirement_definitions is not None:
        for requirement_name, requirement_definition in requirement_definitions:
            requirement_assignment = convert_requirement_from_definition_to_assignment(context, requirement_definition, presentation)
            requirement_assignments.append((requirement_name, requirement_assignment))

    # Add/merge our requirement assignments
    our_requirement_assignments = presentation.requirements
    if our_requirement_assignments is not None:
        for requirement_name, our_requirement_assignment in our_requirement_assignments:
            our_requirement_assignment = our_requirement_assignment._clone()
            fill_in_requirement_assignment(context, our_requirement_assignment)
            requirement_assignment = get_requirement(requirement_assignments, requirement_name)
            if requirement_assignment is not None:
                merge_raw_requirement_assignment(context, requirement_assignment._raw, our_requirement_assignment)
            else:
                requirement_assignments.append((requirement_name, our_requirement_assignment))

    return requirement_assignments

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
            
            # Convert property definitions to values
            the_type = relationship._get_type(context) # RelationshipType
            if the_type is not None:
                property_definitions = the_type._get_properties(context)
                if len(property_definitions):
                    raw['properties'] = convert_property_definitions_to_values(property_definitions)
            
            # Convert interface definitions to templates
            interface_definitions = relationship_type._get_interfaces(context) # InterfaceDefinitionForType
            if len(interface_definitions):
                raw['interfaces'] = convert_interface_definition_from_type_to_raw_template(context, interface_definitions)

    return RequirementAssignment(name=presentation._name, raw=raw, container=container)

def fill_in_requirement_assignment(context, requirement):
    relationship = requirement.relationship
    if relationship is None:
        return
    
    relationship_type, relationship_type_variant = relationship._get_type(context)
    if relationship_type is None:
        return

    if relationship_type_variant == 'relationship_type':
        property_values = get_assigned_and_defined_property_values(context, relationship)
    else:
        property_values = relationship_type._get_property_values(context)
    
    interfaces = get_template_interfaces(context, relationship, 'relationship definition')
        
    if len(property_values):
        relationship._raw['properties'] = property_values
        
    if len(interfaces):
        relationship._raw['interfaces'] = OrderedDict()
        for interface_name, interface in interfaces.iteritems():
            relationship._raw['interfaces'][interface_name] = interface._raw

def merge_raw_requirement_assignment(context, raw_requirement, our_requirement):
    capability = our_requirement.capability
    if capability is not None:
        raw_requirement['capability'] = capability
        
    node = our_requirement.node
    if node is not None:
        raw_requirement['node'] = node
        
    relationship = our_requirement.relationship # RequirementAssignmentRelationship
    if relationship is not None:
        # Make sure we have a dict
        if 'relationship' not in raw_requirement:
            raw_requirement['relationship'] = OrderedDict()
        elif not isinstance(raw_requirement['relationship'], dict):
            # Convert from short form to long form
            the_type = raw_requirement['relationship']
            raw_requirement['relationship'] = OrderedDict()
            raw_requirement['relationship']['type'] = the_type

        the_type = relationship.type
        if the_type is not None:
            raw_requirement['relationship']['type'] = the_type

        properties = relationship.properties # PropertyAssignment
        if properties is not None:
            # Make sure we have a dict
            if 'properties' not in raw_requirement:
                raw_requirement['properties'] = OrderedDict()
            
            merge(raw_requirement['properties'], deepclone(properties._raw))

        interfaces = relationship.interfaces # InterfaceDefinitionForTemplate
        if interfaces is not None:
            # Make sure we have a dict
            if 'interfaces' not in raw_requirement:
                raw_requirement['interfaces'] = OrderedDict()
            
            merge(raw_requirement['interfaces'], deepclone(interfaces._raw))

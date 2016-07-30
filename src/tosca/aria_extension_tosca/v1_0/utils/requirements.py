
from .properties import convert_property_definitions_to_values, get_assigned_and_defined_property_values
from .interfaces import convert_interface_definition_from_type_to_raw_template
from aria import Issue
from aria.utils import deepclone
from collections import OrderedDict

#
# NodeType
#

def get_inherited_requirement_definitions(context, presentation):
    """
    Returns our requirement definitions added on top of those of our parent, if we have one (recursively).
    
    Allows overriding requirement definitions if they have the same name.  
    """
    
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
    Returns our requirements added on top of those of the node type if they exist there.
    
    If the requirement has a relationship, the relationship properties and interfaces are assigned.
    
    Returns the assigned property, interface input, and interface operation input values while making
    sure they are defined in our type. Default values, if available, will be used if we did not assign
    them. Also makes sure that required properties and inputs indeed end up with a value.
    """

    requirement_assignments = []

    the_type = presentation._get_type(context) # NodeType
    requirement_definitions = the_type._get_requirements(context) if the_type is not None else None
    
    # Add our requirement assignments
    our_requirement_assignments = presentation.requirements
    if our_requirement_assignments is not None:
        for requirement_name, our_requirement_assignment in our_requirement_assignments:
            requirement_definition = get_requirement(requirement_definitions, requirement_name)
            if requirement_definition is not None:
                requirement_assignment = convert_requirement_from_definition_to_assignment(context, requirement_definition, presentation)
                merge_requirement_assignment(context, requirement_assignment, our_requirement_assignment)
                requirement_assignments.append((requirement_name, requirement_assignment))
            else:
                context.validation.report('requirement "%s" not declared at node type "%s" in "%s"' % (requirement_name, presentation.type, presentation._fullname), locator=our_requirement_assignment._locator, level=Issue.BETWEEN_TYPES)

    # Validate occurrences
    if requirement_definitions is not None:
        for requirement_name, requirement_definition in requirement_definitions:
            # Allowed occurrences
            allowed_occurrences = requirement_definition.occurrences
            allowed_occurrences = allowed_occurrences if allowed_occurrences is not None else None
            
            # Count actual occurrences
            actual_occurrences = 0
            for n, _ in requirement_assignments:
                if n == requirement_name:
                    actual_occurrences += 1
            
            if allowed_occurrences is None:
                # If not specified, we interpret this to mean that exactly 1 occurrence is required
                if actual_occurrences == 0:
                    # If it's not there, We will automatically add it
                    requirement_assignment = convert_requirement_from_definition_to_assignment(context, requirement_definition, presentation)
                    requirement_assignments.append((requirement_name, requirement_assignment))
                elif actual_occurrences > 1:
                    context.validation.report('requirement "%s" is allowed only one occurrence in "%s": %d' % (requirement_name, presentation._fullname, actual_occurrences), locator=presentation._locator, level=Issue.BETWEEN_TYPES)
            else:
                if not allowed_occurrences.is_in(actual_occurrences):
                    if allowed_occurrences.value[1] == 'UNBOUNDED':
                        context.validation.report('requirement "%s" does not have at least %d occurrences in "%s": has %d' % (requirement_name, allowed_occurrences.value[0], presentation._fullname, actual_occurrences), locator=presentation._locator, level=Issue.BETWEEN_TYPES)
                    else:
                        context.validation.report('requirement "%s" is allowed between %d and %d occurrences in "%s": has %d' % (requirement_name, allowed_occurrences.value[0], allowed_occurrences.value[1], presentation._fullname, actual_occurrences), locator=presentation._locator, level=Issue.BETWEEN_TYPES)

    return requirement_assignments

#
# Utils
#

def convert_requirement_from_definition_to_assignment(context, presentation, container):
    from ..assignments import RequirementAssignment
    
    raw = OrderedDict()
    
    raw['capability'] = deepclone(presentation.capability) # capability type name
    
    node_type = presentation._get_node_type(context)
    if node_type is not None:
        raw['node'] = deepclone(node_type._name)
        
    relationship = presentation.relationship # RequirementDefinitionRelationship
    if relationship is not None:
        raw['relationship'] = OrderedDict()
        relationship_type = relationship._get_type(context)
        if relationship_type is not None:
            raw['relationship']['type'] = deepclone(relationship_type._name)
            
            # Convert property definitions to values
            property_definitions = relationship_type._get_properties(context)
            if property_definitions:
                raw['properties'] = convert_property_definitions_to_values(property_definitions)
            
            # Convert interface definitions to templates
            interface_definitions = relationship_type._get_interfaces(context) # InterfaceDefinitionForType
            if interface_definitions:
                raw['interfaces'] = convert_interface_definition_from_type_to_raw_template(context, interface_definitions)

    return RequirementAssignment(name=presentation._name, raw=raw, container=container)

def merge_requirement_assignment(context, requirement, our_requirement):
    our_capability = our_requirement.capability
    if our_capability is not None:
        requirement._raw['capability'] = deepclone(our_capability)
        
    our_node = our_requirement.node
    if our_node is not None:
        requirement._raw['node'] = deepclone(our_node)
        
    our_relationship = our_requirement.relationship # RequirementAssignmentRelationship
    if our_relationship is not None:
        # Make sure we have a dict
        if 'relationship' not in requirement._raw:
            requirement._raw['relationship'] = OrderedDict()
        elif not isinstance(requirement._raw['relationship'], dict):
            # Convert from short form to long form
            the_type = requirement._raw['relationship']
            requirement._raw['relationship'] = OrderedDict()
            requirement._raw['relationship']['type'] = deepclone(the_type)

        the_type = our_relationship.type
        if the_type is not None:
            requirement._raw['relationship']['type'] = deepclone(the_type)
            
        our_relationship_properties = our_relationship.properties # PropertyAssignment
        if our_relationship_properties:
            # Make sure we have a dict
            if 'properties' not in requirement._raw['relationship']:
                requirement._raw['relationship']['properties'] = OrderedDict()
                
            # Merge our relationship property assignments
            for property_name, our_relationship_property in our_relationship_properties.iteritems():
                requirement._raw['relationship']['properties'][property_name] = deepclone(our_relationship_property.value)

        # Reinitialize relationship properties (will trigger validation)
        values = get_assigned_and_defined_property_values(context, requirement.relationship, our_relationship)
        if values:
            requirement._raw['relationship']['properties'] = values

        our_relationship_interfaces = our_relationship.interfaces # InterfaceDefinitionForTemplate
        if our_relationship_interfaces is not None:
            # Make sure we have a dict
            if 'interfaces' not in requirement._raw['relationship']:
                requirement._raw['relationship']['interfaces'] = OrderedDict()
            
            for interface_name, our_relationship_interface in our_relationship_interfaces.iteritems():
                requirement._raw['relationship']['interfaces'][interface_name] = our_relationship_interface._clone(requirement)

def get_requirement(requirement_definitions, name):
    if requirement_definitions is not None:
        for n, requirement in requirement_definitions:
            if n == name:
                return requirement
    return None

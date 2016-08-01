
from aria.deployment import Topology, Type, NodeTemplate, Interface, Operation, Requirement, Relationship, Capability
from .data import coerce_value
import re

def normalize_topology(context, presenter):
    topology = Topology()

    normalize_types(context, topology.node_types, presenter.node_types)
    normalize_types(context, topology.capability_types, presenter.capability_types)
    
    topology_template = presenter.service_template.topology_template
    if topology_template is not None:
        if topology_template.node_templates:
            for node_template_name, node_template in topology_template.node_templates.iteritems():
                topology.node_templates[node_template_name] = normalize_node_template(context, node_template)

    return topology

def normalize_types(context, root, types):
    if types is None:
        return
    
    def added_all():
        for name in types:
            if root.get_descendant(name) is None:
                return False
        return True

    while not added_all():    
        for name, the_type in types.iteritems():
            if root.get_descendant(name) is None:
                parent_type = the_type._get_parent(context)
                if parent_type is None:
                    root.children.append(Type(the_type._name))
                else:
                    container = root.get_descendant(parent_type._name)
                    if container is not None:
                        container.children.append(Type(the_type._name))

def normalize_node_template(context, node_template):
    the_type = node_template._get_type(context)
    r = NodeTemplate(name=node_template._name, type_name=the_type._name)

    properties = node_template._get_property_values(context)
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop

    interfaces = node_template._get_interfaces(context)
    if interfaces:
        for interface_name, interface in interfaces.iteritems():
            interface = normalize_interface(context, interface)
            if interface is not None:
                r.interfaces[interface_name] = interface

    requirements = node_template._get_requirements(context)
    if requirements:
        for _, requirement in requirements:
            r.requirements.append(normalize_requirement(context, requirement))

    capabilities = node_template._get_capabilities(context)
    if capabilities:
        for capability_name, capability in capabilities.iteritems():
            r.capabilities[capability_name] = normalize_capability(context, capability)

    normalize_node_filter(context, node_template.node_filter, r.target_node_type_constraints)
    
    return r

def normalize_interface(context, interface):
    r = Interface(name=interface._name)

    inputs = interface.inputs
    if inputs:
        for input_name, the_input in inputs.iteritems():
            r.inputs[input_name] = the_input.value

    operations = interface.operations
    if operations:
        for operation_name, operation in operations.iteritems():
            #if operation.implementation is not None:
            r.operations[operation_name] = normalize_operation(context, operation)
    
    return r #if r.operations else None

def normalize_operation(context, operation):
    r = Operation(name=operation._name)

    implementation = operation.implementation
    if implementation is not None:
        r.implementation = implementation.primary
        dependencies = implementation.dependencies
        if dependencies is not None:
            r.dependencies = dependencies

    inputs = operation.inputs
    if inputs:
        for input_name, the_input in inputs.iteritems():
            r.inputs[input_name] = the_input.value
    
    return r

def normalize_requirement(context, requirement):
    r = {'name': requirement._name}

    node, node_variant = requirement._get_node(context)
    if node is not None:
        if node_variant == 'node_type':
            r['node_type_name'] = node._name
        else:
            r['node_template_name'] = node._name

    capability, capability_variant = requirement._get_capability(context)
    if capability is not None:
        if capability_variant == 'capability_type':
            r['capability_type_name'] = capability._name
        else:
            r['capability_name'] = capability._name

    r = Requirement(**r)

    normalize_node_filter(context, requirement.node_filter, r.node_type_constraints)

    relationship = requirement.relationship
    if relationship is not None:
        r.relationship = normalize_relationship(context, relationship)
        
    return r

def normalize_relationship(context, relationship):
    relationship_type, relationship_type_variant = relationship._get_type(context)
    if relationship_type_variant == 'relationship_type':
        r = Relationship(type_name=relationship_type._name)
    else:
        r = Relationship(template_name=relationship_type._name)

    properties = relationship.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value

    interfaces = relationship.interfaces
    if interfaces:
        for interface_name, interface in interfaces.iteritems():
            interface = normalize_interface(context, interface)
            if interface is not None:
                r.interfaces[interface_name] = interface
    
    return r

def normalize_capability(context, capability):
    capability_type = capability._get_type(context)
    r = Capability(name=capability._name, type_name=capability_type._name)
    
    capability_definition = capability._get_definition(context)
    occurrences = capability_definition.occurrences
    if occurrences is not None:
        r.min_occurrences = occurrences.value[0]
        if occurrences.value[1] != 'UNBOUNDED':
            r.max_occurrences = occurrences.value[1]
    else:
        r.min_occurrences = 1
    
    valid_source_types = capability_definition.valid_source_types
    if valid_source_types:
        r.valid_source_node_type_names = valid_source_types

    properties = capability.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value
    
    return r

def normalize_node_filter(context, node_filter, node_type_constraints):
    if node_filter is None:
        return
    
    properties = node_filter.properties
    if properties is not None:
        for property_name, constraint_clause in properties:
            fn = normalize_constraint_clause(context, node_filter, constraint_clause, property_name, None)
            if fn is not None:
                node_type_constraints.append(fn)

    capabilities = node_filter.capabilities
    if capabilities is not None:
        for capability_name, capability in capabilities: 
            properties = capability.properties
            if properties is not None:
                for property_name, constraint_clause in properties:
                    fn = normalize_constraint_clause(context, node_filter, constraint_clause, property_name, capability_name)
                    if fn is not None:
                        node_type_constraints.append(fn)

def normalize_constraint_clause(context, node_filter, constraint_clause, property_name, capability_name):
    constraint_key = constraint_clause._raw.keys()[0]
    the_type = constraint_clause._get_type(context)

    def coerce(constraint):
        return coerce_value(context, node_filter, the_type, None, None, constraint, constraint_key) if the_type is not None else constraint
    
    def get_value(node_type):
        if capability_name is not None:
            capability = node_type.capabilities.get(capability_name)
            return capability.properties.get(property_name) if capability is not None else None
        return node_type.properties.get(property_name)

    if constraint_key == 'equal':
        constraint = coerce(constraint_clause.equal)

        def equal(node_type):
            value = get_value(node_type)
            return value == constraint
        
        return equal

    elif constraint_key == 'greater_than':
        constraint = coerce(constraint_clause.greater_than)

        def greater_than(node_type):
            value = get_value(node_type)
            return value > constraint
        
        return greater_than

    elif constraint_key == 'greater_or_equal':
        constraint = coerce(constraint_clause.greater_or_equal)

        def greater_or_equal(node_type):
            value = get_value(node_type)
            return value >= constraint
        
        return greater_or_equal

    elif constraint_key == 'less_than':
        constraint = coerce(constraint_clause.less_than)

        def less_than(node_type):
            value = get_value(node_type)
            return value < constraint
        
        return less_than

    elif constraint_key == 'less_or_equal':
        constraint = coerce(constraint_clause.less_or_equal)

        def less_or_equal(node_type):
            value = get_value(node_type)
            return value <= constraint
        
        return less_or_equal

    elif constraint_key == 'in_range':
        lower, upper = constraint_clause.in_range
        lower, upper = coerce(lower), coerce(upper)

        def in_range(node_type):
            value = get_value(node_type)
            if value < lower:
                return False
            if (upper != 'UNBOUNDED') and (value > upper):
                return False
            return True
        
        return in_range

    elif constraint_key == 'valid_values':
        constraint = tuple(coerce(v) for v in constraint_clause.valid_values)

        def valid_values(node_type):
            value = get_value(node_type)
            return value in constraint

        return valid_values

    elif constraint_key == 'length':
        constraint = constraint_clause.length

        def length(node_type):
            value = get_value(node_type)
            return len(value) == constraint

        return length

    elif constraint_key == 'min_length':
        constraint = constraint_clause.min_length

        def min_length(node_type):
            value = get_value(node_type)
            return len(value) >= constraint

        return min_length

    elif constraint_key == 'max_length':
        constraint = constraint_clause.max_length

        def max_length(node_type):
            value = get_value(node_type)
            return len(value) >= constraint

        return max_length

    elif constraint_key == 'pattern':
        constraint = constraint_clause.pattern

        def pattern(node_type):
            # Note: the TOSCA 1.0 spec does not specify the regular expression grammar, so we will just use Python's
            value = node_type.properties.get(property_name)
            return re.match(constraint, str(value)) is not None

        return pattern

    return None

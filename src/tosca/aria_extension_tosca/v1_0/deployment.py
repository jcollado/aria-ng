
from aria.deployment import NodeTemplate, Interface, Operation, Requirement, Relationship, Capability

def get_node_template_deployment(context, node_template):
    r = NodeTemplate()
    
    r.name = node_template._name

    properties = node_template.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value

    requirements = node_template._get_requirements(context)
    if requirements:
        for _, requirement in requirements:
            r.requirements.append(get_requirement_deployment(context, requirement))

    capabilities = node_template._get_capabilities(context)
    if capabilities:
        for capability_name, capability in capabilities.iteritems():
            r.capabilities[capability_name] = get_capability_deployment(context, capability)
    
    return r

def get_interface_deployment(context, interface):
    r = Interface()
    
    r.name = interface._name

    inputs = interface.inputs
    if inputs:
        for input_name, input in inputs.iteritems():
            r.inputs[input_name] = input.value

    operations = interface.operations
    if operations:
        for operation_name, operation in operations.iteritems():
            r.operations[operation_name] = get_operation_deployment(context, operation)
    
    return r

def get_operation_deployment(context, operation):
    r = Operation()

    r.name = operation._name

    implementation = operation.implementation
    if implementation is not None:
        r.implementation = implementation.primary
        dependencies = implementation.dependencies
        if dependencies is not None:
            r.dependencies = dependencies

    inputs = operation.inputs
    if inputs:
        for input_name, input in inputs.iteritems():
            r.inputs[input_name] = input.value
    
    return r

def get_requirement_deployment(context, requirement):
    r = Requirement()
    
    r.name = requirement._name

    node, node_variant = requirement._get_node(context)
    if node is not None:
        if node_variant == 'node_type':
            r.node_type = node._name
        else:
            r.node_template = node._name

    capability, capability_variant = requirement._get_capability(context)
    if capability is not None:
        if capability_variant == 'capability_type':
            r.capability_type = capability._name
        else:
            r.capability_name = capability._name

    relationship = requirement.relationship
    if relationship is not None:
        r.relationship = get_relationship_deployment(context, relationship)
        
    return r

def get_relationship_deployment(context, relationship):
    r = Relationship()

    relationship_type, relationship_type_variant = relationship._get_type(context)
    if relationship_type is not None:
        if relationship_type_variant == 'relationship_type':
            r.type = relationship_type._name
        else:
            r.template = relationship_type._name

    properties = relationship.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value

    interfaces = relationship.interfaces
    if interfaces:
        for interface_name, interface in interfaces.iteritems():
            r.interfaces[interface_name] = get_interface_deployment(context, interface)
    
    return r

def get_capability_deployment(context, capability):
    r = Capability()

    r.name = capability._name

    capability_definition = capability._get_definition(context)
    
    capability_type = capability._get_type(context)
    r.type = capability_type._name
    
    occurrences = capability_definition.occurrences
    if occurrences is not None:
        r.min_occurrences = occurrences.value[0]
        if occurrences.value[1] != 'UNBOUNDED':
            r.max_occurrences = occurrences.value[1]
    else:
        r.min_occurrences = 1
    
    valid_source_types = capability_definition.valid_source_types
    if valid_source_types:
        r.valid_source_node_types = valid_source_types

    properties = capability.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value
    
    return r

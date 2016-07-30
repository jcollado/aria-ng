
from aria.deployment import Topology, Type, NodeTemplate, Interface, Operation, Requirement, Relationship, Capability

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
    r = NodeTemplate(name=node_template._name, type=the_type._name)

    properties = node_template._get_property_values(context)
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop

    requirements = node_template._get_requirements(context)
    if requirements:
        for _, requirement in requirements:
            r.requirements.append(normalize_requirement(context, requirement))

    capabilities = node_template._get_capabilities(context)
    if capabilities:
        for capability_name, capability in capabilities.iteritems():
            r.capabilities[capability_name] = normalize_capability(context, capability)
    
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
            r.operations[operation_name] = normalize_operation(context, operation)
    
    return r

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
            r['node_type'] = node._name
        else:
            r['node_template'] = node._name

    capability, capability_variant = requirement._get_capability(context)
    if capability is not None:
        if capability_variant == 'capability_type':
            r['capability_type'] = capability._name
        else:
            r['capability_name'] = capability._name

    r = Requirement(**r)

    relationship = requirement.relationship
    if relationship is not None:
        r.relationship = normalize_relationship(context, relationship)
        
    return r

def normalize_relationship(context, relationship):
    relationship_type, relationship_type_variant = relationship._get_type(context)
    if relationship_type_variant == 'relationship_type':
        r = Relationship(type=relationship_type._name)
    else:
        r = Relationship(template=relationship_type._name)

    properties = relationship.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value

    interfaces = relationship.interfaces
    if interfaces:
        for interface_name, interface in interfaces.iteritems():
            r.interfaces[interface_name] = normalize_interface(context, interface)
    
    return r

def normalize_capability(context, capability):
    capability_type = capability._get_type(context)
    r = Capability(name=capability._name, type=capability_type._name)
    
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
        r.valid_source_node_types = valid_source_types

    properties = capability.properties
    if properties:
        for property_name, prop in properties.iteritems():
            r.properties[property_name] = prop.value
    
    return r

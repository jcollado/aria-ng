
from aria.deployment import DeploymentTemplate, Type, NodeTemplate, RelationshipTemplate, CapabilityTemplate, GroupTemplate, PolicyTemplate, Interface, Operation, Artifact, Requirement

def get_deployment_template(context, presenter):
    r = DeploymentTemplate()

    normalize_types(context, context.deployment.node_types, presenter.node_types)

    normalize_property_values(r.inputs, presenter.service_template._get_input_values(context))
    normalize_properties(r.outputs, presenter.outputs)

    node_templates = presenter.node_templates
    if node_templates:
        for node_template_name, node_template in node_templates.iteritems():
            r.node_templates[node_template_name] = normalize_node_template(context, node_template)

    return r

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
    
    normalize_property_values(r.properties, node_template._get_property_values(context))
    #normalize_interfaces(context, r.interfaces, node_template._get_interfaces(context))

    return r






#
# Utils
#

def normalize_property_values(properties, source_properties):
    if source_properties:
        for property_name, prop in source_properties.iteritems():
            properties[property_name] = prop

def normalize_properties(properties, source_properties):
    if source_properties:
        for property_name, prop in source_properties.iteritems():
            properties[property_name] = prop.value

def normalize_interfaces(context, interfaces, source_interfaces):
    if source_interfaces:
        for interface_name, interface in source_interfaces.iteritems():
            interface = normalize_interface(context, interface)
            if interface is not None:
                interfaces[interface_name] = interface

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

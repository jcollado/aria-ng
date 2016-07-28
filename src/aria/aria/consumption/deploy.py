
from .consumer import Consumer
from clint.textui import puts, colored, indent

class Deploy(Consumer):
    """
    ARIA deployer.
    
    Created a deployment plan for the presentation.
    """

    def consume(self):
        self.dump()
    
    def dump(self):
        if self.context.presentation.node_templates:
            for node_template_name, node_template in self.context.presentation.node_templates.iteritems():
                puts('Node template: %s' % self.context.style.node(node_template_name))

                requirements = node_template._get_requirements(self.context)
                if requirements:
                    with self.context.style.indent:
                        puts('Requirements:')
                        with self.context.style.indent:
                            for requirement_name, requirement in requirements:
                                puts(self.context.style.node(requirement_name))
                                with self.context.style.indent:
                                    node, node_variant = requirement._get_node(self.context)
                                    if node is not None:
                                        if node_variant == 'node_type':
                                            puts('Node type: %s' % self.context.style.type(node._name))
                                        else:
                                            puts('Node template: %s' % self.context.style.node(node._name))
                                            
                                    capability, capability_variant = requirement._get_capability(self.context)
                                    if capability is not None:
                                        capability_type = capability
                                        if capability_variant == 'capability_type':
                                            puts('Capability type: %s' % self.context.style.type(capability_type._name))
                                        else:
                                            capability_type = capability._get_type(self.context)
                                            puts('Capability name: %s (type: %s)' % (capability._name, self.context.style.type(capability_type._name)))
                                    
                                    relationship = requirement.relationship
                                    if relationship is not None:
                                        relationship_type, relationship_type_variant = relationship._get_type(self.context)
                                        if relationship_type is not None:
                                            if relationship_type_variant == 'relationship_type':
                                                puts('Relationship type: %s' % self.context.style.type(relationship_type._name))
                                            else:
                                                puts('Relationship template: %s' % self.context.style.type(relationship_type._name))
                                        
                                            properties = relationship.properties
                                            if properties:
                                                with self.context.style.indent:
                                                    puts('Properties:')
                                                    with self.context.style.indent:
                                                        for property_name, prop in properties.iteritems():
                                                            puts('%s = %s' % (self.context.style.property(property_name), self.context.style.literal(prop.value)))

                                            interfaces = relationship.interfaces
                                            if interfaces:
                                                with self.context.style.indent:
                                                    puts('Interfaces:')
                                                    with self.context.style.indent:
                                                        for interface_name, interface in interfaces.iteritems():
                                                            the_type = interface._get_type(self.context)
                                                            
                                                            if the_type is not None:
                                                                puts('%s (type: %s)' % (self.context.style.node(interface_name), self.context.style.type(the_type._name)))
                                                            else:
                                                                puts(self.context.style.node(interface_name))
                                                            
                                                            inputs = interface.inputs
                                                            if inputs:
                                                                with self.context.style.indent:
                                                                    puts('Inputs:')
                                                                    with self.context.style.indent:
                                                                        for input_name, input in inputs.iteritems():
                                                                            puts('%s = %s' % (self.context.style.property(input_name), self.context.style.literal(input.value)))

                                                            operations = interface.operations
                                                            if operations:
                                                                with self.context.style.indent:
                                                                    puts('Operations:')
                                                                    with self.context.style.indent:
                                                                        for operation_name, operation in operations.iteritems():
                                                                            implementation = operation.implementation
                                                                            inputs = operation.inputs
                                                                            
                                                                            if implementation is None and not inputs:
                                                                                continue
                                                                            
                                                                            puts(self.context.style.node(operation_name))

                                                                            with self.context.style.indent:
                                                                                if implementation is not None:
                                                                                    puts('Implementation: %s' % implementation.primary)
                                                                                    if implementation.dependencies:
                                                                                        puts('Dependencies: %s' % implementation.dependencies)
    
                                                                                if inputs:
                                                                                    puts('Inputs:')
                                                                                    with self.context.style.indent:
                                                                                        for input_name, input in inputs.iteritems():
                                                                                            puts('%s = %s' % (self.context.style.property(input_name), self.context.style.literal(input.value)))

                capabilities = node_template._get_capabilities(self.context)
                if capabilities:
                    with self.context.style.indent:
                        puts('Capabilities:')
                        with self.context.style.indent:
                            for capability_name, capability in capabilities.iteritems():
                                capability_definition = capability._get_definition(self.context)
                                the_type = capability._get_type(self.context)
                                
                                if the_type is not None:
                                    puts('%s (type: %s)' % (self.context.style.node(capability_name), self.context.style.type(the_type._name)))
                                else:
                                    puts(self.context.style.node(capability_name))
                                
                                with self.context.style.indent:
                                    if capability_definition is not None:
                                        valid_source_types = capability_definition.valid_source_types
                                        if valid_source_types:
                                            puts('Valid source node types: %s' % valid_source_types)

                                    properties = capability.properties
                                    if properties:
                                            puts('Properties:')
                                            with self.context.style.indent:
                                                for property_name, prop in properties.iteritems():
                                                    puts('%s = %s' % (self.context.style.property(property_name), self.context.style.literal(prop.value)))

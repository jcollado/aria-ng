
from .consumer import Consumer
from clint.textui import puts, colored

class Print(Consumer):
    def consume(self):
        puts(self.context.style.section('Type:'))
        with self.context.style.indent:
            puts(self.context.presentation.__class__.__name__)

        if self.context.presentation.service_template.description:
            puts(self.context.style.section('Description:'))
            with self.context.style.indent:
                self.print_description(self.context.presentation.service_template.description)
        
        if self.context.presentation.inputs:
            puts(self.context.style.section('Inputs:'))
            with self.context.style.indent:
                for name, input in self.context.presentation.inputs.iteritems():
                    puts(self.context.style.property(name))
                    if hasattr(input, 'description') and input.description: # cloudify_dsl
                        with self.context.style.indent:
                            self.print_description(input.description)

        if self.context.presentation.outputs:
            puts(self.context.style.section('Outputs:'))
            with self.context.style.indent:
                for name, output in self.context.presentation.outputs.iteritems():
                    puts(self.context.style.property(name))
                    with self.context.style.indent:
                        self.print_description(output.description)
                        for k, v in output.value.iteritems():
                            self.print_assignment(k, v)

        if self.context.presentation.node_types:
            puts(self.context.style.section('Node types:'))
            with self.context.style.indent:
                for name, node_type in self.context.presentation.node_types.iteritems():
                    puts(self.context.style.type(name))
                    with self.context.style.indent:
                        self.print_description(node_type.description)
                        if node_type.derived_from:
                            puts('Derived from: %s' % self.context.style.type(node_type.derived_from))
                        if node_type.properties:
                            puts('Properties:')
                            with self.context.style.indent:
                                for k, property in node_type.properties.iteritems():
                                    puts(self.context.style.property(k))
                                    with self.context.style.indent:
                                        self.print_description(property.description)
                                        if property.type:
                                            puts('Type: %s' % property.type)
                                        if property.default:
                                            self.print_assignment('Default', property.default)
                        if node_type.interfaces:
                            puts('Interfaces:')
                            with self.context.style.indent:
                                for k, interface in node_type.interfaces.iteritems():
                                    self.print_interface(k, interface)

        if self.context.presentation.relationship_types:
            puts(self.context.style.section('Relationship types:'))
            with self.context.style.indent:
                for name, relationship_type in self.context.presentation.relationship_types.iteritems():
                    puts(self.context.style.type(name))
                    self.print_description(relationship_type.description)
                    with self.context.style.indent:
                        if relationship_type.derived_from:
                            puts('Derived from: %s' % self.context.style.type(relationship_type.derived_from))
                        if hasattr(relationship_type, 'target_interfaces') and relationship_type.target_interfaces: # cloudify_dsl
                            puts('Target interfaces:')
                            with self.context.style.indent:
                                for k, target_interface in relationship_type.target_interfaces.iteritems():
                                    self.print_interface(k, target_interface)
        
        if self.context.presentation.node_templates:
            puts(self.context.style.section('Node templates:'))
            with self.context.style.indent:
                for name, node_template in self.context.presentation.node_templates.iteritems():
                    puts(self.context.style.node(name))
                    with self.context.style.indent:
                        self.print_description(node_template.description)
                        puts('Type: %s' % self.context.style.type(node_template.type))
                        if node_template.properties:
                            puts('Properties:')
                            with self.context.style.indent:
                                for k, v in node_template.properties.iteritems():
                                    self.print_assignment(k, v.value)
                        if hasattr(node_template, 'node_template.relationships') and node_template.relationships: # cloudify_dsl
                            puts('Relationships:')
                            with self.context.style.indent:
                                for relationship in node_template.relationships:
                                    puts(self.context.style.type(relationship.type))
                                    with self.context.style.indent:
                                        puts('Target: %s' % self.context.style.node(relationship.target))

    def print_description(self, description):
        if description:
            puts(colored.green(description.strip()))

    def print_assignment(self, k, value):
        if isinstance(value, dict):
            puts('%s: ' % k)
            with self.context.style.indent:
                for kk, vv in value.iteritems():
                    self.print_assignment(kk, vv)
        else:
            puts('%s: %s' % (k, self.context.style.literal(value)))

    def print_interface(self, k, interface):
        puts(self.context.style.type(k))
        with self.context.style.indent:
            if hasattr(interface, 'operations') and interface.operations: # cloudify_dsl
                puts('Operations:')
                with self.context.style.indent:
                    for kk, operation in interface.operations.iteritems():
                        puts(self.context.style.property(kk))
                        with self.context.style.indent:
                            if operation.implementation:
                                if '/' in operation.implementation:
                                    puts('Implementation: %s' % self.context.style.literal(operation.implementation))
                                else:
                                    puts('Implementation: %s' % self.context.style.type(operation.implementation))
                            if hasattr(operation, 'executor') and operation.executor:
                                puts('Executor: %s' % self.context.style.node(operation.executor))
                            if operation.inputs:
                                puts('Inputs:') # TODO
                                with self.context.style.indent:
                                    for kkk, v in operation.inputs.iteritems():
                                        self.print_assignment(kkk, v)

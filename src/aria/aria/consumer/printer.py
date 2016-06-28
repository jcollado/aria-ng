
from ..consumer import Consumer
from .style import Style
from clint.textui import puts, colored, indent

class Printer(Consumer):
    def __init__(self, presentation, args=[], style=Style()):
        super(Printer, self).__init__(presentation, args)
        self.style = style

    def consume(self):
        puts(self.style.section('Type:'))
        with self.style.indent:
            puts(self.presentation.__class__.__name__)

        if self.presentation.service_template.description:
            puts(self.style.section('Description:'))
            with self.style.indent:
                self.print_description(self.presentation.service_template.description)
        
        if self.presentation.inputs:
            puts(self.style.section('Inputs:'))
            with self.style.indent:
                for name, input in self.presentation.inputs.iteritems():
                    puts(self.style.property(name))
                    if hasattr(input, 'description') and input.description: # cloudify_dsl
                        with self.style.indent:
                            self.print_description(input.description)

        if self.presentation.outputs:
            puts(self.style.section('Outputs:'))
            with self.style.indent:
                for name, output in self.presentation.outputs.iteritems():
                    puts(self.style.property(name))
                    with self.style.indent:
                        self.print_description(output.description)
                        for k, v in output.value.iteritems():
                            self.print_assignment(k, v)

        if self.presentation.node_types:
            puts(self.style.section('Node types:'))
            with self.style.indent:
                for name, node_type in self.presentation.node_types.iteritems():
                    puts(self.style.type(name))
                    with self.style.indent:
                        self.print_description(node_type.description)
                        if node_type.derived_from:
                            puts('Derived from: %s' % self.style.type(node_type.derived_from))
                        if node_type.properties:
                            puts('Properties:')
                            with self.style.indent:
                                for k, property in node_type.properties.iteritems():
                                    puts(self.style.property(k))
                                    with self.style.indent:
                                        self.print_description(property.description)
                                        if property.type:
                                            puts('Type: %s' % property.type)
                                        if property.default:
                                            self.print_assignment('Default', property.default)
                        if node_type.interfaces:
                            puts('Interfaces:')
                            with self.style.indent:
                                for k, interface in node_type.interfaces.iteritems():
                                    self.print_interface(k, interface)

        if self.presentation.relationship_types:
            puts(self.style.section('Relationship types:'))
            with self.style.indent:
                for name, relationship_type in self.presentation.relationship_types.iteritems():
                    puts(self.style.type(name))
                    self.print_description(relationship_type.description)
                    with self.style.indent:
                        if relationship_type.derived_from:
                            puts('Derived from: %s' % self.style.type(relationship_type.derived_from))
                        if relationship_type.target_interfaces:
                            puts('Target interfaces:')
                            with self.style.indent:
                                for k, target_interface in relationship_type.target_interfaces.iteritems():
                                    self.print_interface(k, target_interface)
        
        if self.presentation.node_templates:
            puts(self.style.section('Node templates:'))
            with self.style.indent:
                for name, node_template in self.presentation.node_templates.iteritems():
                    puts(self.style.node(name))
                    with self.style.indent:
                        puts('Type: %s' % self.style.type(node_template.type))
                        if node_template.properties:
                            puts('Properties:')
                            with self.style.indent:
                                for k, v in node_template.properties.iteritems():
                                    self.print_assignment(k, v.value)
                        if hasattr(node_template, 'node_template.relationships') and node_template.relationships: # cloudify_dsl
                            puts('Relationships:')
                            with self.style.indent:
                                for relationship in node_template.relationships:
                                    puts(self.style.type(relationship.type))
                                    with self.style.indent:
                                        puts('Target: %s' % self.style.node(relationship.target))

    def print_description(self, description):
        if description:
            puts(colored.green(description.strip()))

    def print_assignment(self, k, value):
        if isinstance(value, dict):
            puts('%s: ' % k)
            with self.style.indent:
                for kk, vv in value.iteritems():
                    self.print_assignment(kk, vv)
        else:
            puts('%s: %s' % (k, self.style.literal(value)))

    def print_interface(self, k, interface):
        puts(self.style.type(k))
        with self.style.indent:
            if interface.operations:
                puts('Operations:')
                with self.style.indent:
                    for kk, operation in interface.operations.iteritems():
                        puts(self.style.property(kk))
                        with self.style.indent:
                            if operation.implementation:
                                if '/' in operation.implementation:
                                    puts('Implementation: %s' % self.style.literal(operation.implementation))
                                else:
                                    puts('Implementation: %s' % self.style.type(operation.implementation))
                            if operation.executor:
                                puts('Executor: %s' % self.style.node(operation.executor))
                            if operation.inputs:
                                puts('Inputs:') # TODO
                                with self.style.indent:
                                    for kkk, v in operation.inputs.iteritems():
                                        self.print_assignment(kkk, v)

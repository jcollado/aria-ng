
from consumer import Consumer
from aria.presenter.cloudify import CloudifyPresenter1_3
from clint.textui import puts, colored, indent

class Printer(Consumer):
    def __init__(self, presentation, indent=2):
        super(Printer, self).__init__(presentation)
        self.indent = 2

    def consume(self):
        puts(self._section('Type:') + ' %s' % self.presentation.__class__.__name__)

        if isinstance(self.presentation, CloudifyPresenter1_3):
            self._print_cloudify()
        
    def _print_cloudify(self):
        profile = self.presentation.profile

        if profile.description:
            puts(self._section('Description:'))
            with indent(self.indent):
                self._print_description(profile.description)
        
        if profile.inputs:
            puts(self._section('Inputs:'))
            with indent(self.indent):
                for name, input in profile.inputs.iteritems():
                    puts(self._property(name))
                    with indent(self.indent):
                        self._print_description(input.description)

        if profile.outputs:
            puts(self._section('Outputs:'))
            with indent(self.indent):
                for name, output in profile.outputs.iteritems():
                    puts(self._property(name))
                    with indent(self.indent):
                        self._print_description(output.description)
                        for k, v in output.value.iteritems():
                            self._print_assignment(k, v.value)

        if profile.node_types:
            puts(self._section('Node types:'))
            with indent(self.indent):
                for name, node_type in profile.node_types.iteritems():
                    puts(self._type(name))
                    with indent(self.indent):
                        self._print_description(node_type.description)
                        if node_type.derived_from:
                            puts('Derived from: %s' % self._type(node_type.derived_from))
                        if node_type.properties:
                            puts('Properties:')
                            with indent(self.indent):
                                for k, property in node_type.properties.iteritems():
                                    puts(self._property(k))
                                    with indent(self.indent):
                                        self._print_description(property.description)
                                        if property.type:
                                            puts('Type: %s' % property.type)
                                        if property.default:
                                            self._print_assignment('Default', property.default)
                        if node_type.interfaces:
                            puts('Interfaces:')
                            with indent(self.indent):
                                for k, interface in node_type.interfaces.iteritems():
                                    self._print_interface(k, interface)

        if profile.relationships:
            puts(self._section('Relationships:'))
            with indent(self.indent):
                for name, relationship in profile.relationships.iteritems():
                    puts(self._type(name))
                    self._print_description(relationship.description)
                    with indent(self.indent):
                        if relationship.derived_from:
                            puts('Derived from: %s' % self._type(relationship.derived_from))
                        if relationship.target_interfaces:
                            puts('Target interfaces:')
                            with indent(self.indent):
                                for k, target_interface in relationship.target_interfaces.iteritems():
                                    self._print_interface(k, target_interface)
        
        if profile.node_templates:
            puts(self._section('Node templates:'))
            with indent(self.indent):
                for name, node_template in profile.node_templates.iteritems():
                    puts(self._node(name))
                    with indent(self.indent):
                        puts('Type: %s' % self._type(node_template.type))
                        if node_template.properties:
                            puts('Properties:')
                            with indent(self.indent):
                                for k, v in node_template.properties.iteritems():
                                    self._print_assignment(k, v.value)
                        if node_template.relationships:
                            puts('Relationships:')
                            with indent(self.indent):
                                for relationship in node_template.relationships:
                                    puts(self._type(relationship.type))
                                    with indent(self.indent):
                                        puts('Target: %s' % self._node(relationship.target))

    def _print_description(self, description):
        if description:
            puts(colored.green(description.strip()))

    def _print_assignment(self, k, value):
        if isinstance(value, dict):
            puts('%s: ' % k)
            with indent(self.indent):
                for kk, vv in value.iteritems():
                    self._print_assignment(kk, vv)
        else:
            puts('%s: %s' % (k, self._literal(value)))

    def _section(self, value):
        return colored.cyan(value, bold=True)
    
    def _type(self, value):
        return colored.blue(value, bold=True)

    def _node(self, value):
        return colored.red(value, bold=True)
    
    def _property(self, value):
        return colored.magenta(value, bold=True)

    def _literal(self, value):
        return colored.yellow(repr(value), bold=True)

    def _print_interface(self, k, interface):
        puts(self._type(k))
        with indent(self.indent):
            if interface.workflows:
                puts('Workflows:')
                with indent(self.indent):
                    for kk, workflow in interface.workflows.iteritems():
                        puts(self._property(kk))
                        with indent(self.indent):
                            if workflow.implementation:
                                if '/' in workflow.implementation:
                                    puts('Implementation: %s' % self._literal(workflow.implementation))
                                else:
                                    puts('Implementation: %s' % self._type(workflow.implementation))
                            if workflow.executor:
                                puts('Executor: %s' % self._node(workflow.executor))
                            if workflow.inputs:
                                puts('Inputs:') # TODO
                                with indent(self.indent):
                                    for kkk, v in workflow.inputs.iteritems():
                                        self._print_assignment(kkk, v.value)

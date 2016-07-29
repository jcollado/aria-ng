
from clint.textui import puts
from collections import OrderedDict

class Deployment(object):
    def __init__(self):
        self.node_templates = OrderedDict()
        self.groups = OrderedDict()
        self.policies = OrderedDict()

    def link(self, context):
        for node_template in self.node_templates.itervalues():
            for requirement in node_template.requirements:
                if requirement.node_template is None:
                    print requirement

    def dump(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.dump(context)

class NodeTemplate(object):
    def __init__(self):
        self.name = None
        self.properties = OrderedDict()
        self.interfaces = OrderedDict()
        self.requirements = []
        self.capabilities = OrderedDict()
    
    def dump(self, context):
        puts('Node template: %s' % context.style.node(self.name))
        dump_properties(context, self.properties)
        if self.interfaces:
            with context.style.indent:
                puts('Interfaces:')
                with context.style.indent:
                    for interface in self.interfaces.itervalues():
                        interface.dump(context)
        if self.requirements:
            with context.style.indent:
                puts('Requirements:')
                with context.style.indent:
                    for requirement in self.requirements:
                        requirement.dump(context)
        if self.capabilities:
            with context.style.indent:
                puts('Capabilities:')
                with context.style.indent:
                    for capabilitiy in self.capabilities.itervalues():
                        capabilitiy.dump(context)

class Interface(object):
    def __init__(self):
        self.name = None
        self.inputs = OrderedDict()
        self.operations = OrderedDict()

    def dump(self, context):
        dump_properties(context, self.inputs, 'Inputs')
        if self.operations:
            with context.style.indent:
                puts('Operations:')
                with context.style.indent:
                    for operation in self.operations.itervalues():
                        operation.dump(context)
        

class Operation(object):
    def __init__(self):
        self.name = None
        self.implementation = None
        self.dependencies = []
        self.inputs = OrderedDict()

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.implementation:
                puts('Implementation: %s' % context.style.literal(self.implementation))
            if self.dependencies:
                puts('Dependencies: %s' % ', '.join((str(context.style.literal(v)) for v in self.dependencies)))
        dump_properties(context, self.inputs, 'Inputs')

class Requirement(object):
    def __init__(self):
        self.name = None
        self.node_type = None
        self.node_template = None
        self.capability_type = None
        self.capability_name = None
        self.relationship = None

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.node_type:
                puts('Node type: %s' % context.style.type(self.node_type))
            elif self.node_template:
                puts('Node template: %s' % context.style.node(self.node_template))
            if self.capability_type:
                puts('Capability type: %s' % context.style.type(self.capability_type))
            else:
                puts('Capability name: %s' % context.style.node(self.capability_name))
            if self.relationship:
                self.relationship.dump(context)

class Relationship(object):
    def __init__(self):
        self.type = None
        self.template = None
        self.properties = OrderedDict()
        self.interfaces = OrderedDict()

    def dump(self, context):
        if self.type:
            puts('Relationship type: %s' % context.style.type(self.type))
        else:
            puts('Relationship template: %s' % context.style.node(self.template))
        dump_properties(context, self.properties)
        if self.interfaces:
            with context.style.indent:
                puts('Interfaces:')
                for interface in self.interfaces.itervalues():
                    interface.dump(context)

class Capability(object):
    def __init__(self):
        self.name = None
        self.type = None
        self.occurrences = 0
        self.min_occurrences = None
        self.max_occurrences = None
        self.valid_source_node_types = []
        self.properties = OrderedDict()

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type))
            puts('Occurrences: %s (%s%s)' % (self.occurrences, self.min_occurrences or 0, (' to %d' % self.max_occurrences) if self.max_occurrences is not None else ' or more'))
            if self.valid_source_node_types:
                puts('Valid source node types: %s' % ', '.join((str(context.style.type(v)) for v in self.valid_source_node_types)))
        dump_properties(context, self.properties)

def dump_properties(context, properties, name='Properties'):
    if not properties:
        return
    with context.style.indent:
        puts('%s:' % name)
        with context.style.indent:
            for property_name, value in properties.iteritems():
                puts('%s = %s' % (context.style.property(property_name), context.style.literal(value)))

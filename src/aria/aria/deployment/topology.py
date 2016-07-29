
from .. import Issue
from clint.textui import puts
from collections import OrderedDict

class Topology(object):
    def __init__(self):
        self.node_templates = OrderedDict()
        self.groups = OrderedDict()
        self.policies = OrderedDict()

    def link(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.link(context, self)
                    
    def find_target_node_template(self, context, requirement, source_node_template):
        for target_node_template in self.node_templates.itervalues():
            target_capability = None
            
            # Try to match node type
            if requirement.node_type is not None:
                if requirement.node_type != target_node_template.type:
                    continue
            
            # Try to match capability name
            if requirement.capability_name is not None:
                if requirement.capability_name in target_node_template.capabilities:
                    target_capability = target_node_template.capabilities[requirement.capability_name]
                else:
                    continue
                #elif requirement.capability_type is not None:
                #    # Make sure the matching capability is of the right type
                #    capability = target_node_template.capabilities[requirement.capability_name]
                #    if requirement.capability_type != capability.type:
                #        context.validation.report('requirement "%s" in "%s" refers to a capability of type "%s" but it is a "%s"' % (requirement.name, source_node_template.name, requirement.capability_type, capability.type), level=Issue.BETWEEN_INSTANCES)

            # Try to match capability type
            elif requirement.capability_type is not None:
                for capability in target_node_template.capabilities.itervalues():
                    if requirement.capability_type == capability.type:
                        target_capability = capability
                        break
                if target_capability is None:
                    continue
            
            return target_node_template, target_capability
        
        return None, None
            

    def dump(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.dump(context)

class NodeTemplate(object):
    def __init__(self):
        self.name = None # required
        self.type = None # required
        self.properties = OrderedDict()
        self.interfaces = OrderedDict()
        self.requirements = []
        self.capabilities = OrderedDict()
    
    def link(self, context, topology):
        for requirement in self.requirements:
            requirement.link(context, topology, self)
    
    def dump(self, context):
        puts('Node template: %s' % context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)
        with context.style.indent:
            if self.requirements:
                puts('Requirements:')
                with context.style.indent:
                    for requirement in self.requirements:
                        requirement.dump(context)
            if self.capabilities:
                puts('Capabilities:')
                with context.style.indent:
                    for capabilitiy in self.capabilities.itervalues():
                        capabilitiy.dump(context)

class Interface(object):
    def __init__(self):
        self.name = None # required
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
        self.name = None # required
        self.implementation = None # optional
        self.dependencies = []
        self.inputs = OrderedDict()

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.implementation is not None:
                puts('Implementation: %s' % context.style.literal(self.implementation))
            if self.dependencies:
                puts('Dependencies: %s' % ', '.join((str(context.style.literal(v)) for v in self.dependencies)))
        dump_properties(context, self.inputs, 'Inputs')

class Requirement(object):
    def __init__(self):
        self.name = None # required
        self.node_type = None # either this or node_template can be set
        self.node_template = None # either this or node_type can be set
        self.capability_type = None # either this or capability_name can be set
        self.capability_name = None # either this or capability_type can be set
        self.relationship = None # optional

    def link(self, context, topology, node_template):
        if self.node_template is None:
            target_node_template, target_capability = topology.find_target_node_template(context, self, node_template)
            if target_node_template is not None:
                puts('%s -> %s.%s' % (node_template.name, target_node_template.name, target_capability.name))
                self.relate(context, target_node_template, target_capability)
            else:
                context.validation.report('requirement "%s" in node template "%s" has no target node template' % (self.name, node_template.name), level=Issue.BETWEEN_INSTANCES)

    def relate(self, context, target_node_template, target_capability):
        if target_capability.relate(context):
            self.node_template = target_node_template.name
            self.node_type = None
            self.capability_name = target_capability.name
            self.capability_type = None

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.node_type is not None:
                puts('Node type: %s' % context.style.type(self.node_type))
            elif self.node_template is not None:
                puts('Node template: %s' % context.style.node(self.node_template))
            if self.capability_type is not None:
                puts('Capability type: %s' % context.style.type(self.capability_type))
            elif self.capability_name is not None:
                puts('Capability name: %s' % context.style.node(self.capability_name))
            if self.relationship:
                self.relationship.dump(context)

class Relationship(object):
    def __init__(self):
        self.type = None # either this or template must be set
        self.template = None # either this or type must be set
        self.properties = OrderedDict()
        self.interfaces = OrderedDict()

    def dump(self, context):
        if self.type is not None:
            puts('Relationship type: %s' % context.style.type(self.type))
        else:
            puts('Relationship template: %s' % context.style.node(self.template))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)

class Capability(object):
    def __init__(self):
        self.name = None # required
        self.type = None # required
        self.min_occurrences = None # optional
        self.max_occurrences = None # optional
        self.valid_source_node_types = []
        self.properties = OrderedDict()
        self.occurrences = 0

    def relate(self, context):
        if self.max_occurrences is not None:
            if self.occurrences == self.max_occurrences:
                context.validation.report(':(')
                return False
        self.occurrences += 1
        return True 

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

def dump_interfaces(context, interfaces):
    if not interfaces:
        return
    with context.style.indent:
        puts('Interfaces:')
        for interface in interfaces.itervalues():
            interface.dump(context)

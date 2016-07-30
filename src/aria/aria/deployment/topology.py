
from .. import Issue
from ..utils import StrictList, StrictDict
from .plan import Node
from .ids import generate_id
from clint.textui import puts
from collections import OrderedDict

class Topology(object):
    def __init__(self):
        self.node_types = TypeHierarchy()
        self.capability_types = TypeHierarchy()
        self.node_templates = StrictDict(str, NodeTemplate)
        self.groups = OrderedDict() # TODO
        self.policies = OrderedDict() # TODO

    def link(self, context):
        linked = True
        for node_template in self.node_templates.itervalues():
            if not node_template.link(context, self):
                linked = False
        return linked
                    
    def find_target_node_template(self, context, source_node_template, requirement):
        for target_node_template in self.node_templates.itervalues():
            target_capability = None

            # Try to match node template
            if requirement.node_template is not None:
                if requirement.node_template != target_node_template.name:
                    continue
            
            # Try to match node type
            if requirement.node_type is not None:
                if not self.node_types.is_descendant(requirement.node_type, target_node_template.type):
                    continue
            
            # Try to match capability name
            if requirement.capability_name is not None:
                if requirement.capability_name in target_node_template.capabilities:
                    target_capability = target_node_template.capabilities[requirement.capability_name]
                else:
                    continue

            # Try to match capability type
            elif requirement.capability_type is not None:
                for capability in target_node_template.capabilities.itervalues():
                    if self.capability_types.is_descendant(requirement.capability_type, capability.type):
                        target_capability = capability
                        break
                if target_capability is None:
                    continue
            
            return target_node_template, target_capability
        
        return None, None

    def validate(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.validate(context, self)
        for group in self.groups.itervalues():
            group.validate(context, self)
        for policy in self.policies.itervalues():
            policy.validate(context, self)

    def dump(self, context):
        if self.node_types:
            puts('Node types:')
            self.node_types.dump(context)
        if self.capability_types:
            puts('Capability types:')
            self.capability_types.dump(context)
        for node_template in self.node_templates.itervalues():
            node_template.dump(context)

class Type(object):
    def __init__(self, name):
        if not name:
            raise ValueError('must set name')
        self.name = name
        self.children = StrictList(Type)
    
    def get_descendant(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.get_descendant(name)
            if found is not None:
                return found
        return None
    
    def is_descendant(self, base_name, name):
        base = self.get_descendant(base_name)
        if base is not None:
            if base.get_descendant(name) is not None:
                print base_name, name
                return True
        return False
    
    def dump(self, context):
        if self.name:
            puts(context.style.type(self.name))
        with context.style.indent:
            for child in self.children:
                child.dump(context)

class TypeHierarchy(Type):
    def __init__(self):
        self.name = None
        self.children = StrictList(Type)

class NodeTemplate(object):
    def __init__(self, name, type):
        if (not name) or (not type):
            raise ValueError('must set name and type')
        self.name = name
        self.type = type
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.requirements = StrictList(Requirement)
        self.capabilities = StrictDict(str, Capability)
    
    def instantiate(self):
        id = generate_id()
        id = '%s_%s' % (self.name, id)
        return Node(id, self)
    
    @property
    def requirements_satisfied(self):
        for requirement in self.requirements:
            if not requirement.satisfied:
                return False
        return True
    
    def link(self, context, topology):
        satisfied = True
        for requirement in self.requirements:
            if not requirement.satisfied:
                if not requirement.link(context, topology, self):
                    satisfied = False
        return satisfied

    def validate(self, context, topology):
        if topology.node_types.get_descendant(self.type) is None:
            context.validation.report('node template "%s" has an unknown type: %s' % (self.name, repr(self.type)), level=Issue.BETWEEN_TYPES)        
        for interface in self.interfaces.itervalues():
            interface.validate(context, topology)
        for requirement in self.requirements:
            requirement.validate(context, topology)
        for capability in self.capabilities.itervalues():
            capability.validate(context, topology)
    
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
    def __init__(self, name):
        if not name:
            raise ValueError('must set name')
        self.name = name
        self.inputs = StrictDict(str)
        self.operations = StrictDict(str, Operation)

    def validate(self, context, topology):
        for operation in self.operations.itervalues():
            operation.validate(context, topology)

    def dump(self, context):
        dump_properties(context, self.inputs, 'Inputs')
        if self.operations:
            with context.style.indent:
                puts('Operations:')
                with context.style.indent:
                    for operation in self.operations.itervalues():
                        operation.dump(context)
        

class Operation(object):
    def __init__(self, name):
        if not name:
            raise ValueError('must set name')
        self.name = name
        self.implementation = None
        self.dependencies = StrictList(str)
        self.inputs = StrictDict(str)

    def validate(self, context, topology):
        pass

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.implementation is not None:
                puts('Implementation: %s' % context.style.literal(self.implementation))
            if self.dependencies:
                puts('Dependencies: %s' % ', '.join((str(context.style.literal(v)) for v in self.dependencies)))
        dump_properties(context, self.inputs, 'Inputs')

class Requirement(object):
    def __init__(self, name, node_type=None, node_template=None, capability_type=None, capability_name=None):
        if not name:
            raise ValueError('must set name')
        if (node_type and node_template) or ((not node_type) and (not node_template)):
            raise ValueError('must set either node_type or node_template')
        if capability_type and capability_name:
            raise ValueError('can set either capability_type or capability_name')
        self.name = name
        self.node_type = node_type
        self.node_template = node_template
        self.capability_type = capability_type
        self.capability_name = capability_name
        self.relationship = None # optional

    @property
    def satisfied(self):
        return self.node_template is not None

    def link(self, context, topology, node_template):
        if self.satisfied:
            return True
        target_node_template, target_capability = topology.find_target_node_template(context, node_template, self)
        if target_node_template is not None:
            #puts('%s.%s -> %s.%s' % (node_template.name, self.name, target_node_template.name, target_capability.name))
            return self.relate(context, target_node_template, target_capability)
        else:
            context.validation.report('requirement "%s" in node template "%s" has no target node template' % (self.name, node_template.name), level=Issue.BETWEEN_TYPES)
        return False

    def relate(self, context, target_node_template, target_capability):
        if not target_capability.relate(context):
            return False
        self.node_template = target_node_template.name
        self.node_type = None
        self.capability_name = target_capability.name
        self.capability_type = None
        return True

    def validate(self, context, topology):
        if (self.node_type) and (topology.node_types.get_descendant(self.node_type) is None):
            context.validation.report('requirement "%s" refers to an unknown node type: %s' % (self.name, repr(self.node_type)), level=Issue.BETWEEN_TYPES)        
        if (self.capability_type) and (topology.capability_types.get_descendant(self.capability_type) is None):
            context.validation.report('requirement "%s" refers to an unknown capability type: %s' % (self.name, repr(self.capability_type)), level=Issue.BETWEEN_TYPES)        
        if self.relationship:
            self.relationship.validate(context, topology)

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
    def __init__(self, type=None, template=None):
        # TODO: do we really need type and/or template?
        if (type and template) or ((not type) and (not template)):
            raise ValueError('must set either type or template')
        self.type = type
        self.template = template
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)

    def validate(self, context, topology):
        # TODO: check type?
        for interface in self.interfaces.itervalues():
            interface.validate(context, topology)

    def dump(self, context):
        if self.type is not None:
            puts('Relationship type: %s' % context.style.type(self.type))
        else:
            puts('Relationship template: %s' % context.style.node(self.template))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)

class Capability(object):
    def __init__(self, name, type):
        if (not name) or (not type):
            raise ValueError('must set name and type')
        self.name = name
        self.type = type
        self.min_occurrences = None # optional
        self.max_occurrences = None # optional
        self.valid_source_node_types = []
        self.properties = StrictDict(str)
        self.occurrences = 0

    def relate(self, context):
        # TODO: this check should be in the plan, not the topology
        if self.max_occurrences is not None:
            if self.occurrences == self.max_occurrences:
                context.validation.report(':(')
                return False
        self.occurrences += 1
        return True 

    def validate(self, context, topology):
        if topology.capability_types.get_descendant(self.type) is None:
            context.validation.report('capability "%s" has an unknown type: %s' % (self.name, repr(self.type)), level=Issue.BETWEEN_TYPES)        

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

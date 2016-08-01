
from .. import Issue
from ..utils import StrictList, StrictDict
from .plan import Node
from .ids import generate_id
from clint.textui import puts
from collections import OrderedDict
from types import FunctionType

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
                    
    def find_target_node_template_capability(self, context, source_node_template, requirement):
        for target_node_template in self.node_templates.itervalues():
            target_capability = None

            if requirement.node_template_name is not None:
                # Try to match node template
                if requirement.node_template_name != target_node_template.name:
                    continue
            
            if requirement.node_type_name is not None:
                # Try to match node type
                if not self.node_types.is_descendant(requirement.node_type_name, target_node_template.type_name):
                    continue
                
            if source_node_template.target_node_type_constraints:
                # Apply node constraints
                for node_type_constraint in source_node_template.target_node_type_constraints:
                    if not node_type_constraint(target_node_template):
                        target_node_template = None
                        break
                if target_node_template is None:
                    continue

            if requirement.capability_name is not None:
                # Try to match capability name
                if requirement.capability_name in target_node_template.capabilities:
                    target_capability = target_node_template.capabilities[requirement.capability_name]
                else:
                    continue

            elif requirement.capability_type_name is not None:
                # Try to match capability type
                for capability in target_node_template.capabilities.itervalues():
                    if self.capability_types.is_descendant(requirement.capability_type_name, capability.type_name):
                        if capability.valid_source_node_type_names is None:
                            target_capability = capability
                        else:
                            # Are we in valid_source_node_type_names?
                            for valid_source_node_type_name in capability.valid_source_node_type_names:
                                if self.node_types.is_descendant(valid_source_node_type_name, source_node_template.type_name):
                                    target_capability = capability
                                    break
                        if target_capability is not None:
                            break
                if target_capability is None:
                    continue
            
            if (target_capability is not None) and requirement.node_type_constraints:
                # Apply requirement constraints
                for node_type_constraint in requirement.node_type_constraints:
                    if not node_type_constraint(target_node_template):
                        target_capability = None
                        continue
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
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
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
    def __init__(self, name, type_name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if not isinstance(type_name, basestring):
            raise ValueError('must set type_name (string)')
        
        self.name = name
        self.type_name = type_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.requirements = StrictList(Requirement)
        self.capabilities = StrictDict(str, Capability)
        self.target_node_type_constraints = StrictList(FunctionType)
    
    def instantiate(self):
        id = generate_id()
        id = '%s_%s' % (self.name, id)
        return Node(id, self)
    
    def link(self, context, topology):
        satisfied = True
        for requirement in self.requirements:
            if not requirement.link(context, topology, self):
                satisfied = False
        return satisfied

    def validate(self, context, topology):
        if topology.node_types.get_descendant(self.type_name) is None:
            context.validation.report('node template "%s" has an unknown type: %s' % (self.name, repr(self.type_name)), level=Issue.BETWEEN_TYPES)        
        for interface in self.interfaces.itervalues():
            interface.validate(context, topology)
        for requirement in self.requirements:
            requirement.validate(context, topology)
        for capability in self.capabilities.itervalues():
            capability.validate(context, topology)
    
    def dump(self, context):
        puts('Node template: %s' % context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
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
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
        self.name = name
        self.inputs = StrictDict(str)
        self.operations = StrictDict(str, Operation)

    def validate(self, context, topology):
        for operation in self.operations.itervalues():
            operation.validate(context, topology)

    def dump(self, context):
        puts(context.style.node(self.name))
        dump_properties(context, self.inputs, 'Inputs')
        with context.style.indent:
            if self.operations:
                puts('Operations:')
                with context.style.indent:
                    for operation in self.operations.itervalues():
                        operation.dump(context)
        

class Operation(object):
    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
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
    def __init__(self, name, node_type_name=None, node_template_name=None, capability_type_name=None, capability_name=None):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if node_type_name and not isinstance(node_type_name, basestring):
            raise ValueError('node_type_name must be string')
        if node_template_name and not isinstance(node_template_name, basestring):
            raise ValueError('node_template_name must be string')
        if capability_type_name and not isinstance(capability_type_name, basestring):
            raise ValueError('capability_type_name must be string')
        if capability_name and not isinstance(capability_name, basestring):
            raise ValueError('capability_name must be string')
        if (node_type_name and node_template_name) or ((not node_type_name) and (not node_template_name)):
            raise ValueError('must set either node_type_name or node_template_name')
        if capability_type_name and capability_name:
            raise ValueError('can set either capability_type_name or capability_name')
        
        self.name = name
        self.node_type_name = node_type_name
        self.node_template_name = node_template_name
        self.node_type_constraints = StrictList(FunctionType)
        self.capability_type_name = capability_type_name
        self.capability_name = capability_name
        self.relationship = None # optional

    def link(self, context, topology, node_template):
        if self.node_template_name:
            # Apply node template constraints
            if node_template.target_node_type_constraints:
                target_node_template = topology.node_templates[self.node_template_name] 
                for node_type_constraint in node_template.target_node_type_constraints:
                    if not node_type_constraint(target_node_template):
                        context.validation.report('requirement "%s" in node template "%s" is for node template "%s" but it does not match constraints' % (self.name, self.node_template_name, node_template.name), level=Issue.BETWEEN_TYPES)
                        return False
            return True
        
        target_node_template, target_capability = topology.find_target_node_template_capability(context, node_template, self)
        if target_node_template is not None:
            #puts('%s.%s -> %s.%s' % (node_template.name, self.name, target_node_template.name, target_capability.name))
            return self.relate(context, target_node_template, target_capability)
        else:
            context.validation.report('requirement "%s" in node template "%s" has no target node template' % (self.name, node_template.name), level=Issue.BETWEEN_TYPES)
        return False

    def relate(self, context, target_node_template, target_capability):
        if not target_capability.relate(context):
            return False
        self.node_template_name = target_node_template.name
        self.capability_name = target_capability.name
        self.node_type_name = None
        self.capability_type_name = None
        return True

    def validate(self, context, topology):
        if (self.node_type_name) and (topology.node_types.get_descendant(self.node_type_name) is None):
            context.validation.report('requirement "%s" refers to an unknown node type: %s' % (self.name, repr(self.node_type_name)), level=Issue.BETWEEN_TYPES)        
        if (self.capability_type_name) and (topology.capability_types.get_descendant(self.capability_type_name) is None):
            context.validation.report('requirement "%s" refers to an unknown capability type: %s' % (self.name, repr(self.capability_type_name)), level=Issue.BETWEEN_TYPES)        
        if self.relationship:
            self.relationship.validate(context, topology)

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.node_type_name is not None:
                puts('Node type: %s' % context.style.type(self.node_type_name))
            elif self.node_template_name is not None:
                puts('Node template: %s' % context.style.node(self.node_template_name))
            if self.capability_type_name is not None:
                puts('Capability type: %s' % context.style.type(self.capability_type_name))
            elif self.capability_name is not None:
                puts('Capability name: %s' % context.style.node(self.capability_name))
            if self.relationship:
                self.relationship.dump(context)

class Relationship(object):
    def __init__(self, type_name=None, template_name=None):
        # TODO: do we really need type_name and/or template_name?
        if type_name and not isinstance(type_name, basestring):
            raise ValueError('type_name must be string')
        if template_name and not isinstance(template_name, basestring):
            raise ValueError('template_name must be string')
        if (type_name and template_name) or ((not type_name) and (not template_name)):
            raise ValueError('must set either type_name or template_name')
        
        self.type_name = type_name
        self.template_name = template_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)

    def validate(self, context, topology):
        # TODO: check type?
        for interface in self.interfaces.itervalues():
            interface.validate(context, topology)

    def dump(self, context):
        if self.type_name is not None:
            puts('Relationship type: %s' % context.style.type(self.type_name))
        else:
            puts('Relationship template: %s' % context.style.node(self.template_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)

class Capability(object):
    def __init__(self, name, type_name):
        if not isinstance(name, basestring):
            raise ValueError('name must be string')
        if not isinstance(type_name, basestring):
            raise ValueError('type_name must be string')
        
        self.name = name
        self.type_name = type_name
        self.min_occurrences = None # optional
        self.max_occurrences = None # optional
        self.valid_source_node_type_names = None
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
        if topology.capability_types.get_descendant(self.type_name) is None:
            context.validation.report('capability "%s" has an unknown type: %s' % (self.name, repr(self.type)), level=Issue.BETWEEN_TYPES)        

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
            puts('Occurrences: %s (%s%s)' % (self.occurrences, self.min_occurrences or 0, (' to %d' % self.max_occurrences) if self.max_occurrences is not None else ' or more'))
            if self.valid_source_node_type_names:
                puts('Valid source node types: %s' % ', '.join((str(context.style.type(v)) for v in self.valid_source_node_type_names)))
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
        with context.style.indent:
            for interface in interfaces.itervalues():
                interface.dump(context)

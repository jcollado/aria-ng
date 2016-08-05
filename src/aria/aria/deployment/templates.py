
from .elements import Template, Interface, Requirement
from .utils import instantiate_properties, instantiate_interfaces, dump_properties, dump_interfaces
from .plan import DeploymentPlan, Node, Capability, Relationship, Group
from .. import Issue
from ..utils import StrictList, StrictDict
from clint.textui import puts
from types import FunctionType

class DeploymentTemplate(Template):
    def __init__(self):
        self.node_templates = StrictDict(str, NodeTemplate)
        self.group_templates = StrictDict(str, GroupTemplate)
        self.policies = StrictDict(str) # TODO

    def instantiate(self, context, container):
        r = DeploymentPlan()
        context.deployment.plan = r
        for node_template in self.node_templates.itervalues():
            node = node_template.instantiate(context, container)
            r.nodes[node.id] = node
        for group_template in self.group_templates.itervalues():
            group = group_template.instantiate(context, container)
            r.groups[group.name] = group
        return r

    def validate(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.validate(context)
        for group_template in self.group_templates.itervalues():
            group_template.validate(context)
        for policy in self.policies.itervalues():
            policy.validate(context)

    def dump(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.dump(context)
        for group_template in self.group_templates.itervalues():
            group_template.dump(context)
        for policy in self.policies.itervalues():
            policy.dump(context)

class NodeTemplate(Template):
    def __init__(self, name, type_name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if not isinstance(type_name, basestring):
            raise ValueError('must set type_name (string)')
        
        self.name = name
        self.type_name = type_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.capabilities = StrictDict(str, CapabilityTemplate)
        self.requirements = StrictList(Requirement)
        self.target_node_type_constraints = StrictList(FunctionType)
    
    def is_target_node_valid(self, target_node_template):
        if self.target_node_type_constraints:
            for node_type_constraint in self.target_node_type_constraints:
                if not node_type_constraint(target_node_template, self):
                    return False
        return True
    
    def instantiate(self, context, container):
        r = Node(self.name)
        instantiate_properties(context, self, r.properties, self.properties)
        instantiate_interfaces(context, self, r.interfaces, self.interfaces)
        for capability_name, capability in self.capabilities.iteritems():
            r.capabilities[capability_name] = capability.instantiate(context, self)
        return r
    
    def validate(self, context):
        if context.deployment.node_types.get_descendant(self.type_name) is None:
            context.validation.report('node template "%s" has an unknown type: %s' % (self.name, repr(self.type_name)), level=Issue.BETWEEN_TYPES)        
        for interface in self.interfaces.itervalues():
            interface.validate(context)
        for capability in self.capabilities.itervalues():
            capability.validate(context)
        for requirement in self.requirements:
            requirement.validate(context)
    
    def dump(self, context):
        puts('Node template: %s' % context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)
        with context.style.indent:
            if self.capabilities:
                puts('Capabilities:')
                with context.style.indent:
                    for capabilitiy in self.capabilities.itervalues():
                        capabilitiy.dump(context)
            if self.requirements:
                puts('Requirements:')
                with context.style.indent:
                    for requirement in self.requirements:
                        requirement.dump(context)

class CapabilityTemplate(Template):
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
        
    def satisfies_requirement(self, context, source_node_template, requirement, target_node_template):
        # Do we match the required capability type?
        if not context.deployment.capability_types.is_descendant(requirement.target_capability_type_name, self.type_name):
            return False
        
        # Are we in valid_source_node_type_names?
        if self.valid_source_node_type_names:
            for valid_source_node_type_name in self.valid_source_node_type_names:
                if not context.deployment.node_types.is_descendant(valid_source_node_type_name, source_node_template.type_name):
                    return False
        
        # Apply requirement constraints
        if requirement.target_node_type_constraints:
            for node_type_constraint in requirement.target_node_type_constraints:
                if not node_type_constraint(target_node_template, source_node_template):
                    return False
        
        return True

    def instantiate(self, context, container):
        r = Capability(self.name, self.type_name)
        r.min_occurrences = self.min_occurrences
        r.max_occurrences = self.max_occurrences
        instantiate_properties(context, container, r.properties, self.properties)
        return r

    def validate(self, context):
        if context.deployment.capability_types.get_descendant(self.type_name) is None:
            context.validation.report('capability "%s" has an unknown type: %s' % (self.name, repr(self.type)), level=Issue.BETWEEN_TYPES)        

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
            puts('Occurrences: %s%s' % (self.min_occurrences or 0, (' to %d' % self.max_occurrences) if self.max_occurrences is not None else ' or more'))
            if self.valid_source_node_type_names:
                puts('Valid source node types: %s' % ', '.join((str(context.style.type(v)) for v in self.valid_source_node_type_names)))
        dump_properties(context, self.properties)

class RelationshipTemplate(Template):
    def __init__(self, type_name=None, template_name=None):
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

    def instantiate(self, context, container):
        r = Relationship(self.type_name, self.template_name)
        instantiate_properties(context, container, r.properties, self.properties)
        instantiate_interfaces(context, container, r.interfaces, self.interfaces)
        return r

    def validate(self, context):
        for interface in self.interfaces.itervalues():
            interface.validate(context)

    def dump(self, context):
        if self.type_name is not None:
            puts('Relationship type: %s' % context.style.type(self.type_name))
        else:
            puts('Relationship template: %s' % context.style.node(self.template_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)

class GroupTemplate(Template):
    def __init__(self, name, type_name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if not isinstance(type_name, basestring):
            raise ValueError('must set type_name (string)')
        
        self.name = name
        self.type_name = type_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.member_node_template_names = StrictList(str)

    def instantiate(self, context, container):
        r = Group(self.name, self.type_name)
        instantiate_properties(context, self, r.properties, self.properties)
        instantiate_interfaces(context, self, r.interfaces, self.interfaces)
        for member_node_template_name in self.member_node_template_names:
            for node in context.deployment.plan.nodes.itervalues():
                if node.template_name == member_node_template_name:
                    r.member_node_ids.append(node.id)
        return r

    def dump(self, context):
        puts('Group template: %s' % context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)
        with context.style.indent:
            if self.member_node_template_names:
                puts('Member node templates: %s' % ', '.join((str(context.style.node(v)) for v in self.member_node_template_names)))

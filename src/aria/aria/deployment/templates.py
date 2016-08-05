
from .elements import Template, Interface, Requirement, Capability
from .utils import instantiate_properties, instantiate_interfaces, dump_properties, dump_interfaces
from .plan import DeploymentPlan, Node, Relationship
from .. import Issue
from ..utils import StrictList, StrictDict
from clint.textui import puts
from types import FunctionType

class DeploymentTemplate(Template):
    def __init__(self):
        self.node_templates = StrictDict(str, NodeTemplate)
        self.groups = StrictDict(str) # TODO
        self.policies = StrictDict(str) # TODO

    def instantiate(self, context):
        r = DeploymentPlan()
        for node_template in self.node_templates.itervalues():
            node = node_template.instantiate(context)
            r.nodes[node.id] = node
        return r

    def validate(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.validate(context)
        for group in self.groups.itervalues():
            group.validate(context)
        for policy in self.policies.itervalues():
            policy.validate(context)

    def dump(self, context):
        for node_template in self.node_templates.itervalues():
            node_template.dump(context)

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
        self.capabilities = StrictDict(str, Capability)
        self.requirements = StrictList(Requirement)
        self.target_node_type_constraints = StrictList(FunctionType)
    
    def is_target_node_valid(self, target_node_template):
        if self.target_node_type_constraints:
            for node_type_constraint in self.target_node_type_constraints:
                if not node_type_constraint(target_node_template):
                    return False
        return True
    
    def instantiate(self, context):
        r = Node(self.name)
        instantiate_properties(context, r.properties, self.properties)
        instantiate_interfaces(context, r.interfaces, self.interfaces)
        for capability_name, capability in self.capabilities.iteritems():
            r.capabilities[capability_name] = capability.instantiate(context)
        #for requirement in self.requirements:
        #    if requirement.relationship_template:
        #        r.relationships.append(requirement.relationship_template.instantiate(context))
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

class RelationshipTemplate(Template):
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

    def instantiate(self, context):
        r = Relationship(self.type_name, self.template_name)
        instantiate_properties(context, r.properties, self.properties)
        instantiate_interfaces(context, r.interfaces, self.interfaces)
        return r

    def validate(self, context):
        # TODO: check type?
        for interface in self.interfaces.itervalues():
            interface.validate(context)

    def dump(self, context):
        if self.type_name is not None:
            puts('Relationship type: %s' % context.style.type(self.type_name))
        else:
            puts('Relationship template: %s' % context.style.node(self.template_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)

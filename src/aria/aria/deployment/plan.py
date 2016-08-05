
from .elements import Element, Interface, Capability
from .ids import generate_id
from .utils import dump_properties, dump_interfaces
from .. import Issue
from ..utils import StrictList, StrictDict, ReadOnlyList
from clint.textui import puts, indent

class DeploymentPlan(object):
    def __init__(self):
        self.nodes = StrictDict(str, Node) 

    def satisfy_requirements(self, context):
        satisfied = True
        for node in self.nodes.itervalues():
            if not node.satisfy_requirements(context):
                satisfied = False
        return satisfied
    
    def find_nodes(self, target_node_template_name):
        nodes = []
        for node in self.nodes.itervalues():
            if node.template_name == target_node_template_name:
                nodes.append(node)
        return ReadOnlyList(nodes)
    
    def is_node_a_target(self, node_id):
        pass

    def _is_node_a_target(self, source_node, target_node):
        if source_node.relationships:
            for relationship in source_node.relationships:
            

    def dump(self, context):
        for node in self.nodes.itervalues():
            node.dump(context)

    def dump_graph(self, context):
        for node in self.nodes.itervalues():
            self._dump_graph_node(context, node)
        
    def _dump_graph_node(self, context, node):
        puts(context.style.node(node.id))
        if node.relationships:
            with context.style.indent:
                for relationship in node.relationships:
                    puts('-> %s %s' % (context.style.type(relationship.type_name), context.style.node(relationship.target_capability_name)))
                    target_node = self.nodes[relationship.target_node_id]
                    with indent(3):
                        self._dump_graph_node(context, target_node)

class Node(Element):
    def __init__(self, template_name):
        if not isinstance(template_name, basestring):
            raise ValueError('must set template_name (string)')

        self.id = '%s_%s' % (template_name, generate_id())
        self.template_name = template_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.capabilities = StrictDict(str, Capability)
        self.relationships = StrictList(Relationship)
    
    def satisfy_requirements(self, context):
        node_template = context.deployment.template.node_templates.get(self.template_name)
        satisfied = True
        for requirement in node_template.requirements:
            target_node_template, target_capability = requirement.find_target(context, node_template)
            if target_node_template is not None:
                #puts('%s.%s -> %s.%s' % (node_template.name, requirement.name, target_node_template.name, target_capability.name))
                target_nodes = context.deployment.plan.find_nodes(target_node_template.name)
                if target_nodes:
                    target_node = target_nodes[0]
                    target_capability = target_node.capabilities[target_capability.name]
                    
                    if requirement.relationship_template is not None:
                        relationship = requirement.relationship_template.instantiate(context)
                        relationship.target_node_id = target_node.id
                        relationship.target_capability_name = target_capability.name
                        self.relationships.append(relationship)
                else:
                    # TODO: no node for template?!
                    pass
                #return self.relate(context, target_node_template, target_capability)
                pass
            else:
                context.validation.report('requirement "%s" of node "%s" has no target node template' % (requirement.name, self.id), level=Issue.BETWEEN_TYPES)
                satisfied = False
        return satisfied
            
    def dump(self, context):
        puts('Node: %s' % context.style.node(self.id))
        with context.style.indent:
            puts('Template: %s' % context.style.node(self.template_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)
        with context.style.indent:
            if self.capabilities:
                puts('Capabilities:')
                with context.style.indent:
                    for capability in self.capabilities.itervalues():
                        capability.dump(context)
            if self.relationships:
                puts('Relationships:')
                with context.style.indent:
                    for relationship in self.relationships:
                        relationship.dump(context)

class Relationship(Element):
    def __init__(self, type_name=None, template_name=None):
        # TODO: do we really need type_name and/or template_name?
        if type_name and not isinstance(type_name, basestring):
            raise ValueError('type_name must be string')
        if template_name and not isinstance(template_name, basestring):
            raise ValueError('template_name must be string')
        if (type_name and template_name) or ((not type_name) and (not template_name)):
            raise ValueError('must set either type_name or template_name')
        
        self.target_node_id = None
        self.target_capability_name = None
        self.type_name = type_name
        self.template_name = template_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)

    def validate(self, context):
        # TODO: check type?
        for interface in self.interfaces.itervalues():
            interface.validate(context)

    def dump(self, context):
        puts('Target node: %s' % context.style.node(self.target_node_id))
        puts('Target capability: %s' % context.style.node(self.target_capability_name))
        if self.type_name is not None:
            puts('Relationship type: %s' % context.style.type(self.type_name))
        else:
            puts('Relationship template: %s' % context.style.node(self.template_name))
        dump_properties(context, self.properties)
        dump_interfaces(context, self.interfaces)

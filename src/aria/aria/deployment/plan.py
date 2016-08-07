
from .elements import Element, Interface, Artifact
from .ids import generate_id
from .utils import dump_list_values, dump_dict_values, dump_properties, dump_interfaces
from .. import Issue
from ..utils import StrictList, StrictDict, ReadOnlyList
from collections import OrderedDict
from clint.textui import puts, indent

class DeploymentPlan(Element):
    def __init__(self):
        self.nodes = StrictDict(str, Node) 
        self.groups = StrictDict(str, Group) 
        self.inputs = StrictDict(str)
        self.outputs = StrictDict(str)

    def satisfy_requirements(self, context):
        satisfied = True
        for node in self.nodes.itervalues():
            if not node.satisfy_requirements(context):
                satisfied = False
        return satisfied
    
    def validate_capabilities(self, context):
        satisfied = True
        for node in self.nodes.itervalues():
            if not node.validate_capabilities(context):
                satisfied = False
        return satisfied
    
    def find_nodes(self, target_node_template_name):
        nodes = []
        for node in self.nodes.itervalues():
            if node.template_name == target_node_template_name:
                nodes.append(node)
        return ReadOnlyList(nodes)
    
    def is_node_a_target(self, context, target_node):
        for node in self.nodes.itervalues():
            if self._is_node_a_target(context, node, target_node):
                return True
        return False

    def _is_node_a_target(self, context, source_node, target_node):
        if source_node.relationships:
            for relationship in source_node.relationships:
                if relationship.target_node_id == target_node.id:
                    return True
                else:
                    node = context.deployment.plan.nodes.get(relationship.target_node_id)
                    return self._is_node_a_target(context, node, target_node)
        return False
    
    def validate(self, context):
        for node in self.nodes.itervalues():
            node.validate(context)
        for group in self.groups.itervalues():
            group.validate(context)

    @property
    def as_raw(self):
        return OrderedDict((
            ('nodes', [v.as_raw for v in self.nodes.itervalues()]),
            ('groups', [v.as_raw for v in self.groups.itervalues()]),
            ('inputs', self.inputs),
            ('outputs', self.outputs)))

    def dump(self, context):
        for node in self.nodes.itervalues():
            node.dump(context)
        for group in self.groups.itervalues():
            group.dump(context)
        dump_properties(context, self.inputs, 'Inputs')
        dump_properties(context, self.outputs, 'Outputs')

    def dump_graph(self, context):
        for node in self.nodes.itervalues():
            if not self.is_node_a_target(context, node):
                self._dump_graph_node(context, node)
        
    def _dump_graph_node(self, context, node):
        puts(context.style.node(node.id))
        if node.relationships:
            with context.style.indent:
                for relationship in node.relationships:
                    puts('-> %s %s' % (context.style.type(relationship.type_name), context.style.node(relationship.target_capability_name)))
                    target_node = self.nodes.get(relationship.target_node_id)
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
        self.artifacts = StrictDict(str, Artifact)
        self.capabilities = StrictDict(str, Capability)
        self.relationships = StrictList(Relationship)
    
    def satisfy_requirements(self, context):
        node_template = context.deployment.template.node_templates.get(self.template_name)
        satisfied = True
        for requirement in node_template.requirements:
            # Find target template
            target_node_template, target_capability = requirement.find_target(context, node_template)
            if target_node_template is not None:
                # Find target nodes
                target_nodes = context.deployment.plan.find_nodes(target_node_template.name)
                if target_nodes:
                    related = False
                    for target_node in target_nodes:
                        # Relate to the first target node that has capacity
                        target_capability = target_node.capabilities.get(target_capability.name)
                        if target_capability.relate():
                            if requirement.relationship_template is not None:
                                relationship = requirement.relationship_template.instantiate(context, self)
                                relationship.target_node_id = target_node.id
                                relationship.target_capability_name = target_capability.name
                                self.relationships.append(relationship)
                            related = True
                            break
                    if not related:
                        context.validation.report('requirement "%s" of node "%s" targets node template "%s" but its instantiated nodes do not have enough capacity' % (requirement.name, self.id, target_node_template.name), level=Issue.BETWEEN_INSTANCES)
                        satisfied = False
                else:
                    context.validation.report('requirement "%s" of node "%s" targets node template "%s" but it has no instantiated nodes' % (requirement.name, self.id, target_node_template.name), level=Issue.BETWEEN_INSTANCES)
                    satisfied = False
            else:
                context.validation.report('requirement "%s" of node "%s" has no target node template' % (requirement.name, self.id), level=Issue.BETWEEN_INSTANCES)
                satisfied = False
        return satisfied

    def validate_capabilities(self, context):
        satisfied = False
        for capability in self.capabilities.itervalues():
            if not capability.has_enough_relationships:
                context.validation.report('capability "%s" of node "%s" requires at least %d relationships but has %d' % (capability.name, self.id, capability.min_occurrences, capability.occurrences), level=Issue.BETWEEN_INSTANCES)
                satisfied = False
        return satisfied

    def validate(self, context):
        for interface in self.interfaces.itervalues():
            interface.validate(context)
        for artifact in self.artifacts.itervalues():
            artifact.validate(context)
        for capability in self.capabilities.itervalues():
            capability.validate(context)
        for relationship in self.relationships:
            relationship.validate(context)

    @property
    def as_raw(self):
        return OrderedDict((
            ('id', self.id),
            ('template_name', self.template_name),
            ('properties', self.properties),
            ('interfaces', [v.as_raw for v in self.interfaces.itervalues()]),
            ('artifacts', [v.as_raw for v in self.artifacts.itervalues()]),
            ('capabilities', [v.as_raw for v in self.capabilities.itervalues()]),
            ('relationships', [v.as_raw for v in self.relationships])))
            
    def dump(self, context):
        puts('Node: %s' % context.style.node(self.id))
        with context.style.indent:
            puts('Template: %s' % context.style.node(self.template_name))
            dump_properties(context, self.properties)
            dump_interfaces(context, self.interfaces)
            dump_dict_values(context, self.artifacts, 'Artifacts')
            dump_dict_values(context, self.capabilities, 'Capabilities')
            dump_list_values(context, self.relationships, 'Relationships')

class Capability(Element):
    def __init__(self, name, type_name):
        if not isinstance(name, basestring):
            raise ValueError('name must be string')
        if not isinstance(type_name, basestring):
            raise ValueError('type_name must be string')
        
        self.name = name
        self.type_name = type_name
        self.min_occurrences = None # optional
        self.max_occurrences = None # optional
        self.properties = StrictDict(str)
        self.occurrences = 0
    
    @property
    def has_enough_relationships(self):
        if self.min_occurrences is not None:
            return self.occurrences >= self.min_occurrences
        return True

    def relate(self):
        if self.max_occurrences is not None:
            if self.occurrences == self.max_occurrences:
                return False
        self.occurrences += 1
        return True 

    @property
    def as_raw(self):
        return OrderedDict((
            ('name', self.name),
            ('type_name', self.type_name),
            ('properties', self.properties)))
            
    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
            puts('Occurrences: %s (%s%s)' % (self.occurrences, self.min_occurrences or 0, (' to %d' % self.max_occurrences) if self.max_occurrences is not None else ' or more'))
            dump_properties(context, self.properties)

class Relationship(Element):
    def __init__(self, type_name=None, template_name=None):
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
        for interface in self.interfaces.itervalues():
            interface.validate(context)

    @property
    def as_raw(self):
        return OrderedDict((
            ('target_node_id', self.target_node_id),
            ('target_capability_name', self.target_capability_name),
            ('type_name', self.type_name),
            ('properties', self.properties),
            ('interfaces', [v.as_raw for v in self.interfaces.itervalues()])))            

    def dump(self, context):
        puts('Target node: %s' % context.style.node(self.target_node_id))
        with context.style.indent:
            puts('Target capability: %s' % context.style.node(self.target_capability_name))
            if self.type_name is not None:
                puts('Relationship type: %s' % context.style.type(self.type_name))
            else:
                puts('Relationship template: %s' % context.style.node(self.template_name))
            dump_properties(context, self.properties)
            dump_interfaces(context, self.interfaces)

class Group(Element):
    def __init__(self, name, type_name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if not isinstance(type_name, basestring):
            raise ValueError('must set type_name (string)')
        
        self.name = name
        self.type_name = type_name
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.member_node_ids = StrictList(str)

    @property
    def as_raw(self):
        return OrderedDict((
            ('name', self.name),
            ('type_name', self.type_name),
            ('properties', self.properties),
            ('interfaces', [v.as_raw for v in self.interfaces.itervalues()]),
            ('member_node_ids', self.member_node_ids)))

    def dump(self, context):
        puts('Group: %s' % context.style.node(self.name))
        with context.style.indent:
            puts('Type: %s' % context.style.type(self.type_name))
            dump_properties(context, self.properties)
            dump_interfaces(context, self.interfaces)
            if self.member_node_ids:
                puts('Member nodes:')
                with context.style.indent:
                    for node_id in self.member_node_ids:
                        puts(context.style.node(node_id))

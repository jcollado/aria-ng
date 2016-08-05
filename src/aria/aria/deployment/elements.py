
from .utils import instantiate_properties, dump_properties
from .. import Issue, UnimplementedFunctionalityError, classname
from ..utils import StrictList, StrictDict
from clint.textui import puts
from types import FunctionType

class Element(object):
    def validate(self, context):
        pass

    def dump(self, context):
        pass

class Template(Element):
    def instantiate(self, context, container):
        pass

class Function(object):
    def evaluate(self, context, container):
        raise UnimplementedFunctionalityError(classname(self) + '.evaluate')

class Interface(Template):
    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
        self.name = name
        self.inputs = StrictDict(str)
        self.operations = StrictDict(str, Operation)

    def instantiate(self, context, container):
        r = Interface(self.name)
        instantiate_properties(context, container, r.inputs, self.inputs)
        for operation_name, operation in self.operations.iteritems():
            r.operations[operation_name] = operation.instantiate(context, container)
        return r
                
    def validate(self, context):
        for operation in self.operations.itervalues():
            operation.validate(context)

    def dump(self, context):
        puts(context.style.node(self.name))
        dump_properties(context, self.inputs, 'Inputs')
        with context.style.indent:
            if self.operations:
                puts('Operations:')
                with context.style.indent:
                    for operation in self.operations.itervalues():
                        operation.dump(context)

class Operation(Template):
    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
        self.name = name
        self.implementation = None
        self.dependencies = StrictList(str)
        self.inputs = StrictDict(str)

    def instantiate(self, context, container):
        r = Operation(self.name)
        r.implementation = self.implementation
        r.dependencies = self.dependencies
        instantiate_properties(context, container, r.inputs, self.inputs)
        return r

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.implementation is not None:
                puts('Implementation: %s' % context.style.literal(self.implementation))
            if self.dependencies:
                puts('Dependencies: %s' % ', '.join((str(context.style.literal(v)) for v in self.dependencies)))
        dump_properties(context, self.inputs, 'Inputs')

class Requirement(Element):
    def __init__(self, name, target_node_type_name=None, target_node_template_name=None, target_capability_type_name=None, target_capability_name=None):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if target_node_type_name and not isinstance(target_node_type_name, basestring):
            raise ValueError('target_node_type_name must be string')
        if target_node_template_name and not isinstance(target_node_template_name, basestring):
            raise ValueError('target_node_template_name must be string')
        if target_capability_type_name and not isinstance(target_capability_type_name, basestring):
            raise ValueError('target_capability_type_name must be string')
        if target_capability_name and not isinstance(target_capability_name, basestring):
            raise ValueError('target_capability_name must be string')
        if (target_node_type_name and target_node_template_name) or ((not target_node_type_name) and (not target_node_template_name)):
            raise ValueError('must set either target_node_type_name or target_node_template_name')
        if target_capability_type_name and target_capability_name:
            raise ValueError('can set either target_capability_type_name or target_capability_name')
        
        self.name = name
        self.target_node_type_name = target_node_type_name
        self.target_node_template_name = target_node_template_name
        self.target_node_type_constraints = StrictList(FunctionType)
        self.target_capability_type_name = target_capability_type_name
        self.target_capability_name = target_capability_name
        self.relationship_template = None # optional

    def find_target(self, context, source_node_template):
        # We might already have a specific node template, so we'll just verify it
        if self.target_node_template_name:
            target_node_template = context.deployment.template.node_templates.get(self.target_node_template_name)
            
            if not source_node_template.is_target_node_valid(target_node_template):
                context.validation.report('requirement "%s" of node template "%s" is for node template "%s" but it does not match constraints' % (self.name, self.target_node_template_name, source_node_template.name), level=Issue.BETWEEN_TYPES)
                return None, None
            
            target_capability = self.find_target_capability(context, source_node_template, target_node_template)
            if target_capability is None:
                return None, None
            
            return target_node_template, target_capability

        # Find first node that matches the type
        elif self.target_node_type_name is not None:
            for target_node_template in context.deployment.template.node_templates.itervalues():
                if not context.deployment.node_types.is_descendant(self.target_node_type_name, target_node_template.type_name):
                    continue
                
                if not source_node_template.is_target_node_valid(target_node_template):
                    continue
    
                target_capability = self.find_target_capability(context, source_node_template, target_node_template)
                if target_capability is None:
                    continue
                
                return target_node_template, target_capability
        
        return None, None

    def find_target_capability(self, context, source_node_template, target_node_template):
        for capability in target_node_template.capabilities.itervalues():
            if capability.satisfies_requirement(context, source_node_template, self, target_node_template):
                return capability
        return None

    def validate(self, context):
        if (self.target_node_type_name) and (context.deployment.node_types.get_descendant(self.target_node_type_name) is None):
            context.validation.report('requirement "%s" refers to an unknown node type: %s' % (self.name, repr(self.target_node_type_name)), level=Issue.BETWEEN_TYPES)        
        if (self.target_capability_type_name) and (context.deployment.capability_types.get_descendant(self.target_capability_type_name) is None):
            context.validation.report('requirement "%s" refers to an unknown capability type: %s' % (self.name, repr(self.target_capability_type_name)), level=Issue.BETWEEN_TYPES)        
        if self.relationship_template:
            self.relationship_template.validate(context)

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.target_node_type_name is not None:
                puts('Target node type: %s' % context.style.type(self.target_node_type_name))
            elif self.target_node_template_name is not None:
                puts('Target node template: %s' % context.style.node(self.target_node_template_name))
            if self.target_capability_type_name is not None:
                puts('Target capability type: %s' % context.style.type(self.target_capability_type_name))
            elif self.target_capability_name is not None:
                puts('Target capability name: %s' % context.style.node(self.target_capability_name))
            if self.relationship_template:
                self.relationship_template.dump(context)

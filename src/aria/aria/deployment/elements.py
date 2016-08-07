
from .utils import instantiate_properties, dump_properties
from .. import UnimplementedFunctionalityError, classname
from ..utils import StrictList, StrictDict
from collections import OrderedDict
from clint.textui import puts

class Element(object):
    def validate(self, context):
        pass
    
    @property
    def as_raw(self):
        raise UnimplementedFunctionalityError(classname(self) + '.as_raw')

    def dump(self, context):
        pass

class Template(Element):
    def instantiate(self, context, container):
        pass

class Function(object):
    def _evaluate(self, context, container):
        raise UnimplementedFunctionalityError(classname(self) + '._evaluate')

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
    
    @property
    def as_raw(self):
        return OrderedDict((
            ('name', self.name),
            ('inputs', self.inputs),
            ('operations', {k: v.as_raw for k, v in self.operations.iteritems()})))

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            dump_properties(context, self.inputs, 'Inputs')
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

    @property
    def as_raw(self):
        return OrderedDict((
            ('name', self.name),
            ('implementation', self.implementation),
            ('dependencies', self.dependencies),
            ('inputs', self.inputs)))

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            if self.implementation is not None:
                puts('Implementation: %s' % context.style.literal(self.implementation))
            if self.dependencies:
                puts('Dependencies: %s' % ', '.join((str(context.style.literal(v)) for v in self.dependencies)))
            dump_properties(context, self.inputs, 'Inputs')

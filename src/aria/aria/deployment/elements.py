
from .utils import instantiate_properties, dump_dict_values, dump_properties
from .. import UnimplementedFunctionalityError, classname
from ..utils import StrictList, StrictDict, make_agnostic
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
            ('operations', [v.as_raw for v in self.operations.itervalues()])))

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            dump_properties(context, self.inputs, 'Inputs')
            dump_dict_values(context, self.operations, 'Operations')

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

class Artifact(Template):
    def __init__(self, name, type_name, source_path):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        if not isinstance(type_name, basestring):
            raise ValueError('must set type_name (string)')
        if not isinstance(source_path, basestring):
            raise ValueError('must set source_path (string)')
        
        self.name = name
        self.type_name = type_name
        self.source_path = source_path
        self.target_path = None
        self.repository_url = None
        self.repository_credential = StrictDict(str, str)
        self.properties = StrictDict(str)

    def instantiate(self, context, container):
        r = Artifact(self.name, self.type_name, self.source_path)
        r.target_path = self.target_path
        r.repository_url = self.repository_url
        r.repository_credential = self.repository_credential
        instantiate_properties(context, self, r.properties, self.properties)
        return r

    @property
    def as_raw(self):
        return OrderedDict((
            ('name', self.name),
            ('type_name', self.type_name),
            ('source_path', self.source_path),
            ('target_path', self.target_path),
            ('repository_url', self.repository_url),
            ('repository_credential', make_agnostic(self.repository_credential)),
            ('properties', self.properties)))

    def dump(self, context):
        puts(context.style.node(self.name))
        with context.style.indent:
            puts('Artifact type: %s' % context.style.type(self.type_name))
            puts('Source path: %s' % context.style.literal(self.source_path))
            if self.target_path is not None:
                puts('Target path: %s' % context.style.literal(self.target_path))
            if self.repository_url is not None:
                puts('Repository URL: %s' % context.style.literal(self.repository_url))
            if self.repository_credential:
                puts('Repository credential: %s' % context.style.literal(self.repository_credential))
            dump_properties(context, self.properties)

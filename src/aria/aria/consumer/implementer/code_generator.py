
from ... import make_agnostic
from .writer import Writer, create_header, one_line, repr_assignment
from collections import OrderedDict
import os

class CodeModule(object):
    def __init__(self, generator, name='', parent=None):
        self.generator = generator
        self.name = name
        self.parent = parent
        self.children = {}
        self.classes = OrderedDict()
    
    def get_module(self, name, create=True):
        if name is None:
            return self
            
        if '.' in name:
            name, remainder = name.split('.', 1)
            m = self.get_module(name)
            return m.get_module(remainder)
        
        for n, m in self.children.iteritems():
            if n == name:
                return m
        
        if create:
            m = CodeModule(self.generator, name, self)
            self.children[name] = m
            return m
        
        return None
    
    def get_class(self, name, create=True):
        if name in self.classes:
            return self.classes[name]
        if create:
            c = CodeClass(self.generator, name, module=self)
            self.classes[name] = c
            return c
        return None
    
    def find_class(self, name, create=True):
        module = None
        if '.' in name:
            module, name = name.rsplit('.', 1)
        module = self.get_module(module, create)
        return module.get_class(name, create) if module else None
    
    def sort_classes(self):
        class Wrapper(object):
            def __init__(self, cls):
                self.cls = cls
            def __cmp__(self, o):
                if (self.cls.module == o.cls.module):
                    if (self.cls.base == o.cls):
                        return 1
                    elif (o.cls.base == self.cls):
                        return -1
                return 0
                
        def key((_, c)):
            return Wrapper(c)
        
        items = self.classes.items()
        items.sort(key=key)
        self.classes = OrderedDict(items)

    @property
    def all_modules(self):
        yield self
        for m in self.children.itervalues():
            for m in m.all_modules:
                yield m

    @property
    def all_classes(self):
        for c in self.classes.itervalues():
            yield c
        for m in self.children.itervalues():
            for c in m.all_classes:
                yield c

    @property
    def fullname(self):
        n = self.parent.fullname if self.parent else ''
        return '%s.%s' % (n, self.name) if n else self.name
    
    @property
    def path(self):
        p = self.parent.path if self.parent else ''
        return os.path.join(p, self.name) if p else self.name
    
    @property
    def file(self):
        f = self.parent.path if self.parent else ''
        if self.children:
            if self.name:
                f = os.path.join(f, self.name)
            f = os.path.join(f, '__init__.py')
        else:
            f = os.path.join(f, self.name + '.py')
        return f
    
    def __str__(self):
        self.sort_classes()
        with Writer() as w:
            w.write(create_header())
            imports = set()
            for c in self.classes.itervalues():
                if (c.base != 'object') and (c.base.module != self):
                    imports.add(c.base.module.fullname)
                for p in c.properties.itervalues():
                    if p.type:
                        cc = self.generator.get_class(p.type, False)
                        if cc:
                            if cc.module != self:
                                imports.add(cc.module.fullname)
            for i in imports:
                w.write('import %s' % i)
            w.write()
            for c in self.classes.itervalues():
                w.write(str(c))
            if self.children:
                all = [m.name for m in self.children.itervalues()]
                all += [c.name for c in self.classes.itervalues()]
                w.write('__all__ = %s' % repr(all))
            return str(w)

class CodeClass(object):
    def __init__(self, generator, name, module=None, base='object', description=None):
        self.generator = generator
        self.name = name
        self.module = module
        self.base = base
        self.description = description
        self.properties = OrderedDict()
        self.methods = OrderedDict()
    
    @property
    def fullname(self):
        return '%s.%s' % (self.module.fullname, self.name)
    
    def make_names_unique(self):
        names = []
        def unique_name(name):
            if name not in names:
                names.append(name)
                return name
            else:
                return unique_name(name + '_')
        
        for m in self.methods.itervalues():
            m.name = unique_name(m.name)
    
    def __str__(self):
        self.make_names_unique()

        with Writer() as w:
            w.write('@has_validated_properties')
            w.write('@has_interfaces')
            base = self.base if isinstance(self.base, str) else (self.base.name if self.base.module == self.module else self.base.fullname)
            w.write('class %s(%s):' % (self.name, base))
            w.i()
            if self.description:
                w.write_docstring(self.description)
            w.write('def __init__(self, context):')
            w.i()
            w.write('self.context = context')
            w.o()
            for n, p in self.properties.iteritems():
                w.write()
                if p.default is not None:
                    w.write('@property_default(%s)' % repr(make_agnostic(p.default)))
                if p.type:
                    w.write('@property_type(%s)' % self.generator.get_classname(p.type))
                w.write('@validated_property')
                w.write('def %s():' % n)
                w.i()
                if p.description or p.type is not None:
                    w.write('"""')
                    if p.description:
                        w.write(p.description.strip())
                    if p.type is not None:
                        if p.description:
                            w.write()
                        w.write(':rtype: :class:`%s`' % self.generator.get_classname(p.type))
                    w.write('"""')
                else:
                    w.write('pass')
                w.o()
            for n, m in self.methods.iteritems():
                w.write()
                w.write(m)
            return str(w)

class CodeProperty(object):
    def __init__(self, generator, name, description=None, type=None, default=None):
        self.generator = generator
        self.name = name
        self.description = description
        self.type = type
        self.default = default

    @property
    def docstring(self):
        with Writer() as w:
            w.put(':param')
            if self.type:
                w.put(' %s' % self.type)
            w.put(' %s: %s' % (self.name, one_line(self.description or self.name)))
            return str(w)
    
    @property
    def signature(self):
        with Writer() as w:
            w.put('%s=%s' % (self.name, repr(make_agnostic(self.default))))
            #if self.default is not None:
            #    w.put('=%s' % repr(make_agnostic(self.default)))
            return str(w)

class CodeAssignment(object):
    def __init__(self, generator, name, description, value):
        self.generator = generator
        self.name = name
        self.description = description
        self.value = value

class CodeMethod(object):
    def __init__(self, generator, name, interface, description, implementation, executor):
        self.generator = generator
        self.name = name
        self.interface = interface
        self.description = description
        self.implementation = implementation
        self.executor = executor
        self.arguments = OrderedDict()
    
    def __str__(self):
        with Writer() as w:
            if self.interface:
                w.write('@interfacemethod(%s)' % repr(self.interface))
            w.put('def %s(self' % self.name)
            if self.arguments:
                for a in self.arguments.itervalues():
                    w.put(', %s' % a.signature)
            w.put('):\n')
            w.i()
            if self.description or self.arguments:
                w.write('"""')
                if self.description:
                    self.write(description.strip())
                if self.arguments:
                    if self.description:
                        self.write()
                    for n, a in self.arguments.iteritems():
                        w.write(a.docstring)
                w.write('"""')
            w.put_indent()
            if self.implementation:
                if self.executor:
                    w.put('self.context.executor(%s).' % repr(self.executor))
                else:
                    w.put('self.context.executor().')
                if '/' in self.implementation:
                    w.put('selc.context.executor().execute(self, %s' % repr(self.implementation))
                else:
                    w.put('%s(self' % self.implementation)
                if self.arguments:
                    for n in self.arguments:
                        w.put(', %s' % n)
                w.put(')')
            else:
                w.put('pass')
            return str(w)

class CodeNodeTemplate(object):
    def __init__(self, generator, name, type, description):
        self.generator = generator
        self.name = name
        self.type = type
        self.description = description
        self.assignments = OrderedDict()
        self.relationships = []
        
    def relate(self, w):
        if self.relationships:
            for r in self.relationships:
                w.write('context.relate(self.%s, %s(context), self.%s)' % (self.name, self.generator.get_classname(r.type), r.target))
    
    def __str__(self):
        with Writer() as w:
            if self.description:
                w.write('%s' % self.description.strip(), prefix='# ')
            w.write('self.%s = %s(context)' % (self.name, self.generator.get_classname(self.type)))
            if self.assignments:
                for k, v in self.assignments.iteritems():
                    w.write('self.%s.%s = %s' % (self.name, k, repr_assignment(v)))
            return str(w)

class CodeRelationship(object):
    def __init__(self, generator, type, target):
        self.generator = generator
        self.type = type
        self.target = target

class CodeGenerator(object):
    def __init__(self):
        self.description = None
        self.module = CodeModule(self)
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.nodes = OrderedDict()
        self.workflows = OrderedDict()
        self.translate_classes = {
            'string': 'str',
            'integer': 'int',
            'boolean': 'bool'}
        self.common_module_name = 'common'
    
    def get_class(self, name, create=True):
        return self.module.find_class(name, create)

    def get_classname(self, name):
        if name in self.translate_classes:
            r = self.translate_classes[name]
            return r if isinstance(r, str) else r.fullname
        return name

    def link_classes(self):
        for c in self.module.all_classes:
            if isinstance(c.base, str):
                b = self.get_class(c.base, False)
                if b:
                    c.base = b
        for c in self.module.all_classes:
            if not c.module.name:
                del c.module.classes[c.name]
                root = self.module.get_module(self.common_module_name)
                c.module = root
                root.classes[c.name] = c
                self.translate_classes[c.name] = c
    
    def write_file(self, file, content):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as e:
            if e.errno != 17:
                raise e
        with open(file, 'w') as f:
            f.write(str(content))
    
    def write(self, root):
        self.link_classes()
        for m in self.module.all_modules:
            if m.name:
                file = os.path.join(root, m.file)
                self.write_file(file, m)
        file = os.path.join(root, 'service.py')
        self.write_file(file, self.service)

    @property
    def service(self):
        with Writer() as w:
            w.write(create_header())
            for m in self.module.all_modules:
                if m.fullname:
                    w.write('import %s' % m.fullname)
            w.write()
            w.write('class Service(object):')
            w.i()
            if self.description or self.inputs:
                w.write('"""')
                if self.description:
                    w.write(self.description.strip())
                if self.inputs:
                    if self.description:
                        w.write()
                    for i in self.inputs.itervalues():
                        w.write(i.docstring)
                w.write('"""')
            if self.inputs or self.outputs or self.nodes or self.workflows:
                w.write()
                if self.inputs:
                    w.write('INPUTS = %s' % repr(tuple(self.inputs.keys())))
                if self.outputs:
                    w.write('OUTPUTS = %s' % repr(tuple(self.outputs.keys())))
                if self.nodes:
                    w.write('NODES = %s' % repr(tuple(self.nodes.keys())))
                if self.workflows:
                    w.write('WORKFLOWS = %s' % repr(tuple(self.workflows.keys())))
                w.write()
            w.put_indent()
            w.put('def __init__(self, context')
            if self.inputs:
                for i in self.inputs.itervalues():
                    w.put(', %s' % i.signature)
            w.put('):\n')
            w.i()
            w.write('self.context = context')
            w.write('self.context.service = self')
            if self.inputs:
                w.write()
                w.write('# Inputs')
                for i in self.inputs:
                    w.write('self.%s = %s' % (i, i))
            if self.nodes:
                w.write()
                for n in self.nodes.itervalues():
                    w.write(n.description or 'Node: %s' % n.name, prefix='# ')
                    w.write(n)
                has_relationships = False
                for n in self.nodes.itervalues():
                    if n.relationships:
                        has_relationships = True
                        break
                if has_relationships:
                    w.write('# Relationships')
                    for n in self.nodes.itervalues():
                        n.relate(w)
            w.o()
            if self.outputs:
                w.write()
                w.write('# Outputs')
                for o in self.outputs.itervalues():
                    w.write()
                    w.write('@property')
                    w.write('def %s(self):' % o.name)
                    w.i()
                    if o.description:
                        w.write_docstring(o.description)
                    w.write('return %s' % repr_assignment(o.value))
                    w.o()
            if self.workflows:
                w.write()
                w.write('# Workflows')
                for workflow in self.workflows.itervalues():
                    w.write()
                    w.write(str(workflow))
            return str(w)

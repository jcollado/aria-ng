
from aria import make_agnostic
from consumer import Consumer
from cStringIO import StringIO
from collections import OrderedDict
from clint.textui import puts, colored, indent
import json, os, os.path, sys

class Writer(object):
    def __init__(self):
        self.indent = 0
    
    def write(self, s=None):
        if s:
            for s in s.split('\n'):
                if self.indent:
                    for i in range(self.indent):
                        self.io.write('    ')
                self.io.write(s)
                self.io.write('\n')
        else:
            self.io.write('\n')
    
    def write_docstring(self, s):
        self.write('"""')
        self.write(s)
        self.write('"""')
    
    def i(self):
        self.indent += 1
    
    def o(self):
        self.indent -= 1
    
    def __enter__(self):
        self.io = StringIO()
        return self
        
    def __exit__(self, type, value, traceback):
        self.io.close()
        
    def __str__(self):
        return self.io.getvalue()

class CodeModule(object):
    def __init__(self, name='', parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.classes = OrderedDict()
    
    def get_module(self, name, create=True):
        if not name:
            return self
        
        elif '.' in name:
            name, remainder = name.split('.', 1)
            m = self.get_module(name)
            return m.get_module(remainder)
        
        for n, m in self.children.iteritems():
            if n == name:
                return m
        
        if create:
            m = CodeModule(name, self)
            self.children[name] = m
            return m
        
        return None
    
    def get_class(self, name, create=True):
        if name in self.classes:
            return self.classes[name]
        if create:
            c = CodeClass(name, module=self)
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
        for c in self.classes.itervalues():
            if c.base:
                no_base = False
                for cc in self.classes.itervalues():
                    if cc == c:
                        no_base = True
                        break
                    elif cc.name == c.base:
                        pass

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
            w.write('from aria import has_validated_properties, validated_property, property_type, property_default, property_status, required_property')
            imports = set()
            for c in self.classes.itervalues():
                if (c.base != 'object') and (c.base.module != self):
                    imports.add(c.base.module.fullname)
            for i in imports:
                w.write('import %s' % i)
            w.write()
            for c in self.classes.itervalues():
                w.write(str(c))
            return str(w)

class CodeClass(object):
    def __init__(self, name, module=None, base='object', description=None):
        self.name = name
        self.module = module
        self.base = base
        self.description = description
        self.properties = OrderedDict()
    
    @property
    def fullname(self):
        return '%s.%s' % (self.module.fullname, self.name)
    
    def __str__(self):
        with Writer() as w:
            w.write('@has_validated_properties')
            base = self.base if isinstance(self.base, str) else (self.base.name if self.base.module == self.module else self.base.fullname)
            w.write('class %s(%s):' % (self.name, base))
            w.i()
            if self.description:
                w.write_docstring(self.description)
            w.write('def __init__(self):')
            w.i()
            w.write('pass')
            w.o()
            for n, p in self.properties.iteritems():
                w.write()
                if p.default is not None:
                    w.write('@property_default(%s)' % repr(make_agnostic(p.default)))
                if p.type is not None:
                    w.write('#@property_type(%s)' % p.type)
                w.write('@validated_property')
                w.write('def %s(self):' % n)
                w.i()
                if p.description:
                    w.write_docstring(p.description)
                else:
                    w.write('pass')
                w.o()
            return str(w)

class CodeProperty(object):
    def __init__(self, name, description=None, type=None, default=None):
        self.name = name
        self.description = description
        self.type = type
        self.default = default

class CodeGenerator(object):
    def __init__(self):
        self.module = CodeModule()
    
    def get_class(self, name, create=True):
        return self.module.find_class(name, create)

    def link_classes(self):
        for c in self.module.all_classes:
            if isinstance(c.base, str):
                b = self.get_class(c.base, False)
                if b:
                    c.base = b
    
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
            file = os.path.join(root, m.file)
            self.write_file(file, m)
        file = os.path.join(root, 'profile.py')
        self.write_file(file, self.profile)

    @property
    def profile(self):
        with Writer() as w:
            for m in self.module.all_modules:
                if m.fullname:
                    w.write('import %s' % m.fullname)
            return str(w)

class Implementer(Consumer):
    """
    ARIA implementer.
    
    Creates Python classes for the presentation.
    """

    def __init__(self, presentation, root='out'):
        super(Implementer, self).__init__(presentation)
        self.root = root

    def consume(self):
        self.generate()

        sys.path.append(self.root)
        from nodecellar.nodes import MongoDatabase

    def generate(self):
        profile = self.presentation.profile
        
        generator = CodeGenerator()

        if profile.node_types:
            for name, node_type in profile.node_types.iteritems():
                cls = generator.get_class(name)
                if node_type.derived_from:
                    cls.base = node_type.derived_from
                if node_type.description:
                    cls.description = node_type.description
                if node_type.properties:
                    for name, p in node_type.properties.iteritems():
                        cls.properties[name] = CodeProperty(name, p.description, p.type, p.default)
        
        generator.write(self.root)
        
        return generator

    def dump(self):
        generator = self.implement()
        for m in generator.module.modules:
            if m.name:
                puts(colored.red(m.file))
            with indent(2):
                for c in m.classes.itervalues():
                    puts(str(c))

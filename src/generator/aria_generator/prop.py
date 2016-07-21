
from .writer import Writer, one_line
from aria import make_agnostic

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

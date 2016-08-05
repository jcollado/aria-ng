
from ..utils import StrictList
from clint.textui import puts

class Type(object):
    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
        self.name = name
        self.children = StrictList(Type)
    
    def get_descendant(self, name):
        if self.name == name:
            return self
        for child in self.children:
            found = child.get_descendant(name)
            if found is not None:
                return found
        return None
    
    def is_descendant(self, base_name, name):
        base = self.get_descendant(base_name)
        if base is not None:
            if base.get_descendant(name) is not None:
                return True
        return False
    
    def dump(self, context):
        if self.name:
            puts(context.style.type(self.name))
        with context.style.indent:
            for child in self.children:
                child.dump(context)

class TypeHierarchy(Type):
    def __init__(self):
        self.name = None
        self.children = StrictList(Type)

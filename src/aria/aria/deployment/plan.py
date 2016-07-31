
from ..utils import StrictList, StrictDict

class Plan(object):
    def __init__(self):
        self.nodes = StrictDict(str, Node) 

class Node(object):
    def __init__(self, id, template_name):
        if not isinstance(id, basestring):
            raise ValueError('must set id (string)')
        if not isinstance(template_name, basestring):
            raise ValueError('must set template_name (string)')
        
        self.id = id
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.relationships = StrictList(Relationship)
        self.template = template_name

class Interface(object):
    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
        self.name = name
        self.implementation = None
        self.dependencies = StrictList(str)
        self.inputs = StrictDict(str)

class Operation(object):
    def __init__(self, name):
        if not isinstance(name, basestring):
            raise ValueError('must set name (string)')
        
        self.name = name
        self.implementation = None
        self.dependencies = StrictList(str)
        self.inputs = StrictDict(str)

class Relationship(object):
    def __init__(self, target_node):
        if not isinstance(target_node, Node):
            raise ValueError('must set target_node (Node)')
        
        self.target_node = target_node
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)

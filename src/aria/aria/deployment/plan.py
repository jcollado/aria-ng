
from .ids import generate_id
from ..utils import StrictList, StrictDict

class Plan(object):
    def __init__(self):
        self.nodes = StrictDict(str, Node) 

    def dump(self, context):
        pass

class Node(object):
    def __init__(self, node_template):
        node_id = generate_id()
        node_id = '%s_%s' % (node_template.name, node_id)
        
        self.id = node_id
        self.properties = StrictDict(str)
        self.interfaces = StrictDict(str, Interface)
        self.relationships = StrictList(Relationship)
        self.template = node_template

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

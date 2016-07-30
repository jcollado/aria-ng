
from ..utils import StrictList, StrictDict

class Plan(object):
    def __init__(self):
        self.nodes = StrictDict(str, Node) 

class Node(object):
    def __init__(self, id, template):
        self.id = id
        self.template = template

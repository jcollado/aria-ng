
from .hierarchy import TypeHierarchy
from clint.textui import puts

class DeploymentContext(object):
    def __init__(self):
        self.template = None
        self.plan = None
        self.node_types = TypeHierarchy()
        self.capability_types = TypeHierarchy()

    def dump_types(self, context):
        if self.node_types:
            puts('Node types:')
            self.node_types.dump(context)
        if self.capability_types:
            puts('Capability types:')
            self.capability_types.dump(context)

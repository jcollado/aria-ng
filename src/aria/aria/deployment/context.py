
from ..utils import JSONValueEncoder, prune
from .hierarchy import TypeHierarchy
from clint.textui import puts
import json

class DeploymentContext(object):
    def __init__(self):
        self.template = None
        self.plan = None
        self.node_types = TypeHierarchy()
        self.capability_types = TypeHierarchy()

    @property
    def plan_as_raw(self):
        raw = self.plan.as_raw
        prune(raw)
        return raw

    def get_plan_as_json(self, indent=None):
        raw = self.plan_as_raw
        return json.dumps(raw, indent=indent, cls=JSONValueEncoder)

    def dump_types(self, context):
        if self.node_types:
            puts('Node types:')
            self.node_types.dump(context)
        if self.capability_types:
            puts('Capability types:')
            self.capability_types.dump(context)

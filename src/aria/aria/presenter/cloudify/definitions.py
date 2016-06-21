
from ... import has_fields
from ..tosca import InterfaceDefinition as BaseInterfaceDefinition
from .misc import Workflow

@has_fields
class InterfaceDefinition(BaseInterfaceDefinition):
    @property
    def workflows(self):
        """
        :rtype: dict of str, :class:`Workflow`
        """
        return {k: Workflow(v) for k, v in self.raw.iteritems()}

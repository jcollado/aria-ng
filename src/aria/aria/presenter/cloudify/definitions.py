
from misc import Workflow
from aria import has_fields
from aria.presenter.tosca_simple import InterfaceDefinition as BaseInterfaceDefinition

@has_fields
class InterfaceDefinition(BaseInterfaceDefinition):
    @property
    def workflows(self):
        """
        :rtype: dict of str, :class:`PropertyAssignment`
        """
        return {k: Workflow(v) for k, v in self.raw.iteritems()}

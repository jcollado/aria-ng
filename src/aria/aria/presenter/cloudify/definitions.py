
from misc import Workflow
from aria.presenter import has_properties
from aria.presenter.tosca_simple import InterfaceDefinition as BaseInterfaceDefinition

@has_properties
class InterfaceDefinition(BaseInterfaceDefinition):
    @property
    def workflows(self):
        """
        :class:`PropertyAssignment`
        """
        return {k: Workflow(v) for k, v in self.raw.iteritems()}

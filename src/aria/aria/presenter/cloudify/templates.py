
from misc import Relationship
from aria.presenter import has_properties, property_object_list
from aria.presenter.tosca_simple import NodeTemplate as BaseNodeTemplate

@has_properties
class NodeTemplate(BaseNodeTemplate):
    @property_object_list(Relationship)
    def relationships(self):
        """
        :class:`Relationship`
        """

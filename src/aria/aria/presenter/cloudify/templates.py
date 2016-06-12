
from misc import Relationship
from aria import has_fields, object_list_field
from aria.presenter.tosca_simple import NodeTemplate as BaseNodeTemplate

@has_fields
class NodeTemplate(BaseNodeTemplate):
    @object_list_field(Relationship)
    def relationships(self):
        """
        :rtype: list of :class:`Relationship`
        """

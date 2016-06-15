
from ... import has_fields, object_list_field
from ..tosca import NodeTemplate as BaseNodeTemplate
from .misc import Relationship

@has_fields
class NodeTemplate(BaseNodeTemplate):
    @object_list_field(Relationship)
    def relationships():
        """
        :rtype: list of :class:`Relationship`
        """

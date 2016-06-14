
from definitions import InterfaceDefinition
from aria import has_fields, object_dict_field
from aria.presenter.tosca_simple import NodeType as BaseNodeType, RelationshipType as BaseRelationshipType

@has_fields
class NodeType(BaseNodeType):
    @object_dict_field(InterfaceDefinition)
    def interfaces():
        """
        :class:`InterfaceDefinition`
        """

@has_fields
class RelationshipType(BaseRelationshipType):
    @object_dict_field(InterfaceDefinition)
    def target_interfaces():
        """
        :rtype: dict of str, :class:`InterfaceDefinition`
        """

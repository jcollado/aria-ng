
from definitions import InterfaceDefinition
from aria.presenter import has_properties, property_object_dict
from aria.presenter.tosca_simple import NodeType as BaseNodeType, RelationshipType as BaseRelationshipType

@has_properties
class NodeType(BaseNodeType):
    @property_object_dict(InterfaceDefinition)
    def interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

@has_properties
class RelationshipType(BaseRelationshipType):
    @property_object_dict(InterfaceDefinition)
    def target_interfaces(self):
        """
        :class:`InterfaceDefinition`
        """

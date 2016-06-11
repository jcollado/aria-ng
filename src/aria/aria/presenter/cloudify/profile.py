
from misc import Input, Output
from types import NodeType, RelationshipType
from templates import NodeTemplate
from aria.presenter import has_properties, property_object_dict
from aria.presenter.tosca_simple import Profile as BaseProfile

@has_properties
class Profile(BaseProfile):
    @property_object_dict(Input)
    def inputs(self):
        """
        :class:`Input`
        """

    @property_object_dict(Output)
    def outputs(self):
        """
        :class:`Output`
        """
    
    @property_object_dict(NodeType)
    def node_types(self):
        """
        :class:`NodeType`
        """

    @property_object_dict(RelationshipType)
    def relationships(self):
        """
        :class:`RelationshipType`
        """
        return self._get_object_dict('relationships', RelationshipType)
    
    @property_object_dict(NodeTemplate)
    def node_templates(self):
        """
        :class:`NodeTemplate`
        """

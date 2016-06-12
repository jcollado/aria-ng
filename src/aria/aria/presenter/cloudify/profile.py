
from misc import Output
from types import NodeType, RelationshipType
from templates import NodeTemplate
from aria import has_fields, object_dict_field
from aria.presenter.tosca_simple import Profile as BaseProfile, PropertyDefinition

@has_fields
class Profile(BaseProfile):
    @object_dict_field(PropertyDefinition)
    def inputs(self):
        """
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(Output)
    def outputs(self):
        """
        :rtype: dict of str, :class:`Output`
        """
    
    @object_dict_field(NodeType)
    def node_types(self):
        """
        :rtype: dict of str, :class:`NodeType`
        """

    @object_dict_field(RelationshipType)
    def relationships(self):
        """
        :rtype: dict of str, :class:`RelationshipType`
        """
        return self._get_object_dict('relationships', RelationshipType)
    
    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        :rtype: dict of str, :class:`NodeTemplate`
        """

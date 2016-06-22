
from ... import has_fields, object_list_field, object_dict_field
from ..tosca import NodeTemplate as BaseNodeTemplate, ServiceTemplate as BaseServiceTemplate
from ..tosca import PropertyDefinition
from .types import NodeType, RelationshipType
from .misc import Relationship, Output, Operation, Plugin

@has_fields
class NodeTemplate(BaseNodeTemplate):
    @object_list_field(Relationship)
    def relationships():
        """
        :rtype: list of :class:`Relationship`
        """

@has_fields
class ServiceTemplate(BaseServiceTemplate):
    @object_dict_field(PropertyDefinition)
    def inputs():
        """
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(Output)
    def outputs():
        """
        :rtype: dict of str, :class:`Output`
        """
    
    @object_dict_field(NodeType)
    def node_types():
        """
        :rtype: dict of str, :class:`NodeType`
        """

    @object_dict_field(RelationshipType)
    def relationships():
        """
        :rtype: dict of str, :class:`RelationshipType`
        """
        return self._get_object_dict('relationships', RelationshipType)
    
    @object_dict_field(NodeTemplate)
    def node_templates():
        """
        :rtype: dict of str, :class:`NodeTemplate`
        """

    @object_dict_field(Operation)
    def workflows():
        """
        :rtype: dict of str, :class:`Operation`
        """
    
    @object_dict_field(Plugin)
    def plugins():
        """
        :rtype: dict of str, :class:`Plugin`
        """

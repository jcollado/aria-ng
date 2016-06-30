
from ... import tosca_specification, has_fields, object_dict_field
from ..tosca import NodeType as BaseNodeType, RelationshipType as BaseRelationshipType
from .definitions import InterfaceDefinition

@has_fields
@tosca_specification('node-types', spec='cloudify-1.3')
class NodeType(BaseNodeType):
    """
    node_types are used for defining common properties and behaviors for node-templates. node-templates can then be created based on these types, inheriting their definitions.

    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-node-types/>`__
    """
    
    @object_dict_field(InterfaceDefinition)
    def interfaces():
        """
        A dictionary of node interfaces.
        
        :class:`InterfaceDefinition`
        """

#@has_fields
#class RelationshipType(BaseRelationshipType):
#    @object_dict_field(InterfaceDefinition)
#    def source_interfaces():
#        """
#        :rtype: dict of str, :class:`InterfaceDefinition`
#        """
#
#    @object_dict_field(InterfaceDefinition)
#    def target_interfaces():
#        """
#        :rtype: dict of str, :class:`InterfaceDefinition`
#        """

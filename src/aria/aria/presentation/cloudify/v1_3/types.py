
from .... import dsl_specification, has_fields, primitive_field, object_dict_field, field_type
from ...tosca.v1_0 import NodeType as BaseNodeType, RelationshipType as BaseRelationshipType
from .definitions import InterfaceDefinition

@has_fields
@dsl_specification('node-types', 'cloudify-1.3')
class NodeType(BaseNodeType):
    """
    node_types are used for defining common properties and behaviors for node-templates. node-templates can then be created based on these types, inheriting their definitions.

    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-node-types/>`__
    """
    
    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        A dictionary of node interfaces.
        
        :class:`InterfaceDefinition`
        """

@has_fields
class RelationshipType(BaseRelationshipType):
    """
    You can declare your own relationship types in the relationships section in the blueprint. This is useful when you want to change the default implementation of how nodes interact.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-relationships/>`__
    """

    @object_dict_field(InterfaceDefinition)
    def source_interfaces(self):
        """
        A dict of interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """

    @object_dict_field(InterfaceDefinition)
    def target_interfaces(self):
        """
        A dict of interfaces.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """
    
    @field_type(str)
    @primitive_field
    def connection_type(self):
        """
        valid values: all_to_all and all_to_one
        
        :rtype: str
        """

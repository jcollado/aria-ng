
from ... import tosca_specification, has_fields, primitive_field, object_field, object_list_field, object_dict_field, field_type
from ..tosca import NodeTemplate as BaseNodeTemplate, ServiceTemplate as BaseServiceTemplate, RelationshipTemplate as BaseRelationshipTemplate
from ..tosca import PropertyDefinition
from .types import NodeType
from .misc import Output, Operation, Plugin, Instances, Scalable

@has_fields
@tosca_specification('relationships', spec='cloudify-1.3')
class RelationshipTemplate(BaseRelationshipTemplate):
    """
    Relationships let you define how nodes relate to one another. For example, a web_server node can be contained_in a vm node or an application node can be connected_to a database node.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-relationships/>`__
    """
    
    @field_type(str)
    @primitive_field
    def target():
        """
        The node's name to relate the current node to.
        
        :rtype: str
        """

@has_fields
@tosca_specification('node-templates', spec='cloudify-1.3')
class NodeTemplate(BaseNodeTemplate):
    """
    node_templates represent the actual instances of node types which would eventually represent a running application/service as described in the blueprint.

    node_templates are more commonly referred to as nodes. nodes can comprise more than one instance. For example, you could define a node which contains two vms. Each vm will then be called a node_instance.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-node-templates/>`__
    """
    
    @object_list_field(RelationshipTemplate)
    def relationships():
        """
        Used for specifying the relationships this node template has with other node templates.
        
        :rtype: list of :class:`RelationshipTemplate`
        """
    
    @object_field(Instances)
    def instances():
        """
        Instances configuration. (Deprecated. Replaced by capabilities.scalable.)
        
        :rtype: :class:`Instances`
        """
    
    @object_field(Scalable)
    def capabilities_scalable():
        """
        :rtype: :class:`Scalable`
        """

@has_fields
class ServiceTemplate(BaseServiceTemplate):
    @object_dict_field(PropertyDefinition)
    @tosca_specification('inputs', spec='cloudify-1.3')
    def inputs():
        """
        Inputs are parameters injected into the blueprint upon deployment creation. These parameters can be referenced by using the get_input intrinsic function.

        Inputs are useful when there's a need to inject parameters to the blueprint which were unknown when the blueprint was created and can be used for distinction between different deployments of the same blueprint.
        
        See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-inputs/>`__
        
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

    @object_dict_field(RelationshipTemplate)
    def relationships():
        """
        :rtype: dict of str, :class:`RelationshipTemplate`
        """
    
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

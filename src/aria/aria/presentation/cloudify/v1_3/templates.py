
from .... import dsl_specification
from ... import Presentation, has_fields, primitive_field, object_field, object_list_field, object_dict_field, field_type, required_field, field_validator, type_validator
from ...tosca.v1_0 import NodeTemplate as BaseNodeTemplate, ServiceTemplate as BaseServiceTemplate, PropertyDefinition
from ..v1_2 import Instances
from .definitions import InterfaceDefinition, GroupDefinition, PolicyDefinition
from .types import NodeType, RelationshipType, PolicyType
from .misc import Output, Workflow, Plugin, Scalable, PolicyTrigger

@has_fields
@dsl_specification('relationships', 'cloudify-1.3')
class RelationshipTemplate(Presentation):
    """
    Relationships let you define how nodes relate to one another. For example, a web_server node can be contained_in a vm node or an application node can be connected_to a database node.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-relationships/>`__
    """

    @field_validator(type_validator('relationship', 'relationship_types'))
    @required_field
    @field_type(str)
    @primitive_field
    def type(self):
        """
        Either a newly declared relationship type or one of the relationship types provided by default when importing the types.yaml file.
        
        :rtype: str
        """
    
    @required_field
    @field_type(str)
    @primitive_field
    def target(self):
        """
        The node's name to relate the current node to.
        
        :rtype: str
        """

    @field_type(str)
    @primitive_field
    def connection_type(self):
        """
        valid values: all_to_all and all_to_one
        
        :rtype: str
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

@has_fields
@dsl_specification('node-templates', 'cloudify-1.3')
class NodeTemplate(BaseNodeTemplate):
    """
    node_templates represent the actual instances of node types which would eventually represent a running application/service as described in the blueprint.

    node_templates are more commonly referred to as nodes. nodes can comprise more than one instance. For example, you could define a node which contains two vms. Each vm will then be called a node_instance.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-node-templates/>`__
    """
    
    @object_list_field(RelationshipTemplate)
    def relationships(self):
        """
        Used for specifying the relationships this node template has with other node templates.
        
        :rtype: list of :class:`RelationshipTemplate`
        """
    
    @object_field(Instances)
    def instances(self):
        """
        Instances configuration. (Deprecated. Replaced by capabilities.scalable.)
        
        :rtype: :class:`Instances`
        """
    
    @object_field(Scalable)
    def capabilities_scalable(self):
        """
        :rtype: :class:`Scalable`
        """

@has_fields
class ServiceTemplate(BaseServiceTemplate):
    @object_dict_field(PropertyDefinition)
    @dsl_specification('inputs', 'cloudify-1.3')
    def inputs(self):
        """
        Inputs are parameters injected into the blueprint upon deployment creation. These parameters can be referenced by using the get_input intrinsic function.

        Inputs are useful when there's a need to inject parameters to the blueprint which were unknown when the blueprint was created and can be used for distinction between different deployments of the same blueprint.
        
        See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-inputs/>`__
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    # Override TOSCA

    @object_dict_field(NodeType)
    def node_types(self):
        """
        :rtype: dict of str, :class:`NodeType`
        """

    @object_dict_field(PolicyType)
    def policy_types(self):
        """
        :rtype: dict of str, :class:`PolicyType`
        """

    # Additions to TOSCA

    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        :rtype: dict of str, :class:`NodeTemplate`
        """

    @object_dict_field(RelationshipType)
    def relationships(self):
        """
        :rtype: dict of str, :class:`RelationshipType`
        """

    @object_dict_field(GroupDefinition)
    def groups(self):
        """
        :rtype: dict of str, :class:`GroupDefinition`
        """

    @object_dict_field(PolicyDefinition)
    def policies(self):
        """
        :rtype: dict of str, :class:`PolicyDefinition`
        """

    @object_dict_field(PolicyTrigger)
    def policy_triggers(self):
        """
        :rtype: dict of str, :class:`PolicyTrigger`
        """
    
    @object_dict_field(Plugin)
    def plugins(self):
        """
        :rtype: dict of str, :class:`Plugin`
        """
    
    @object_dict_field(Workflow)
    def workflows(self):
        """
        :rtype: dict of str, :class:`Workflow`
        """

    @object_dict_field(Output)
    def outputs(self):
        """
        :rtype: dict of str, :class:`Output`
        """

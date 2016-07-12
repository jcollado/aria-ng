
from ..v1_2 import Instances
from .definitions import PropertyDefinition, InterfaceDefinition, GroupDefinition, PolicyDefinition
from .assignments import PropertyAssignment
from .types import NodeType, RelationshipType, PolicyType
from .misc import Output, Workflow, Plugin, Scalable, PolicyTrigger
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, primitive_field, primitive_list_field, object_field, object_list_field, object_dict_field, field_validator, type_validator

from aria_extension_tosca.v1_0.types import DataType

@has_fields
@dsl_specification('relationships-1', 'cloudify-1.3')
class RelationshipTemplate(Presentation):
    """
    Relationships let you define how nodes relate to one another. For example, a web_server node can be contained_in a vm node or an application node can be connected_to a database node.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-relationships/>`__
    """

    @primitive_field(str)
    def description(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @field_validator(type_validator('relationship', 'relationship_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        Either a newly declared relationship type or one of the relationship types provided by default when importing the types.yaml file.
        
        :rtype: str
        """
    
    @primitive_field(str, required=True)
    def target(self):
        """
        The node's name to relate the current node to.
        
        :rtype: str
        """

    @primitive_field(str)
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
class NodeTemplate(Presentation):
    """
    node_templates represent the actual instances of node types which would eventually represent a running application/service as described in the blueprint.

    node_templates are more commonly referred to as nodes. nodes can comprise more than one instance. For example, you could define a node which contains two vms. Each vm will then be called a node_instance.
    
    See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-node-templates/>`__
    """

    @primitive_field(str)
    def description(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @field_validator(type_validator('node type', 'node_types'))
    @primitive_field(str, required=True)
    def type(self):
        """
        The node-type of this node template.
        
        :rtype: str
        """

    @object_dict_field(PropertyAssignment)
    def properties(self):
        """
        The properties of the node template matching its node type properties schema.
        
        :rtype: dict of str, :class:`PropertyAssignment`
        """
    
    @object_field(Instances)
    def instances(self):
        """
        Instances configuration. (Deprecated. Replaced by capabilities.scalable.)
        
        :rtype: :class:`Instances`
        """

    @object_dict_field(InterfaceDefinition)
    def interfaces(self):
        """
        Used for mapping plugins to interfaces operation or for specifying inputs for already mapped node type operations.
        
        :rtype: dict of str, :class:`InterfaceDefinition`
        """
    
    @object_list_field(RelationshipTemplate)
    def relationships(self):
        """
        Used for specifying the relationships this node template has with other node templates.
        
        :rtype: list of :class:`RelationshipTemplate`
        """
    
    @object_dict_field(Scalable)
    def capabilities(self):
        """
        :rtype: dict of str, :class:`Scalable`
        """

@has_fields
class ServiceTemplate(Presentation):
    @primitive_field(str)
    def description(self):
        """
        Not mentioned in the spec.
        
        :rtype: str
        """

    @primitive_field(str)
    @dsl_specification('versioning', 'cloudify-1.3')
    def tosca_definitions_version(self):
        """
        tosca_definitions_version is a top level property of the blueprint which is used to specify the DSL version used. For Cloudify 3.4, the versions that are currently defined are cloudify_dsl_1_0, cloudify_dsl_1_1, cloudify_dsl_1_2 and cloudify_dsl_1_3.

        The version declaration must be included in the main blueprint file. It may also be included in YAML files that are imported in it (transitively), in which case, the version specified in the imported YAMLs must match the version specified in the main blueprint file.

        In future Cloudify versions, as the DSL specification evolves, this mechanism will enable providing backward compatibility for blueprints written in older versions. 
        
        See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-versioning/>`__
        
        :rtype: str
        """

    @primitive_list_field(str)
    @dsl_specification('imports', 'cloudify-1.3')
    def imports(self):
        """
        imports allow the author of a blueprint to reuse blueprint files or parts of them and use predefined types (e.g. from the types.yaml file).
        
        See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-imports/>`__
        
        :rtype: list of :class:`Import`
        """

    @object_dict_field(PropertyDefinition)
    @dsl_specification('inputs', 'cloudify-1.3')
    def inputs(self):
        """
        Inputs are parameters injected into the blueprint upon deployment creation. These parameters can be referenced by using the get_input intrinsic function.

        Inputs are useful when there's a need to inject parameters to the blueprint which were unknown when the blueprint was created and can be used for distinction between different deployments of the same blueprint.
        
        See the `Cloudify DSL v1.3 specification <http://docs.getcloudify.org/3.4.0/blueprints/spec-inputs/>`__
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(NodeTemplate)
    def node_templates(self):
        """
        :rtype: dict of str, :class:`NodeTemplate`
        """

    @object_dict_field(NodeType)
    def node_types(self):
        """
        :rtype: dict of str, :class:`NodeType`
        """

    @object_dict_field(Output)
    def outputs(self):
        """
        :rtype: dict of str, :class:`Output`
        """

    @object_dict_field(RelationshipType)
    def relationships(self):
        """
        :rtype: dict of str, :class:`RelationshipType`
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

    @object_dict_field(PolicyType)
    def policy_types(self):
        """
        :rtype: dict of str, :class:`PolicyType`
        """

    @object_dict_field(PolicyTrigger)
    def policy_triggers(self):
        """
        :rtype: dict of str, :class:`PolicyTrigger`
        """

    @object_dict_field(DataType)
    def data_types(self):
        """
        :rtype: dict of str, :class:`DataType`
        """
